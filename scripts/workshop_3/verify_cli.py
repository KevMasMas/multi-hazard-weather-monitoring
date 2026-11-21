"""Verify the shared CLI and current database without new weather requests."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import psycopg2

ROOT=Path(__file__).resolve().parents[2]


def main():
    commands=[]
    for args in [['--mode','incremental','--replay','config/workshop3_nws_replay.json'],['--mode','status']]:
        run=subprocess.run([sys.executable,str(ROOT/'ingest.py'),*args],capture_output=True,text=True,check=True)
        commands.append({'args':args,'exit_code':run.returncode,'output':json.loads(run.stdout)})
    assert all(p['new']==p['changed']==p['rejected']==0 for p in commands[0]['output']['result'])
    connection=psycopg2.connect(os.environ['DATABASE_URL'])
    try:
        with connection.cursor() as c:
            counts={}
            for table in ('historical_record','incremental_record','incremental_revision','incremental_reject','integrated_weather_record','event_candidate'):
                c.execute('SELECT count(*) FROM '+table) # fixed local identifiers only
                counts[table]=c.fetchone()[0]
            assert counts['historical_record']==19039
            assert counts['integrated_weather_record']==19039+903
            c.execute('SELECT count(*) FROM (SELECT source_id,source_key FROM integrated_weather_record GROUP BY 1,2 HAVING count(*)>1) q')
            assert c.fetchone()[0]==0
            c.execute("SELECT count(*) FROM incremental_state WHERE namespace='live'")
            assert c.fetchone()[0]==2
            c.execute("SELECT count(*) FROM incremental_state WHERE source_id='nws_station_observations' AND namespace='replay'")
            assert c.fetchone()[0]==0
            c.execute("SELECT count(*) FROM event_candidate WHERE review_status!='candidate_not_confirmed'")
            assert c.fetchone()[0]==0
            c.execute('SELECT pages FROM incremental_poll')
            verified={}
            for (pages,) in c.fetchall():
                for page in pages:
                    relative='data/raw/'+page['raw_path']
                    actual=hashlib.sha256((ROOT/relative).read_bytes()).hexdigest().upper()
                    assert actual==page['sha256'].upper()
                    verified[relative]=actual
        proof={'executed_at_utc':datetime.now(timezone.utc).isoformat(),'weather_network':False,
               'cli_commands':commands,'database_counts':counts,
               'integrated_keys_unique':True,'replay_excluded_from_operational_view':True,
               'partial_station_replay_has_no_coverage_watermark':True,
               'no_automatic_candidate_approvals':True,'raw_response_sha256_verified':verified}
        (ROOT/'workshop_3/evidence/incremental_database_audit.json').write_text(json.dumps(proof,indent=2,default=str)+'\n')
    finally:connection.close()
    print(json.dumps(counts))


if __name__=='__main__':main()
