"""Opt-in real PostGIS tests; isolated temporary schema, never a live API.

Set WORKSHOP2_TEST_DATABASE_URL to a disposable development database. Requires
CREATE SCHEMA permission and PostGIS. Without it these are reported as skipped.
"""
import os
import json
import unittest
import uuid
from pathlib import Path
from multi_hazard_weather_monitoring.sources.historical_samples import parse_ghcn_daily, parse_noaa_storm_events
from multi_hazard_weather_monitoring.storage.postgres_historical import load_partition
from multi_hazard_weather_monitoring.storage.migrations import migrate

URL = os.environ.get('WORKSHOP2_TEST_DATABASE_URL')
ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(URL, 'Set WORKSHOP2_TEST_DATABASE_URL for real PostGIS integration tests')
class PostGISIntegrationTests(unittest.TestCase):
    def setUp(self):
        import psycopg2
        from psycopg2 import sql
        self.sql = sql
        self.conn = psycopg2.connect(URL)
        self.schema = 'w2_test_' + uuid.uuid4().hex
        with self.conn.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public')
            cursor.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(self.schema)))
            cursor.execute(sql.SQL('SET search_path TO {}, public').format(sql.Identifier(self.schema)))
        self.conn.commit()
        self.addCleanup(self.cleanup_schema)
        migrate(self.conn)
        self.source = dict(source='ghcn_daily',partition='fixture',source_url='https://example.test',source_format='csv',attribution='synthetic test')
        self.capture = dict(raw_path='synthetic/fixture.csv',content_type='text/csv',byte_count=1,sha256='a'*64,origin='synthetic fixture')

    def cleanup_schema(self):
        self.conn.rollback()
        with self.conn.cursor() as cursor:
            # Only the UUID schema created by this test; never public/application tables.
            cursor.execute(self.sql.SQL('DROP SCHEMA {} CASCADE').format(self.sql.Identifier(self.schema)))
        self.conn.commit()
        self.conn.close()

    def count(self, table):
        with self.conn.cursor() as cursor:
            cursor.execute(self.sql.SQL('SELECT count(*) FROM {}').format(self.sql.Identifier(table)))
            return cursor.fetchone()[0]

    def rows(self):
        return list(parse_ghcn_daily(b'STATION,DATE,PRCP,TMAX,TMIN\nS,2025-01-01,1,12,3\nS,2025-01-02,-1,13,4\n'))

    def test_load_rerun_and_quarantine(self):
        first=load_partition(self.conn, source=self.source,capture=self.capture,records=self.rows())
        self.assertEqual(first,dict(read=6,accepted=5,rejected=1,unchanged=0))
        second=load_partition(self.conn, source=self.source,capture=self.capture,records=self.rows())
        self.assertEqual(second,dict(read=6,accepted=0,rejected=1,unchanged=5))
        self.assertEqual((self.count('historical_record'),self.count('ingestion_run'),self.count('ingestion_state')),(5,2,1))
        self.assertEqual(self.count('rejected_record'),2)  # one reject per actual run
        self.assertEqual(self.count('daily_station_measurement'),5)
        self.assertEqual(self.count('historical_record_revision'),5)
        self.assertEqual(self.count('record_capture_link'),10)

    def test_revised_value_preserves_old_payload_and_replay_adds_no_revision(self):
        row=self.rows()[0]
        load_partition(self.conn,source=self.source,capture=self.capture,records=[row])
        revised=next(parse_ghcn_daily(b'STATION,DATE,PRCP\nS,2025-01-01,7\n'))
        capture=dict(self.capture,sha256='b'*64,raw_path='synthetic/revised.csv')
        load_partition(self.conn,source=self.source,capture=capture,records=[revised])
        load_partition(self.conn,source=self.source,capture=capture,records=[revised])
        self.assertEqual(self.count('historical_record'),1)
        self.assertEqual(self.count('historical_record_revision'),2)
        self.assertEqual(self.count('record_capture_link'),3)
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT raw_fields->>'PRCP' FROM historical_record_revision ORDER BY revision_id")
            self.assertEqual([r[0] for r in cursor.fetchall()],['1','7'])
            cursor.execute('SELECT value FROM daily_station_measurement')
            self.assertEqual(cursor.fetchone()[0],7)
            cursor.execute('''SELECT r.raw_fields->>'PRCP' FROM record_capture_link l
                JOIN historical_record_revision r ON r.revision_id=l.revision_id ORDER BY l.run_id''')
            self.assertEqual([r[0] for r in cursor.fetchall()],['1','7','7'])

    def test_migrations_are_repeatable_and_refuse_changed_applied_sql(self):
        import tempfile
        self.assertEqual(migrate(self.conn),[])
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'001_historical_schema.sql'
            target.write_text('-- changed already applied migration\n')
            with self.assertRaisesRegex(ValueError,'applied_migration_changed'):
                migrate(self.conn,Path(directory))
        self.assertEqual(self.count('schema_migration'),4)

    def test_pipeline_batch_retry_reuses_committed_run(self):
        key='f'*64
        first=load_partition(self.conn,source=self.source,capture=self.capture,records=[self.rows()[0]],batch_key=key)
        second=load_partition(self.conn,source=self.source,capture=self.capture,records=[self.rows()[0]],batch_key=key)
        self.assertEqual(first,second)
        self.assertEqual(self.count('ingestion_run'),1)
        self.assertEqual(self.count('record_capture_link'),1)
        with self.assertRaisesRegex(ValueError,'batch_capture_identity_conflict'):
            load_partition(self.conn,source=self.source,capture=dict(self.capture,sha256='b'*64),records=[],batch_key=key)

    def test_storm_domain_retains_zone_without_fabricated_point(self):
        row=next(parse_noaa_storm_events((ROOT/'workshop_1/samples/noaa_storm_events/details_sample.csv').read_bytes()))
        source=dict(self.source,source='noaa_storm_events')
        load_partition(self.conn,source=source,capture=self.capture,records=[row])
        with self.conn.cursor() as cursor:
            cursor.execute('''SELECT s.source_event_id,g.geography_type,h.latitude,
                s.source_fields->>'CZ_NAME' FROM storm_event s
                JOIN historical_record h USING(record_id)
                JOIN source_geography g ON g.geography_id=s.geography_id''')
            self.assertEqual(cursor.fetchone(),('1155350','Z',None,'CIMARRON'))
        self.assertEqual(self.count('region'),0)
        self.assertEqual(self.count('station_region_assignment'),0)

    def test_silver_keeps_run_snapshot_after_later_source_revision(self):
        import importlib.util
        if importlib.util.find_spec('pyarrow') is None:
            self.skipTest('Install requirements-workshop2-pipeline.txt for Parquet verification')
        import tempfile
        import pyarrow.parquet as pq
        from multi_hazard_weather_monitoring.storage.silver_export import export_run
        load_partition(self.conn,source=self.source,capture=self.capture,records=[self.rows()[0]])
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT last_successful_run_id FROM ingestion_state')
            original_run=cursor.fetchone()[0]
        revised=next(parse_ghcn_daily(b'STATION,DATE,PRCP\nS,2025-01-01,7\n'))
        load_partition(self.conn,source=self.source,capture=dict(self.capture,sha256='b'*64),records=[revised])
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT last_successful_run_id FROM ingestion_state')
            revised_run=cursor.fetchone()[0]
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'output.parquet'
            first=export_run(self.conn,original_run,path)
            self.assertEqual(pq.read_table(path).column('severity_value').to_pylist(),[1])
            self.assertEqual(pq.read_table(path).column('observed_at_utc').null_count,1)
            self.assertEqual(export_run(self.conn,original_run,path)['sha256'],first['sha256'])
            with self.assertRaisesRegex(ValueError,'existing_silver_output_conflict'):
                export_run(self.conn,revised_run,path)
            with self.assertRaisesRegex(ValueError,'successful_run_required'):
                export_run(self.conn,-1,Path(directory)/'bad.parquet')

    def test_mid_partition_failure_leaves_no_state_or_partial_rows(self):
        def failing():
            yield self.rows()[0]
            raise RuntimeError('injected_after_first_row')
        with self.assertRaisesRegex(RuntimeError,'injected_after_first_row'):
            load_partition(self.conn,source=self.source,capture=self.capture,records=failing())
        for table in ['historical_record','raw_capture','ingestion_run','ingestion_state']:
            self.assertEqual(self.count(table),0,table)

    def test_failure_after_success_preserves_prior_checkpoint(self):
        load_partition(self.conn,source=self.source,capture=self.capture,records=self.rows())
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT last_successful_run_id FROM ingestion_state')
            prior=cursor.fetchone()[0]
        def failing():
            row=dict(self.rows()[0],severity_value=7,source_content_sha256='b'*64)
            yield row
            raise RuntimeError('injected_update_failure')
        with self.assertRaisesRegex(RuntimeError,'injected_update_failure'):
            load_partition(self.conn,source=self.source,capture=self.capture,records=failing())
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT last_successful_run_id FROM ingestion_state')
            self.assertEqual(cursor.fetchone()[0],prior)
            cursor.execute("SELECT severity_value FROM historical_record WHERE source_key='S/2025-01-01/PRCP'")
            self.assertEqual(cursor.fetchone()[0],1)
        self.assertEqual(self.count('ingestion_run'),1)
