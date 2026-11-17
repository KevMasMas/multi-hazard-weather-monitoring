"""Capture actual database counts, historical coverage and rejection metrics."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ingest import _connect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='workshop_2/evidence/delivery_database.json')
    args = parser.parse_args()
    proof = dict(verified_at_utc=datetime.now(timezone.utc).isoformat(), weather_network=False)
    with closing(_connect()) as connection, connection.cursor() as cursor:
        def rows(sql):
            cursor.execute(sql)
            names = [column[0] for column in cursor.description]
            return [dict(zip(names, row)) for row in cursor.fetchall()]
        proof['versions'] = rows('SELECT version() AS postgres, postgis_full_version() AS postgis')
        proof['sources'] = rows('''SELECT source_id,count(*) AS records,
            min(coalesce(observed_date,observed_at_utc::date)) AS first_date,
            max(coalesce(observed_date,observed_at_utc::date)) AS last_date,
            count(*) FILTER (WHERE latitude IS NULL) AS missing_point
            FROM historical_record GROUP BY source_id ORDER BY source_id''')
        proof['duplicate_business_keys'] = rows('''SELECT source_id,source_key,count(*) FROM historical_record
            GROUP BY source_id,source_key HAVING count(*)>1''')
        proof['tables'] = rows('''SELECT table_name FROM information_schema.tables WHERE table_schema='public'
            AND table_type='BASE TABLE' ORDER BY table_name''')
        proof['migrations'] = rows('SELECT * FROM schema_migration ORDER BY 1')
        proof['latest_partitions'] = rows('''SELECT r.run_id,r.source_id,r.partition_key,r.rows_read,
            r.rows_accepted,r.rows_rejected,r.rows_unchanged,r.status,r.finished_at_utc
            FROM ingestion_state s JOIN ingestion_run r ON r.run_id=s.last_successful_run_id
            ORDER BY r.source_id,r.partition_key''')
        proof['reject_reasons'] = rows('''SELECT reason_code,count(*) AS records FROM rejected_record
            GROUP BY reason_code ORDER BY reason_code''')
        proof['domains'] = {}
        for table in ['historical_record_revision','record_capture_link','storm_event','station',
                      'daily_station_measurement','source_geography','region','station_region_assignment']:
            cursor.execute('SELECT count(*) FROM ' + table)
            proof['domains'][table] = cursor.fetchone()[0]
        proof['daily_years'] = rows('''SELECT extract(year FROM observation_date)::int AS year,
            count(DISTINCT observation_date) AS days,count(*) AS measurements,
            count(DISTINCT station_id) AS stations FROM daily_station_measurement
            GROUP BY 1 ORDER BY 1''')
        proof['event_years'] = rows('''SELECT (s.source_fields->>'YEAR')::int AS year,count(*) AS events,
            count(*) FILTER (WHERE s.source_fields->>'STATE'='OKLAHOMA') AS oklahoma_events
            FROM storm_event s GROUP BY 1 ORDER BY 1''')
    proof['native_capture_checks'] = []
    acquired = json.loads((ROOT/'workshop_2/evidence/historical_acquisition.json').read_text())
    for entry in acquired['captures']:
        native = entry['native_capture']
        for path, digest in [(native['path'], native['sha256']), (entry['path'], entry['input_sha256'])]:
            actual = hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper()
            if actual != digest.upper():
                raise ValueError('capture_checksum_mismatch:' + path)
        proof['native_capture_checks'].append(dict(partition=entry['partition'], verified=True,
                                                   native_sha256=native['sha256'], input_sha256=entry['input_sha256']))
    (ROOT/args.output).write_text(json.dumps(proof, indent=2, default=str) + '\n')
    print(json.dumps(dict(sources=proof['sources'], duplicates=len(proof['duplicate_business_keys']),
                         capture_checks=len(proof['native_capture_checks'])), default=str))


if __name__ == '__main__':
    main()
