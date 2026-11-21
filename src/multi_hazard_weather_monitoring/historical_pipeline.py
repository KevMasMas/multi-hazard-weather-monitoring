"""Reusable saved-capture Bronze/Silver stages called by thin Airflow tasks."""
import csv
import hashlib
import io
import json
import os
import tempfile
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from .sources.capture_registry import registered_hashes

ROOT=Path(__file__).resolve().parents[2]


def _atomic_json(path, payload):
    body=(json.dumps(payload,indent=2,sort_keys=True)+'\n').encode()
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=body:
            raise ValueError('existing_batch_output_conflict')
        return
    descriptor,temporary=tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(descriptor,'wb') as stream:
            stream.write(body);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def capture_config(partition):
    entries=json.loads((ROOT/'config/workshop2_saved_captures.json').read_text())['captures']
    matches=[e for e in entries if e['partition']==partition]
    if len(matches)!=1:
        raise ValueError('unknown_or_ambiguous_saved_partition')
    return matches[0]


def bronze_quality_profile(rows, source):
    """Count genuine source text coverage without changing native CSV bytes."""
    result={"source_rows":len(rows),"text_applicable":source=="noaa_storm_events"}
    if result["text_applicable"]:
        result["event_narrative_rows"]=sum(bool((r.get("EVENT_NARRATIVE") or "").strip()) for r in rows)
        result["episode_narrative_rows"]=sum(bool((r.get("EPISODE_NARRATIVE") or "").strip()) for r in rows)
    return result


def verify_bronze_profile(path):
    payload=json.loads(checked_bronze_path(path).read_text(encoding="utf-8"))
    expected=bronze_quality_profile(payload["rows"],payload["source"]["source"])
    if payload.get("quality_profile")!=expected:
        raise ValueError("bronze_quality_profile_mismatch")
    return str(checked_bronze_path(path))


def publish_bronze(partition, batch_id, logical_time):
    from .storage.raw_landing import land_capture,require_registered_capture
    source=capture_config(partition)
    body=(ROOT/source['path']).read_bytes()
    register=registered_hashes(ROOT)
    require_registered_capture(body,source['path'],register)
    capture=land_capture(body,source=source['source'],partition=partition,root=ROOT/'data/raw',content_type='text/csv',origin=source['path'])
    parsed=datetime.fromisoformat(logical_time)
    if parsed.utcoffset() is None:
        raise ValueError('logical_time_requires_timezone')
    timestamp=parsed.astimezone(timezone.utc).strftime('%Y%m%d_%H%M%S')
    token=hashlib.sha256(batch_id.encode()).hexdigest()[:12]
    path=ROOT/'data/bronze'/f"{source['source']}_{timestamp}_{token}.json"
    rows=list(csv.DictReader(io.StringIO(body.decode('utf-8-sig'),newline='')))
    payload=dict(schema='bronze-csv-view-v1',batch_id=batch_id,logical_time=logical_time,
        source=source,original_capture=capture,
        evidence_type='Parsed registered CSV view, not an original JSON response. See source_format and acquisition_manifest for native response and subset lineage.',
        quality_profile=bronze_quality_profile(rows,source['source']),rows=rows)
    _atomic_json(path,payload)
    return str(path)


def checked_bronze_path(path):
    resolved=Path(path).resolve()
    if not resolved.is_relative_to((ROOT/'data/bronze').resolve()) or resolved.suffix!='.json':
        raise ValueError('bronze_path_outside_landing')
    return resolved


def process_bronze(path):
    from ingest import _connect,PARSERS
    from .storage.migrations import migrate
    from .storage.raw_landing import require_registered_capture
    from .storage.postgres_historical import load_partition
    from .storage.silver_export import export_run
    from .text_silver import mirror_numeric_silver
    path=checked_bronze_path(path)
    encoded=path.read_bytes();payload=json.loads(encoded)
    if payload.get('schema')!='bronze-csv-view-v1':
        raise ValueError('unsupported_bronze_schema')
    source=capture_config(payload['source']['partition'])
    if payload['source']!=source:
        raise ValueError('bronze_source_configuration_mismatch')
    capture=payload['original_capture']
    if (capture.get('source'),capture.get('partition'),capture.get('origin'),capture.get('content_type'))!=(source['source'],source['partition'],source['path'],'text/csv'):
        raise ValueError('bronze_capture_provenance_mismatch')
    native=(ROOT/'data/raw'/capture['raw_path']).resolve()
    if not native.is_relative_to((ROOT/'data/raw').resolve()):
        raise ValueError('raw_path_outside_landing')
    body=native.read_bytes()
    register=registered_hashes(ROOT)
    require_registered_capture(body,source['path'],register)
    if hashlib.sha256(body).hexdigest()!=capture['sha256'] or len(body)!=capture['byte_count']:
        raise ValueError('bronze_native_capture_mismatch')
    if payload['rows']!=list(csv.DictReader(io.StringIO(body.decode('utf-8-sig'),newline=''))):
        raise ValueError('bronze_parsed_view_mismatch')
    if 'quality_profile' in payload and payload['quality_profile']!=bronze_quality_profile(payload['rows'],source['source']):
        raise ValueError('bronze_quality_profile_mismatch')
    with closing(_connect()) as connection:
        migrate(connection)
        metrics=load_partition(connection,source=source,capture=capture,
            records=PARSERS[source['source']](body),batch_key=hashlib.sha256(encoded).hexdigest())
        destination=ROOT/'data/curated/silver'/(path.stem+'.parquet')
        output=export_run(connection,metrics['run_id'],destination)
    output['path']=destination.relative_to(ROOT).as_posix()
    receipt=dict(bronze_path=path.relative_to(ROOT).as_posix(),
        bronze_sha256=hashlib.sha256(encoded).hexdigest().upper(),native_sha256=capture['sha256'],
        metrics=metrics,silver=output)
    manifest=destination.with_suffix('.manifest.json')
    _atomic_json(manifest,receipt)
    mirror_numeric_silver(destination, ROOT)
    return str(manifest)
