"""Trigger bounded saved partitions via local Airflow and retain real task states."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('partitions', nargs='+')
    parser.add_argument('--receipt', default='workshop_2/evidence/historical_airflow_runs.json')
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args()
    base = os.environ.get('AIRFLOW_API_URL', 'http://localhost:8080/api/v1')
    credentials = (os.environ.get('AIRFLOW_ADMIN_USERNAME', 'airflow') + ':' +
                   os.environ.get('AIRFLOW_ADMIN_PASSWORD', 'airflow')).encode()
    headers = {'Authorization': 'Basic ' + base64.b64encode(credentials).decode(),
               'Content-Type': 'application/json'}

    def api(path, data=None, method=None):
        request = Request(base + path, headers=headers,
                          data=json.dumps(data).encode() if data is not None else None, method=method)
        with urlopen(request, timeout=30) as response:
            return json.load(response)

    for dag in ['weather_bronze_ingestion', 'weather_silver_processing']:
        api('/dags/' + dag, {'is_paused': False}, 'PATCH')
    prefix = 'w2_delivery_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    proof = dict(started_at_utc=datetime.now(timezone.utc).isoformat(), weather_network=False,
                 method='Local Airflow stable REST API; ingestion replays registered captures', runs=[])
    for index, partition in enumerate(args.partitions):
        run_id = f'{prefix}_{index:02d}_{partition}'
        api('/dags/weather_bronze_ingestion/dagRuns', dict(dag_run_id=run_id, conf={'partition': partition}))
        proof['runs'].append(dict(partition=partition, bronze_run_id=run_id, silver_run_id='silver__' + run_id))
    deadline = time.monotonic() + args.timeout
    receipt = ROOT / args.receipt
    while True:
        complete = True
        for run in proof['runs']:
            for layer, dag in [('bronze', 'weather_bronze_ingestion'), ('silver', 'weather_silver_processing')]:
                path = f'/dags/{dag}/dagRuns/' + quote(run[layer + '_run_id'], safe='')
                try:
                    state = api(path)
                    tasks = api(path + '/taskInstances')['task_instances']
                    run[layer] = dict(state=state['state'], start_date=state['start_date'], end_date=state['end_date'],
                                      tasks=[{key: task[key] for key in ['task_id', 'state', 'try_number']} for task in tasks])
                except HTTPError as error:
                    if error.code != 404:
                        raise
                    run[layer] = dict(state='not_created_yet', tasks=[])
                if run[layer]['state'] not in ['success', 'failed']:
                    complete = False
            if run.get('silver', {}).get('state') == 'success' and 'output' not in run:
                path = '/dags/weather_silver_processing/dagRuns/' + quote(run['silver_run_id'], safe='')
                value = api(path + '/taskInstances/load_and_export/xcomEntries/return_value')['value']
                # Airflow's API exposes serialized string values; accept only the expected root.
                if value.startswith('"'):
                    value = json.loads(value)
                relative = Path(value).as_posix().removeprefix('/opt/weather/')
                manifest = ROOT / relative
                if not manifest.resolve().is_relative_to((ROOT / 'data/curated/silver').resolve()):
                    raise ValueError('unexpected_manifest_path')
                run['output'] = json.loads(manifest.read_text())
                run['output_manifest'] = relative
                for field, expected in [(run['output']['bronze_path'], run['output']['bronze_sha256']),
                                        (run['output']['silver']['path'], run['output']['silver']['sha256'])]:
                    if hashlib.sha256((ROOT / field).read_bytes()).hexdigest().upper() != expected.upper():
                        raise ValueError('output_checksum_mismatch')
        proof['verified_at_utc'] = datetime.now(timezone.utc).isoformat()
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps(proof, indent=2) + '\n')
        finished = sum(run.get('silver', {}).get('state') == 'success' for run in proof['runs'])
        print(f'{finished}/{len(proof["runs"])} Silver runs succeeded', flush=True)
        if complete:
            if any(run[layer]['state'] != 'success' for run in proof['runs'] for layer in ['bronze', 'silver']):
                raise SystemExit('At least one real DAG run failed; inspect receipt and Airflow logs.')
            return
        if time.monotonic() >= deadline:
            raise SystemExit('Verification timed out; receipt retains observed states.')
        time.sleep(3)


if __name__ == '__main__':
    main()
