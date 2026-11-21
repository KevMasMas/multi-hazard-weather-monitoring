"""Record/compare persisted W3 state across an explicitly requested DB restart."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import psycopg2

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['before','after'],required=True)
    phase=parser.parse_args().phase
    connection=psycopg2.connect(os.environ['DATABASE_URL'])
    try:
        with connection.cursor() as c:
            c.execute('SELECT pg_postmaster_start_time()');started=c.fetchone()[0]
            tables={}
            for name,order in [('incremental_state','source_id,namespace,scope'),('incremental_record','record_id'),
                               ('incremental_revision','revision_id'),('event_candidate','candidate_key')]:
                c.execute('SELECT * FROM '+name+' ORDER BY '+order)
                rows=c.fetchall()
                tables[name]={'rows':len(rows),'sha256':hashlib.sha256(json.dumps(rows,default=str,separators=(',',':')).encode()).hexdigest().upper()}
            c.execute('SELECT count(*) FROM historical_record');historical=c.fetchone()[0]
    finally:connection.close()
    path=ROOT/'workshop_3/evidence/incremental_restart.json'
    result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'postgres_started_at_utc':str(started),'tables':tables,'historical_records':historical}
    if phase=='before':proof={'before':result,'weather_network':False}
    else:
        proof=json.loads(path.read_text());proof['after']=result
        assert proof['before']['postgres_started_at_utc']!=result['postgres_started_at_utc']
        assert proof['before']['tables']==tables
        assert proof['before']['historical_records']==historical==19039
        proof['database_restarted']=True;proof['persisted_rows_and_hashes_unchanged']=True
    path.write_text(json.dumps(proof,indent=2)+'\n');print(phase+' restart state recorded/verified')


if __name__=='__main__':main()
