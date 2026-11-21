"""Explicit, bounded NWS validation. Invoke only after announcing weather queries.

Two logical source queries plus their pagination/retries. Raw responses remain
in ignored storage. The second database pass reuses bytes and makes no HTTP call.
"""
from contextlib import closing
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import psycopg2
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from multi_hazard_weather_monitoring.incremental import live,persist_poll,status
from multi_hazard_weather_monitoring.event_candidates import build_candidates
from multi_hazard_weather_monitoring.storage.migrations import migrate


def main():
    proof={'started_at_utc':datetime.now(timezone.utc).isoformat(),'weather_network':True,
           'request_scope':'One active OK alerts query and one bounded KOKC observations query, with pagination/retries.',
           'runs':[],'raw_response_sha256':{}}
    destination=ROOT/'workshop_3/evidence/incremental_live.json'
    samples=ROOT/'workshop_3/samples/incremental';samples.mkdir(parents=True,exist_ok=True)
    try:
        with closing(psycopg2.connect(os.environ['DATABASE_URL'])) as connection:
            migrate(connection)
            for source,scope in [('nws_alerts','OK'),('nws_station_observations','KOKC')]:
                result=live(connection,ROOT,source,scope)
                with connection.cursor() as c:
                    c.execute('SELECT pages FROM incremental_poll WHERE poll_id=%s',(result['poll_id'],))
                    pages=c.fetchone()[0]
                for p in pages:
                    path=ROOT/'data/raw'/p['raw_path'];body=path.read_bytes()
                    assert hashlib.sha256(body).hexdigest()==p['sha256']
                    proof['raw_response_sha256'][path.relative_to(ROOT).as_posix()]=p['sha256'].upper()
                    p['body']=body
                repeated=persist_poll(connection,source,scope,'live',result['queried_at_utc'],pages,True)
                assert repeated['new']==repeated['changed']==0
                proof['runs'].append({'query':result,'unchanged_replay_without_HTTP':repeated,
                                      'pages':[{k:v for k,v in p.items() if k!='body'} for p in pages]})
                # Exact bytes are retained separately. This is explicitly a parsed excerpt.
                excerpt={'evidence_type':'parsed_response_excerpt_not_original_HTTP_body',
                         'source_response_sha256':pages[0]['sha256'],
                         'source_url':pages[0]['origin'],'retrieved_at_utc':pages[0]['retrieved_at_utc'],
                         'features':json.loads(pages[0]['body'].decode('utf-8-sig'))['features'][:2]}
                (samples/(source+'_live_excerpt.json')).write_text(json.dumps(excerpt,indent=2)+'\n')
                destination.write_text(json.dumps(proof,indent=2,default=str)+'\n')
            pairs=build_candidates(connection,'live')
            (samples/'live_nws_candidates.json').write_text(json.dumps(pairs,indent=2,default=str)+'\n')
            proof['candidate_count']=len(pairs)
            proof['status']=status(connection)
            proof['success']=True
    except Exception as exc:
        proof.update(success=False,error=type(exc).__name__+':'+str(exc)[:250])
        raise
    finally:
        proof['finished_at_utc']=datetime.now(timezone.utc).isoformat()
        destination.write_text(json.dumps(proof,indent=2,default=str)+'\n')
    print(json.dumps({'success':proof['success'],'runs':[p['query'] for p in proof['runs']],'candidate_count':proof['candidate_count']},default=str))


if __name__=='__main__':main()
