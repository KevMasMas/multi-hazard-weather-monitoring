"""Synthetic fault scenarios, plus real isolated PostGIS transactions. No network."""
import copy
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError, URLError
import uuid

from multi_hazard_weather_monitoring.incremental import (normalize,utc,decode_page,fetch_pages,
    persist_poll,status,station_window)
from multi_hazard_weather_monitoring.event_candidates import build_candidates
from multi_hazard_weather_monitoring.storage.migrations import migrate

ROOT=Path(__file__).resolve().parents[1]
URL=os.environ.get('WORKSHOP2_TEST_DATABASE_URL')


def observation(value=12, hour='10:00', key=None):
    stamp='2026-11-01T'+hour+':00+00:00'
    return {'type':'Feature','id':key or 'https://api.weather.gov/stations/KOKC/observations/'+stamp,
            'geometry':{'type':'Point','coordinates':[-97.6,35.4]},
            'properties':{'stationId':'KOKC','timestamp':stamp,
                          'temperature':{'value':value,'unitCode':'wmoUnit:degC','qualityControl':'V'},
                          'windSpeed':{'value':36,'unitCode':'wmoUnit:km_h-1','qualityControl':'V'}}}


def page(features,next_url=None):
    obj={'type':'FeatureCollection','features':features}
    if next_url:obj['pagination']={'next':next_url}
    body=json.dumps(obj).encode()
    return {'body':body,'sha256':hashlib.sha256(body).hexdigest(),'origin':'https://api.weather.gov/stations/KOKC/observations',
            'retrieved_at_utc':'2026-11-01T12:00:00Z','raw_path':'synthetic_test_only'}


class SourceTests(unittest.TestCase):
    def test_overlap_daily_reconciliation_and_retention_gap(self):
        from datetime import timedelta
        policy=json.loads((ROOT/'config/workshop3_incremental.json').read_text())
        now=utc('2026-11-10T12:00:00Z');previous=now-timedelta(hours=1)
        self.assertEqual(utc(station_window(policy,now,previous,previous)['start_utc']),now-timedelta(hours=2))
        self.assertEqual(station_window(policy,now,previous,now-timedelta(days=1))['reconciliation'],'full')
        full=station_window(policy,now,now-timedelta(days=9),None)
        self.assertEqual(utc(full['start_utc']),now-timedelta(days=7))
        self.assertIsNotNone(full['retention_gap_before_utc'])

    def test_conversion_missing_units_qc_and_offsets(self):
        f=observation()
        f['properties']['temperature']={'value':68,'unitCode':'wmoUnit:degF','qualityControl':'C'}
        f['properties']['dewpoint']={'value':None,'unitCode':'wmoUnit:degC','qualityControl':'Z'}
        f['properties']['windGust']={'value':99,'unitCode':'future:unknown'}
        values=normalize(f,'nws_station_observations','KOKC')['fields']['measurements']
        self.assertAlmostEqual(values['temperature']['value'],20)
        self.assertEqual(values['temperature']['quality_control'],'C')
        self.assertEqual(values['windSpeed']['value'],10)
        self.assertIsNone(values['dewpoint']['value'])
        self.assertEqual(values['windGust']['conversion_status'],'unsupported_unit')
        f['properties']['precipitationLastHour']={'value':0.001,'unitCode':'wmoUnit:m'}
        self.assertEqual(normalize(f,'nws_station_observations','KOKC')['fields']['measurements']['precipitationLastHour']['value'],1)
        self.assertEqual(utc('2026-11-01T05:00:00-05:00'),utc('2026-11-01T10:00:00Z'))
        with self.assertRaises(ValueError):utc('2026-11-01T10:00:00')

    def test_bad_station_coordinate_and_schema(self):
        f=observation(); f['geometry']['coordinates'][1]=100
        with self.assertRaisesRegex(ValueError,'coordinates'):normalize(f,'nws_station_observations','KOKC')
        f=observation(); f['properties']['stationId']='KDEN'
        with self.assertRaisesRegex(ValueError,'scope'):normalize(f,'nws_station_observations','KOKC')
        with self.assertRaisesRegex(ValueError,'collection'):decode_page(b'{"features":[]}')

    def test_retry_429_then_success_and_landing(self):
        calls=[]; delays=[]
        def opener(request,timeout):
            calls.append(request)
            if len(calls)==1:raise HTTPError(request.full_url,429,'rate limit',{'Retry-After':'7'},None)
            return io.BytesIO(page([])['body'])
        with tempfile.TemporaryDirectory() as directory:
            out=fetch_pages('https://api.weather.gov/alerts/active?area=OK',Path(directory),'nws_alerts','OK','team9-test',opener,delays.append)
            self.assertEqual(delays,[7]); self.assertEqual(len(out),1)
            self.assertTrue((Path(directory)/'data/raw'/out[0]['raw_path']).exists())

    def test_timeout_budget_and_untrusted_pagination(self):
        calls=[]
        def timeout(*args,**kwargs):calls.append(1); raise URLError('synthetic timeout')
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(URLError):fetch_pages('https://api.weather.gov/alerts',Path(directory),'nws_alerts','OK','test',timeout,lambda _:None)
        self.assertEqual(len(calls),4)
        with self.assertRaisesRegex(ValueError,'untrusted'):decode_page(page([], 'https://example.test/steal')['body'])

    def test_pagination_cycle_and_page_limit(self):
        url='https://api.weather.gov/alerts'
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError,'cycle'):
                fetch_pages(url,Path(directory),'nws_alerts','OK','test',lambda *a,**k:io.BytesIO(page([],url)['body']))
            with self.assertRaisesRegex(ValueError,'page_limit'):
                fetch_pages(url,Path(directory),'nws_alerts','OK','test',lambda *a,**k:io.BytesIO(page([],url+'?next=1')['body']),max_pages=1)


