"""Explicit, cached acquisition of the Workshop 2 five-year historical slice.

Network access occurs only when this script is explicitly invoked. Original
response bytes, URL, UTC capture time and SHA-256 are retained before subsetting.
"""
import argparse
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
INDEX = 'https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/'
USER_AGENT = 'UD-Team9-WeatherMonitoring/Workshop2 educational historical acquisition'


def sha(body):
    return hashlib.sha256(body).hexdigest().upper()


def fetch(url, target):
    """Reuse a checksum-verified cached response; never overwrite it silently."""
    meta = target.with_suffix(target.suffix + '.capture.json')
    if target.exists() and meta.exists():
        record = json.loads(meta.read_text())
        body = target.read_bytes()
        if record['url'] != url or record['sha256'] != sha(body):
            raise ValueError('cached_capture_mismatch')
        return body, record
    target.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': USER_AGENT}), timeout=120) as response:
                body = response.read()
                record = dict(url=url, captured_at_utc=datetime.now(timezone.utc).isoformat(),
                              sha256=sha(body), bytes=len(body), status=response.status,
                              content_type=response.headers.get('Content-Type'),
                              last_modified=response.headers.get('Last-Modified'),
                              path=target.relative_to(ROOT).as_posix())
            target.write_bytes(body)
            meta.write_text(json.dumps(record, indent=2) + '\n')
            return body, record
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start-year', type=int, default=2021)
    parser.add_argument('--end-year', type=int, default=2025)
    args = parser.parse_args()
    if not 1950 <= args.start_year <= args.end_year <= 2025:
        parser.error('Use complete years 1950..2025 in ascending order.')
    folder = ROOT / 'data/raw/acquired'
    directory, index_capture = fetch(INDEX, folder / 'storm_directory.html')
    names = re.findall(r'StormEvents_details-ftp_v1\.0_d\d{4}_c\d{8}\.csv\.gz', directory.decode())
    evidence = dict(schema='historical-acquisition-v1', index_capture=index_capture,
                    scope='Oklahoma Storm Events; one Oklahoma City GHCN station, not a statewide station inventory',
                    input_sha256={}, captures=[])
    config = json.loads((ROOT / 'config/workshop2_saved_captures.json').read_text())
    for year in range(args.start_year, args.end_year + 1):
        matching = sorted({name for name in names if f'_d{year}_' in name})
        if not matching:
            raise ValueError(f'no_official_archive_for_{year}')
        body, native = fetch(INDEX + matching[-1], folder / matching[-1])
        with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
            reader = csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig', newline=''))
            fields = reader.fieldnames
            rows = [row for row in reader if row.get('STATE') == 'OKLAHOMA']
        if not rows:
            raise ValueError('empty_oklahoma_subset')
        output = io.StringIO(newline='')
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
        subset = output.getvalue().encode('utf-8')
        path = folder / f'noaa_oklahoma_{year}.csv'
        path.write_bytes(subset)
        entry = dict(source='noaa_storm_events', partition=f'OK_{year}', path=path.relative_to(ROOT).as_posix(),
                     start=f'{year}-01-01', end=f'{year}-12-31', source_url=native['url'],
                     source_format='csv_subset_of_preserved_gzip_archive', attribution='NOAA NCEI Storm Events',
                     acquisition_manifest='workshop_2/evidence/historical_acquisition.json')
        evidence['input_sha256'][entry['path']] = sha(subset)
        evidence['captures'].append(dict(**entry, native_capture=native, input_sha256=sha(subset),
                                        csv_rows=len(rows), transformation="Decompress gzip; retain STATE == 'OKLAHOMA'; preserve field values; serialize UTF-8 CSV with LF."))
        config['captures'] = [old for old in config['captures'] if old['partition'] != entry['partition']] + [entry]
        params = dict(dataset='daily-summaries', stations='USW00013967', startDate=f'{year}-01-01',
                      endDate=f'{year}-12-31', dataTypes='TMAX,TMIN,PRCP', units='metric',
                      includeAttributes='true', includeStationName='true', includeStationLocation='true', format='csv')
        url = 'https://www.ncei.noaa.gov/access/services/data/v1?' + urlencode(params)
        path = folder / f'ghcn_USW00013967_{year}.csv'
        body, native = fetch(url, path)
        rows = list(csv.DictReader(io.StringIO(body.decode('utf-8-sig'))))
        if not rows or any(row.get('STATION') != 'USW00013967' or not row.get('DATE', '').startswith(str(year)) for row in rows):
            raise ValueError('unexpected_ghcn_response')
        # Keep older Workshop 1 partitions immutable; distinguish this acquisition.
        entry = dict(source='ghcn_daily', partition=f'USW00013967_{year}_full',
                     path=path.relative_to(ROOT).as_posix(), start=f'{year}-01-01', end=f'{year}-12-31',
                     source_url=url, source_format='csv', attribution='NOAA NCEI GHCN-Daily; metric response',
                     acquisition_manifest='workshop_2/evidence/historical_acquisition.json')
        evidence['input_sha256'][entry['path']] = sha(body)
        evidence['captures'].append(dict(**entry, native_capture=native, input_sha256=sha(body),
                                        csv_rows=len(rows), transformation='None: original CSV response bytes.'))
        config['captures'] = [old for old in config['captures'] if old['partition'] != entry['partition']] + [entry]
        (ROOT / 'config/workshop2_saved_captures.json').write_text(json.dumps(config, indent=2) + '\n')
        (ROOT / 'workshop_2/evidence/historical_acquisition.json').write_text(json.dumps(evidence, indent=2) + '\n')
        print(f'{year}: Oklahoma NOAA subset and GHCN response saved and registered', flush=True)
        time.sleep(1)


if __name__ == '__main__':
    main()
