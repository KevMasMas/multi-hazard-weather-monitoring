"""Execute and observe one local Gold DAG run; retain actual task/API evidence."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-id',default='w3_gold_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
    args=parser.parse_args()
    credentials=(os.environ.get('AIRFLOW_ADMIN_USERNAME','airflow')+':'+os.environ.get('AIRFLOW_ADMIN_PASSWORD','airflow')).encode()
    headers={'Authorization':'Basic '+base64.b64encode(credentials).decode(),'Content-Type':'application/json'}
    def api(path,data=None,method=None):
        url='http://localhost:8080/api/v1'+path
        with urlopen(Request(url,headers=headers,data=json.dumps(data).encode() if data is not None else None,method=method),timeout=30) as r:
            return json.load(r)
    dag='/dags/weather_gold_processing'
    api(dag,{'is_paused':False},'PATCH')
    api(dag+'/dagRuns',{'dag_run_id':args.run_id})
    path=dag+'/dagRuns/'+quote(args.run_id,safe='')
    deadline=time.monotonic()+1200
    while True:
        run=api(path)
        tasks=api(path+'/taskInstances')['task_instances']
        proof={k:run[k] for k in ['dag_id','dag_run_id','state','start_date','end_date']}
        proof['logical_date']=run.get('logical_date') or run.get('execution_date')
        proof['tasks']=[{k:t[k] for k in ['task_id','state','try_number','start_date','end_date']} for t in tasks]
        proof['weather_network']=False
        (ROOT/'workshop_3/evidence/gold_airflow_run.json').write_text(json.dumps(proof,indent=2)+'\n')
        print(run['state'],flush=True)
        if run['state']=='success':
            value=api(path+'/taskInstances/summarize_silver/xcomEntries/return_value')['value']
            if value.startswith('"'):value=json.loads(value)
            relative=value.removeprefix('/opt/weather/')
            manifest=(ROOT/relative).resolve()
            if not manifest.is_relative_to((ROOT/'data/gold').resolve()):raise ValueError('unexpected_gold_path')
            proof['manifest_path']=relative
            proof['manifest_sha256']=hashlib.sha256(manifest.read_bytes()).hexdigest().upper()
            proof['outputs']=json.loads(manifest.read_text())['outputs']
            (ROOT/'workshop_3/evidence/gold_airflow_run.json').write_text(json.dumps(proof,indent=2)+'\n')
            print('Manifest: '+relative)
            return
        if run['state']=='failed':raise SystemExit('Gold DAG failed; inspect task log.')
        if time.monotonic()>deadline:raise SystemExit('Gold DAG timeout; actual states saved.')
        time.sleep(5)


if __name__=='__main__':main()
