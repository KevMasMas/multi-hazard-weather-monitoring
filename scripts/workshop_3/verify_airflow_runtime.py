"""Run revised W3 DAGs and retain post-submission evidence separately."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import time
from urllib.parse import quote
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT/'workshop_3/evidence/runtime_20261123'


def write(path, value):
    path.write_text(json.dumps(value, indent=2, default=str)+'\n',encoding='utf-8',newline='\n')


def main():
    global EVIDENCE
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage', choices=['historical','gold'],required=True)
    parser.add_argument('--resume', help='Complete evidence for an already successful historical receipt; does not retrigger DAGs')
    parser.add_argument('--evidence-dir',default='workshop_3/evidence/runtime_20261123')
    args=parser.parse_args()
    EVIDENCE=(ROOT/args.evidence_dir).resolve()
    if not EVIDENCE.is_relative_to((ROOT/'workshop_3/evidence').resolve()):raise ValueError('Evidence directory outside Workshop 3')
    credentials=(os.environ.get('AIRFLOW_ADMIN_USERNAME','airflow')+':'+os.environ.get('AIRFLOW_ADMIN_PASSWORD','airflow')).encode()
    headers={'Authorization':'Basic '+base64.b64encode(credentials).decode(),'Content-Type':'application/json'}
    def api(path,data=None,method=None):
        with urlopen(Request('http://localhost:8080/api/v1'+path,headers=headers,
                             data=json.dumps(data).encode() if data is not None else None,method=method),timeout=30) as response:
            return json.load(response)
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    dags=['weather_bronze_ingestion','weather_silver_processing'] if args.stage=='historical' else ['weather_gold_processing']
    initial={dag:api('/dags/'+dag)['is_paused'] for dag in dags}
    path=EVIDENCE/(args.stage+'_'+stamp+'.json')
    if args.resume:
        if args.stage!='historical':raise ValueError('Resume is historical evidence only')
        path=(ROOT/args.resume).resolve()
        if not path.is_relative_to(EVIDENCE.resolve()):raise ValueError('Resume receipt outside runtime evidence')
    try:
        if args.stage=='historical':
            expected={'weather_bronze_ingestion':{'publish_bronze','verify_text_coverage','trigger_silver'},
                      'weather_silver_processing':{'validate_manifest_path','wait_for_exact_bronze','load_and_export','publish_narrative'}}
            for dag,ids in expected.items():
                actual={t['task_id'] for t in api('/dags/'+dag+'/tasks')['tasks']}
                if not ids.issubset(actual):raise ValueError('Updated DAG is not loaded: '+dag)
            if not args.resume:
                sys.argv=['run_airflow_verification.py','OK_2021','USW00013967_2021_full',
                          '--receipt',path.relative_to(ROOT).as_posix(),'--timeout','900']
                runpy.run_path(str(ROOT/'scripts/workshop_2/run_airflow_verification.py'),run_name='__main__')
            proof=json.loads(path.read_text(encoding='utf-8'))
            for run in proof['runs']:
                bronze=ROOT/run['output']['bronze_path']
                payload=json.loads(bronze.read_text(encoding='utf-8'))
                run['bronze_quality_profile']=payload['quality_profile']
                task='/dags/weather_silver_processing/dagRuns/'+quote(run['silver_run_id'],safe='')+'/taskInstances/publish_narrative/xcomEntries/return_value'
                try:
                    value=api(task)['value']
                except HTTPError as error:
                    # A successful GHCN task returns None: Airflow stores no XCom.
                    # That is source-specific non-applicability, not task failure.
                    if error.code!=404 or not run['partition'].startswith('USW'):raise
                    value=None
                if isinstance(value,str):
                    try:value=json.loads(value)
                    except json.JSONDecodeError:pass
                run['narrative_output']=value
                for layer,dag in [('bronze','weather_bronze_ingestion'),('silver','weather_silver_processing')]:
                    assert expected[dag].issubset({t['task_id'] for t in run[layer]['tasks']})
                    assert all(t['state']=='success' for t in run[layer]['tasks'])
            proof['updated_tasks_verified']=True
            proof['weather_network']=False
            write(path,proof)
        else:
            dag='/dags/weather_gold_processing'
            api(dag,{'is_paused':False},'PATCH')
            run_id='w3_runtime_gold_'+stamp
            api(dag+'/dagRuns',{'dag_run_id':run_id})
            run_path=dag+'/dagRuns/'+quote(run_id,safe='')
            deadline=time.monotonic()+1500
            while True:
                run=api(run_path);tasks=api(run_path+'/taskInstances')['task_instances']
                proof={k:run[k] for k in ['dag_id','dag_run_id','state','start_date','end_date']}
                proof['logical_date']=run.get('logical_date') or run.get('execution_date')
                proof['tasks']=[{k:t[k] for k in ['task_id','state','try_number','start_date','end_date']} for t in tasks]
                proof['weather_network']=False
                write(path,proof)
                print('Gold: '+run['state'],flush=True)
                if run['state'] in ('success','failed'):break
                if time.monotonic()>deadline:raise TimeoutError('Gold status timeout; observed evidence retained')
                time.sleep(5)
            if run['state']!='success':raise RuntimeError('Gold DAG failed; inspect retained tasks/logs')
            value=api(run_path+'/taskInstances/summarize_silver/xcomEntries/return_value')['value']
            if value.startswith('"'):value=json.loads(value)
            manifest=(ROOT/value.removeprefix('/opt/weather/')).resolve()
            if not manifest.is_relative_to((ROOT/'datalake_gold').resolve()):raise ValueError('unexpected_gold_manifest_path')
            content=json.loads(manifest.read_text())
            proof.update(manifest_path=manifest.relative_to(ROOT).as_posix(),
                         manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest().upper(),
                         outputs=content['outputs'],counts=content['counts'])
            write(path,proof)
    finally:
        # Leave demonstrated DAGs paused to avoid unintended recurring runs.
        for dag in dags:api('/dags/'+dag,{'is_paused':True},'PATCH')
        if path.exists():
            proof=json.loads(path.read_text(encoding='utf-8'))
            proof['initial_paused_state']=initial
            proof['paused_after_verification']={dag:api('/dags/'+dag)['is_paused'] for dag in dags}
            write(path,proof)
    print('Evidence: '+path.relative_to(ROOT).as_posix())


if __name__=='__main__':main()
