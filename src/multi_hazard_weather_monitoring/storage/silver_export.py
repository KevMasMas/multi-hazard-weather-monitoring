"""Publish an accepted run's immutable snapshot as typed Silver Parquet."""
import hashlib
import json
import os
import tempfile
from datetime import date, datetime
from pathlib import Path


def export_run(connection, run_id: int, destination: Path) -> dict:
    import pyarrow as pa
    import pyarrow.parquet as pq
    with connection.cursor() as cursor:
        cursor.execute('''SELECT r.source_id,r.partition_key,r.status,c.sha256,
                          r.rows_accepted+r.rows_unchanged
            FROM ingestion_run r JOIN raw_capture c ON c.capture_id=r.capture_id
            WHERE r.run_id=%s''',(run_id,))
        run=cursor.fetchone()
        if not run or run[2]!='succeeded':
            raise ValueError('successful_run_required')
        cursor.execute('''SELECT l.record_id,l.capture_id,l.source_line,l.revision_id,
                          v.source_content_sha256,v.normalized_fields
            FROM record_capture_link l JOIN historical_record_revision v
              ON v.revision_id=l.revision_id
            WHERE l.run_id=%s ORDER BY l.record_id''',(run_id,))
        source_rows=cursor.fetchall()
    if len(source_rows)!=run[4]:
        raise ValueError('run_snapshot_not_fully_materialized')
    rows=[]
    for record_id,capture_id,line,revision,digest,fields in source_rows:
        rows.append(dict(record_id=record_id,source=run[0],source_key=fields['source_key'],
            event_type=fields['event_type'],
            observed_at_utc=datetime.fromisoformat(fields['observed_at_utc']) if fields['observed_at_utc'] else None,
            observed_date=date.fromisoformat(fields['observed_date']) if fields['observed_date'] else None,
            latitude=fields['latitude'],longitude=fields['longitude'],
            severity_value=fields['severity_value'],severity_unit=fields['severity_unit'],
            magnitude_type=fields.get('magnitude_type'),quality_attributes=fields.get('quality_attributes'),
            source_content_sha256=digest.strip(),capture_sha256=run[3].strip(),
            run_id=run_id,capture_id=capture_id,source_line=line,revision_id=revision))
    schema=pa.schema([
        ('record_id',pa.int64()),('source',pa.string()),('source_key',pa.string()),('event_type',pa.string()),
        ('observed_at_utc',pa.timestamp('us',tz='UTC')),('observed_date',pa.date32()),
        ('latitude',pa.float64()),('longitude',pa.float64()),('severity_value',pa.float64()),
        ('severity_unit',pa.string()),('magnitude_type',pa.string()),('quality_attributes',pa.string()),
        ('source_content_sha256',pa.string()),('capture_sha256',pa.string()),
        ('run_id',pa.int64()),('capture_id',pa.int64()),('source_line',pa.int64()),('revision_id',pa.int64())],
        metadata={b'weather_schema':b'silver-v1',b'run_id':str(run_id).encode(),
                  b'source':run[0].encode(),b'partition':run[1].encode(),
                  b'lineage':b'Immutable accepted revisions observed in the successful run; no live API.'})
    table=pa.Table.from_pylist(rows,schema=schema)
    destination=Path(destination)
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists():
        existing=pq.read_table(destination)
        if not existing.equals(table,check_metadata=True):
            raise ValueError('existing_silver_output_conflict')
    else:
        descriptor,temporary=tempfile.mkstemp(dir=destination.parent,suffix='.parquet.tmp')
        os.close(descriptor)
        try:
            pq.write_table(table,temporary,compression='snappy')
            if not pq.read_table(temporary).equals(table,check_metadata=True):
                raise ValueError('parquet_roundtrip_mismatch')
            os.replace(temporary,destination)
        finally:
            Path(temporary).unlink(missing_ok=True)
    return dict(path=str(destination),rows=len(rows),run_id=run_id,source=run[0],partition=run[1],
                sha256=hashlib.sha256(destination.read_bytes()).hexdigest().upper(),bytes=destination.stat().st_size,
                producer='immutable_database_snapshot_export',schema='silver-v1')
