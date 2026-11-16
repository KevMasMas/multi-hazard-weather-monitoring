"""Rebuild overlap audit and literal report snippets from saved evidence only."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / 'workshop_1/samples'
FIELDS = ['pair_id', 'source_a', 'record_a_id', 'source_b', 'record_b_id',
          'time_difference', 'position_difference', 'magnitude_difference_with_units',
          'identifier_difference', 'match_status', 'evidence_a', 'evidence_b']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def build_overlap_audit():
    """Return no pairs when the three requested source combinations cannot overlap.

    This intentionally stops if new samples add overlapping years: spatial and
    measurement-window review is then required before any pairs can be emitted.
    """
    rows = []
    for path in sorted(SAMPLES.rglob('*.csv')):
        if 'candidate_pairs' in path.parts:
            continue
        df = pd.read_csv(path)
        if 'BEGIN_DATE_TIME' in df:
            dates = pd.to_datetime(df['BEGIN_DATE_TIME'], format='%d-%b-%y %H:%M:%S')
            source = 'Storm Events'
        elif 'DATE' in df:
            dates = pd.to_datetime(df['DATE'])
            source = 'GHCN-Daily'
        else:
            continue
        rows.append(dict(source=source, path=str(path.relative_to(ROOT)).replace('\\', '/'),
                         start=str(dates.min()), end=str(dates.max()),
                         years=sorted(set(dates.dt.year.astype(int))), records=len(df)))
    for path in sorted(SAMPLES.rglob('*.geojson')):
        features = json.loads(path.read_text(encoding='utf-8-sig')).get('features', [])
        if not features:
            continue
        props = [f['properties'] for f in features]
        observation = 'timestamp' in props[0]
        dates = pd.to_datetime([p['timestamp' if observation else 'effective'] for p in props], utc=True)
        rows.append(dict(source='NWS observations' if observation else 'NWS Alerts',
                         path=str(path.relative_to(ROOT)).replace('\\', '/'),
                         start=str(dates.min()), end=str(dates.max()),
                         years=sorted(set(dates.year.astype(int))), records=len(features)))
    years = {name: set().union(*(set(r['years']) for r in rows if r['source'] == name))
             for name in ['Storm Events', 'GHCN-Daily', 'NWS observations', 'NWS Alerts']}
    # Overlap alone is not a pair: daily aggregation is handled separately.
    return pd.DataFrame(columns=FIELDS), rows


def literal_csv_record(path, index=0):
    # Preserve the exact header and one logical record, including quoted newlines.
    text = path.read_bytes().decode('utf-8-sig')
    lines = text.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(text))
    next(reader)
    header_end = reader.line_num
    previous = header_end
    for number, _ in enumerate(reader):
        if number == index:
            return ''.join(lines[:header_end]) + ''.join(lines[previous:reader.line_num])
        previous = reader.line_num
    raise IndexError(index)


def literal_fields(path, fields):
    # Keep original lexical values rather than serialize parsed numbers again.
    text = path.read_text(encoding='utf-8-sig')
    decoder = json.JSONDecoder()
    feature_start = re.search(r'"features"\s*:\s*\[\s*', text).end()
    _, feature_size = decoder.raw_decode(text[feature_start:])
    text = text[feature_start:feature_start + feature_size]
    parsed_feature = json.loads(text)
    properties_start = re.search(r'"properties"\s*:\s*', text).end()
    _, properties_size = decoder.raw_decode(text[properties_start:])
    properties_text = text[properties_start:properties_start + properties_size]
    selected = []
    for field in fields:
        field_text = text if field == 'id' else properties_text
        # Match only top-level keys, skipping nested dictionaries/lists.
        cursor = 1
        match = None
        while cursor < len(field_text):
            cursor_match = re.match(r'\s*,?\s*', field_text[cursor:])
            cursor += cursor_match.end()
            if field_text[cursor:cursor+1] == '}':
                break
            key, key_size = decoder.raw_decode(field_text[cursor:])
            key_start = cursor
            cursor += key_size
            colon = re.match(r'\s*:\s*', field_text[cursor:])
            cursor += colon.end()
            _, value_size = decoder.raw_decode(field_text[cursor:])
            if key == field:
                selected.append(field_text[key_start:cursor + value_size])
                value = decoder.raw_decode(field_text[cursor:])[0]
                expected = parsed_feature.get(field) if field == 'id' else parsed_feature['properties'][field]
                assert value == expected
                match = True
                break
            cursor += value_size
        if match is None:
            raise KeyError(field)
    return '{\n' + ',\n'.join(selected) + '\n...\n}\n'


def tex_escape(value):
    return ''.join({'\\': r'\textbackslash{}', '_': r'\_', '%': r'\%', '&': r'\&',
                    '#': r'\#', '{': r'\{', '}': r'\}', '$': r'\$'}.get(c, c) for c in str(value))


def main():
    pairs, coverage = build_overlap_audit()
    overlap_csv = SAMPLES/'region_comparison/ghcn_okc_usw00013967_2026_overlap.csv'
    if overlap_csv.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('daily_comparison', Path(__file__).with_name('compare_daily_sources.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        pairs, _, _ = module.build_pairs()
    pair_dir = SAMPLES / 'candidate_pairs'
    pairs.to_csv(pair_dir / 'cross_source_candidate_pairs.csv', index=False, lineterminator='\n')
    audit = dict(status='daily_temperature_candidates' if len(pairs) else 'insufficient_temporal_overlap', cross_source_pairs=len(pairs),
                 old_pairs='intra_NWS_not_counted', coverage=coverage)
    (pair_dir / 'cross_source_overlap_audit.json').write_text(json.dumps(audit, indent=2)+'\n', encoding='utf-8')

    noaa = yaml.safe_load((SAMPLES/'noaa_storm_events/source_metadata.yaml').read_text())
    region = yaml.safe_load((SAMPLES/'region_comparison/source_metadata.yaml').read_text())
    alerts = yaml.safe_load((SAMPLES/'nws_alerts/recent_7d_metadata.yaml').read_text())
    parameters = {key: str(value).lower() if isinstance(value, bool) else value
                  for key, value in region['ghcn_daily']['request_parameters'].items()}
    ghcn_url = 'https://www.ncei.noaa.gov/access/services/data/v1?' + urlencode(parameters)
    specs = [
        ('storm_events', 'NOAA Storm Events (derived subset)', SAMPLES/'noaa_storm_events/details_sample.csv',
         noaa['sample']['sha256'], noaa['source_url'], noaa['retrieved_at'], None),
        ('ghcn_daily', 'NCEI GHCN-Daily', SAMPLES/'region_comparison/ghcn_okc_usw00013967_2025.csv',
         region['ghcn_daily']['sha256'], ghcn_url, '2026-11-05T11:38:49Z (registered local file capture time)', None),
        ('nws_alert', 'NWS Alerts', SAMPLES/'nws_alerts/recent_7d_page_1.geojson',
         alerts['pagination']['page_1']['sha256'], alerts['endpoint'], alerts['retrieved_at_utc'],
         ['id', 'sent', 'effective', 'event', 'severity', 'areaDesc']),
        ('nws_observation', 'NWS station observations', SAMPLES/'region_comparison/nws_kokc_observations_snapshot.geojson',
         region['nws_station_observations']['sha256'], region['nws_station_observations']['request_url'],
         region['nws_station_observations']['local_capture_time_utc'], ['@id', 'timestamp', 'stationId', 'temperature', 'windSpeed']),
    ]
    destination = SAMPLES/'response_snippets'
    destination.mkdir(exist_ok=True)
    manifest, tex = [], [r'\section{Literal saved-response excerpts}',
        'CSV excerpts retain the header and first complete logical row. JSON excerpts retain selected key/value substrings verbatim; the standalone ``...'' line indicates omitted fields and is not JSON syntax. Values are not edited. The NOAA file is a derived subset, not the untouched bulk response. Hashes below identify full input files, not the excerpts.']
    for name, label, path, expected, url, captured, fields in specs:
        assert sha(path) == expected.upper(), f'Checksum mismatch: {path}'
        snippet = literal_fields(path, fields) if fields else literal_csv_record(path)
        out = destination/f'{name}.txt'
        out.write_text(snippet, encoding='utf-8')
        entry = dict(source=label, source_path=str(path.relative_to(ROOT)).replace('\\','/'),
                     source_sha256=sha(path), request=url, captured_at=str(captured),
                     excerpt_path=str(out.relative_to(ROOT)).replace('\\','/'), excerpt_sha256=sha(out))
        manifest.append(entry)
        # Copy derived excerpts into the self-contained Overleaf project.
        asset = ROOT/f'workshop_1/report/assets/{name}.txt'
        asset.write_text(snippet, encoding='utf-8')
        tex += [r'\subsection{' + tex_escape(label) + '}',
                r'\textbf{Input:} \path{' + entry['source_path'] + r'}\par',
                r'\textbf{Request:} \url{' + url + r'}\par',
                r'\textbf{Capture:} ' + tex_escape(captured) + r'\par',
                r'\textbf{SHA-256:} \nolinkurl{' + sha(path) + r'}\par',
                r'\lstinputlisting{assets/' + name + '.txt}']
        if name == 'ghcn_daily':
            tex.append('Request URL reconstructed from saved parameters; the recorded capture time is a local file timestamp, not a persisted HTTP Date header.')
    (destination/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    (ROOT/'workshop_1/report/evidence_appendix.tex').write_text('\n'.join(tex)+'\n', encoding='utf-8')
    print(f'Cross-source pairs: {len(pairs)}; four source checksums verified; four literal excerpts generated.')


if __name__ == '__main__':
    main()