@unittest.skipUnless(URL,'Disposable PostGIS URL required')
class TransactionTests(unittest.TestCase):
    def setUp(self):
        import psycopg2
        from psycopg2 import sql
        self.conn=psycopg2.connect(URL); self.sql=sql
        self.schema='w3_test_'+uuid.uuid4().hex
        with self.conn.cursor() as c:
            c.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(self.schema)))
            c.execute(sql.SQL('SET search_path TO {},public').format(sql.Identifier(self.schema)))
        self.conn.commit(); self.addCleanup(self.cleanup); migrate(self.conn)

    def cleanup(self):
        self.conn.rollback()
        with self.conn.cursor() as c:c.execute(self.sql.SQL('DROP SCHEMA {} CASCADE').format(self.sql.Identifier(self.schema)))
        self.conn.commit();self.conn.close()

    def poll(self,features,stamp='2026-11-01T12:00:00Z',complete=True,pages=None):
        return persist_poll(self.conn,'nws_station_observations','KOKC','test',stamp,pages or [page(features)],complete)

    def count(self,table):
        with self.conn.cursor() as c:
            c.execute(self.sql.SQL('SELECT count(*) FROM {}').format(self.sql.Identifier(table)))
            return c.fetchone()[0]

    def test_new_unchanged_changed_and_late_observation(self):
        self.assertEqual(self.poll([observation()])['new'],1)
        self.assertEqual(self.poll([observation()])['unchanged'],1)
        self.assertEqual(self.poll([observation(14)])['changed'],1)
        self.assertEqual(self.poll([observation(9,'09:00')],'2026-11-01T13:00:00Z')['new'],1)
        self.assertEqual((self.count('incremental_record'),self.count('incremental_revision')),(2,3))
        self.assertEqual(self.count('incremental_sighting'),4)
        with self.conn.cursor() as c:
            c.execute("SELECT raw_fields->'properties'->'temperature'->>'value' FROM incremental_revision ORDER BY revision_id")
            self.assertEqual([r[0] for r in c.fetchall()],['12','14','9'])

    def test_partial_quarantine_and_empty_do_not_delete(self):
        self.assertFalse(self.poll([observation()],complete=False)['watermark_advanced'])
        self.assertEqual(self.count('incremental_state'),0)
        f=observation();f['properties']['timestamp']='bad'
        out=self.poll([f]);self.assertEqual(out['rejected'],1)
        self.assertFalse(out['watermark_advanced']);self.assertEqual(self.count('incremental_state'),0)
        self.assertTrue(self.poll([])['watermark_advanced'])
        self.assertEqual(self.count('incremental_record'),1)

    def test_page_failure_leaves_state_and_retry_recovers(self):
        self.poll([observation()])
        before=status(self.conn)['states'][0]['last_successful_query_at_utc']
        with self.assertRaisesRegex(ValueError,'incomplete'):
            self.poll([],stamp='2026-11-01T13:00:00Z',pages=[page([observation(90)],'https://api.weather.gov/missing')])
        self.assertEqual(status(self.conn)['states'][0]['last_successful_query_at_utc'],before)
        self.assertEqual(self.count('incremental_revision'),1)
        self.assertEqual(status(self.conn)['recent_polls'][0]['status'],'failed')
        self.assertEqual(self.poll([observation(13)],'2026-11-01T13:00:00Z')['changed'],1)

    def test_transaction_failure_after_upsert_rolls_back(self):
        self.poll([observation()])
        with self.conn.cursor() as c:
            c.execute("CREATE FUNCTION fail_revision() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'synthetic forced failure'; END $$")
            c.execute('CREATE TRIGGER fail_revision BEFORE INSERT ON incremental_revision FOR EACH ROW EXECUTE FUNCTION fail_revision()')
        self.conn.commit()
        with self.assertRaises(Exception):self.poll([observation(99)],'2026-11-01T13:00:00Z')
        with self.conn.cursor() as c:
            c.execute("SELECT normalized_fields->'measurements'->'temperature'->>'value' FROM incremental_record")
            self.assertEqual(c.fetchone()[0],'12')
            c.execute('DROP TRIGGER fail_revision ON incremental_revision')
        self.conn.commit()
        self.assertEqual(self.poll([observation(99)],'2026-11-01T13:00:00Z')['changed'],1)
        self.assertEqual(self.count('incremental_revision'),2)

    def test_hash_mismatch_stale_query_and_duplicate_id(self):
        self.poll([observation()])
        with self.assertRaisesRegex(ValueError,'out_of_order'):self.poll([observation(99)],'2026-11-01T11:00:00Z')
        p=page([observation(99)]);p['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'hash_mismatch'):self.poll([],pages=[p])
        out=self.poll([observation(),observation()]);self.assertEqual(out['rejected'],1)
        self.assertEqual(self.count('incremental_record'),1)

    def test_polygon_time_candidates_are_idempotent_and_unconfirmed(self):
        alert={'type':'Feature','id':'https://api.weather.gov/alerts/synthetic-test-only',
               'geometry':{'type':'Polygon','coordinates':[[[-98,35],[-97,35],[-97,36],[-98,36],[-98,35]]]},
               'properties':{'sent':'2026-11-01T09:00:00Z','effective':'2026-11-01T09:00:00Z','expires':'2026-11-01T11:00:00Z','event':'High Wind Warning','severity':'Severe'}}
        persist_poll(self.conn,'nws_alerts','OK','test','2026-11-01T12:00:00Z',[page([alert])],True)
        self.poll([observation(),observation(hour='12:00')])
        pairs=build_candidates(self.conn,'test');self.assertEqual(len(pairs),1)
        self.assertEqual(pairs[0]['review_status'],'candidate_not_confirmed')
        build_candidates(self.conn,'test');self.assertEqual(self.count('event_candidate'),1)
        self.assertEqual(self.count('integrated_weather_record'),0) # test/replay never operational


if __name__=='__main__':unittest.main(verbosity=2)
