"""Run saved captures twice, export actual counts and candidate relationships.

No weather network. This extends the local DB additively; never resets it.
"""
from contextlib import closing
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
import psycopg2

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from multi_hazard_weather_monitoring.incremental import replay,status
from multi_hazard_weather_monitoring.event_candidates import build_candidates,import_historical_context
from multi_hazard_weather_monitoring.storage.migrations import migrate


def write(name,value):
    (ROOT/'workshop_3/evidence'/name).write_text(json.dumps(value,indent=2,default=str)+'\n')


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--tests-only',action='store_true',help='Refresh tests without replacing the first saved replay evidence')
    args=parser.parse_args()
    url=os.environ['DATABASE_URL']
    os.environ['WORKSHOP2_TEST_DATABASE_URL']=url
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_incremental.py')
    results=unittest.TextTestRunner(verbosity=2).run(suite)
    files=['src/multi_hazard_weather_monitoring/incremental.py','src/multi_hazard_weather_monitoring/event_candidates.py',
           'src/multi_hazard_weather_monitoring/storage/raw_landing.py','sql/005_incremental_ingestion.sql',
           'tests/test_incremental.py','config/workshop3_nws_replay.json','config/workshop3_incremental.json',
           'ingest.py','airflow/dags/incremental_ingestion_dag.py']
    proof={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'tests':results.testsRun,
           'failures':len(results.failures),'errors':len(results.errors),'skipped':len(results.skipped),
           'successful':results.wasSuccessful(),'weather_network':False,
           'fixture_scope':'Synthetic fault scenarios in disposable UUID schemas; never weather evidence.',
           'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper() for p in files}}
    write('incremental_tests.json',proof)
    if not results.wasSuccessful() or results.skipped:raise SystemExit('Tests failed/skipped')
    if args.tests_only:
        return
    with closing(psycopg2.connect(url)) as connection:
        applied=migrate(connection)
        before=status(connection)
        first=replay(connection,ROOT,ROOT/'config/workshop3_nws_replay.json')
        second=replay(connection,ROOT,ROOT/'config/workshop3_nws_replay.json')
        assert all(r['new']==r['changed']==r['rejected']==0 and r['read']==r['unchanged'] for r in second)
        pairs=build_candidates(connection)
        historical=import_historical_context(connection,ROOT)
        after=status(connection)
        with connection.cursor() as c:
            c.execute('SELECT count(*) FROM historical_record')
            historical_count=c.fetchone()[0]
            c.execute("SELECT count(*) FROM integrated_weather_record WHERE record_kind='live'")
            operational_count=c.fetchone()[0]
            c.execute("SELECT source_id,source_key,normalized_fields FROM incremental_record WHERE namespace='replay' ORDER BY source_id,source_key LIMIT 3")
            sample=[{'source':r[0],'source_key':r[1],'fields':r[2]} for r in c.fetchall()]
        write('incremental_replay.json',{'executed_at_utc':datetime.now(timezone.utc).isoformat(),
              'weather_network':False,'applied_migrations':applied,'before':before,'first':first,'second':second,'after':after,
              'historical_records_preserved':historical_count,'operational_nws_records':operational_count,
              'nws_candidate_count':len(pairs),'reused_W1_historical_candidates':historical,
              'limitation':'KOKC snapshots are partial and have no complete-coverage watermark; replay never populates live records.'})
        out=ROOT/'workshop_3/samples/incremental';out.mkdir(parents=True,exist_ok=True)
        (out/'nws_candidates.json').write_text(json.dumps(pairs,indent=2,default=str)+'\n')
        (out/'normalized_preview.json').write_text(json.dumps(sample,indent=2,default=str)+'\n')
    print(json.dumps({'tests':results.testsRun,'first':first,'second':second,'candidates':len(pairs)},default=str))


if __name__=='__main__':main()
