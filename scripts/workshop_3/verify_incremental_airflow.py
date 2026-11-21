"""Observe a manual replay DAG run and pause it again; no NWS HTTP calls."""
import base64
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import time
from urllib.parse import quote
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[2]


def main():
    credentials=(os.environ.get('AIRFLOW_ADMIN_USERNAME','airflow')+':'+os.environ.get('AIRFLOW_ADMIN_PASSWORD','airflow')).encode()
    headers={'Authorization':'Basic '+base64.b64encode(credentials).decode(),'Content-Type':'application/json'}
    def api(path,data=None,method=None):
        with urlopen(Request('http://localhost:8080/api/v1'+path,headers=headers,
                             data=json.dumps(data).encode() if data is not None else None,method=method),timeout=30) as r:
            return json.load(r)
    dag='/dags/weather_incremental_ingestion'
    run_id='w3_nws_replay_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    api(dag,{'is_paused':False},'PATCH')
    try:
        api(dag+'/dagRuns',{'dag_run_id':run_id,'conf':{'mode':'replay'}})
        path=dag+'/dagRuns/'+quote(run_id,safe='')
        deadline=time.monotonic()+600
        while True:
            run=api(path);tasks=api(path+'/taskInstances')['task_instances']
            proof={k:run[k] for k in ('dag_id','dag_run_id','state','start_date','end_date')}
            proof.update(mode='replay',weather_network=False,
                         tasks=[{k:t[k] for k in ('task_id','state','try_number','start_date','end_date')} for t in tasks])
            (ROOT/'workshop_3/evidence/incremental_airflow_run.json').write_text(json.dumps(proof,indent=2)+'\n')
            print(run['state'],flush=True)
            if run['state'] in ('success','failed'):break
            if time.monotonic()>deadline:raise RuntimeError('DAG wait timeout; evidence retained')
            time.sleep(5)
        if run['state']!='success':raise RuntimeError('Replay DAG failed; inspect retained state/logs')
    finally:
        api(dag,{'is_paused':True},'PATCH')
    proof['paused_after_verification']=api(dag)['is_paused']
    (ROOT/'workshop_3/evidence/incremental_airflow_run.json').write_text(json.dumps(proof,indent=2)+'\n')


if __name__=='__main__':main()
