"""Seal current Gold evidence without changing prior workshop artifacts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import re

ROOT=Path(__file__).resolve().parents[2]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    folder=ROOT/'workshop_3'
    def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
    tests=load(folder/'evidence/spark_tests.json')
    assert tests['successful'] and tests['tests']==8 and not tests['skipped']
    for name,digest in tests['input_sha256'].items():assert sha(ROOT/name)==digest
    regression=load(folder/'evidence/workshop2_regression.json')
    assert regression['successful'] and regression['passed']==29 and not regression['skipped']
    for name,digest in regression['file_sha256'].items():assert sha(ROOT/name)==digest
    run=load(folder/'evidence/gold_airflow_run.json')
    assert run['state']=='success' and all(t['state']=='success' for t in run['tasks'])
    manifest=ROOT/run['manifest_path']
    assert sha(manifest)==run['manifest_sha256']
    batch=load(manifest)
    for name,digest in batch['identity']['inputs'].items():assert sha(ROOT/name)==digest
    assert sha(ROOT/'src/multi_hazard_weather_monitoring/gold.py')==batch['identity']['implementation_sha256']
    sample=load(folder/'evidence/gold_samples.json')
    for item in sample['outputs'].values():assert sha(ROOT/item['path'])==item['sha256']
    for item in batch['outputs'].values():assert sha(ROOT/item['path'])==item['sha256']
    reconciliation=load(folder/'evidence/gold_reconciliation.json')
    assert reconciliation['manifest_sha256']==run['manifest_sha256']
    retry=load(folder/'evidence/gold_retry_verification.json')
    assert retry['manifest_sha256_before']==retry['manifest_sha256_after']==run['manifest_sha256']
    assert retry['output_hashes_unchanged'] and retry['batch_folders_before']==retry['batch_folders_after']
    notebooks=[]
    for notebook,receipt in [('03_silver_quality_review.ipynb','notebook_execution.json'),
                             ('04_gold_review.ipynb','gold_notebook_execution.json')]:
        path=ROOT/'notebooks'/notebook
        execution=load(folder/'evidence'/receipt)
        assert sha(path)==execution['sha256']
        cells=[c for c in load(path)['cells'] if c['cell_type']=='code']
        assert all(c['execution_count'] is not None for c in cells)
        assert not any(o['output_type']=='error' for c in cells for o in c['outputs'])
        notebooks.append(dict(path=path.relative_to(ROOT).as_posix(),code_cells=len(cells),errors=0))
    # W1 immutable submission and W2 submitted data/report/notebook remain preserved.
    preserved=0
    for name in ['01-workshop-1','02-workshop-2']:
        delivery=load(ROOT/'deliveries'/name/'SUBMISSION_MANIFEST.json')
        for path,digest in delivery['artifacts'].items():
            assert sha(ROOT/path)==digest,path
            preserved+=1
    tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    suspicious=[]
    patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    for name in tracked:
        path=ROOT/name
        if not name or not path.is_file():continue
        if path.stat().st_size>50_000_000:suspicious.append(dict(path=name,reason='oversized_review_file'))
        if path.suffix in ['.py','.json','.md','.ipynb','.yml','.yaml','.txt','.in']:
            text=path.read_text(errors='replace')
            if any(re.search(pattern,text) for pattern in patterns):suspicious.append(dict(path=name,reason='recognized_secret_pattern'))
    assert not suspicious,suspicious
    proof=dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),
        spark_tests_passed=tests['tests'],workshop2_regression_passed=regression['passed'],
        gold_dag_run=run['dag_run_id'],counts=batch['counts'],
        gold_output_rows={name:item['rows'] for name,item in batch['outputs'].items()},
        notebooks=notebooks,input_and_output_hashes_verified=True,preserved_prior_delivery_artifacts=preserved,
        committed_batch_retry_unchanged=True,
        reviewed_file_findings=suspicious,secret_scan_scope='Recognized GitHub/AWS/private-key patterns, not an exhaustive guarantee.',
        weather_network=False,commit_or_push=False,
        limits=['This audit covers Gold only; see the current W3 final review for incremental/report status.',
                'No new full dependency environment was installed for notebook execution; fresh kernels used existing environment.'])
    (folder/'evidence/gold_artifact_audit.json').write_text(json.dumps(proof,indent=2)+'\n')
    paths=[ROOT/'notebooks/03_silver_quality_review.ipynb',ROOT/'notebooks/04_gold_review.ipynb',
        ROOT/'src/multi_hazard_weather_monitoring/gold.py',ROOT/'airflow/dags/gold_processing_dag.py',
        ROOT/'config/workshop3_gold.json',*sorted((folder/'evidence').glob('*.json')),
        *sorted((folder/'evidence').glob('*.csv')),*sorted((folder/'samples/gold').glob('*'))]
    lines=['# Workshop 3 evidence register','',
        'This generated register covers Gold only. The complete W3 register is produced by seal_delivery.py. No completed dashboard or forecast is claimed.','',
        '## Current evidence','',
        '- `runtime.json`: actual Java/Python/Airflow/Spark versions and successful pip check.',
        '- `spark_tests.json`: eight tests, including real Spark fixtures; synthetic fixtures are not weather evidence.',
        '- `workshop2_regression.json`: 29 prior tests rerun in the new Docker runtime; original W2 receipt remains untouched.',
        '- `gold_airflow_run.json`: actual successful task/DAG state and committed batch manifest.',
        '- `gold_reconciliation.json`: independent Pandas checks against the same input hashes and monthly groups.',
        '- `gold_samples.json`: unchanged copies of the actual two committed output files.',
        '- `gold_retry_verification.json`: unchanged committed manifest/output hashes and batch count on same-identity replay.',
        '- `gold_airflow_failed_permissions.json` / `gold_permission_error.json`: retained earlier failure state and observed Windows-mount chmod error.',
        '- `notebook_execution.json` and `gold_notebook_execution.json`: fresh-kernel executions, with exact notebook hashes.',
        '- `gold_artifact_audit.json`: final evidence/code/sample preservation checks.','',
        '## Hashes','', '| Repository path | SHA-256 |','| --- | --- |']
    lines.extend('| `'+p.relative_to(ROOT).as_posix()+'` | `'+sha(p)+'` |' for p in paths if p.is_file())
    lines.extend(['','Bulk working directories remain ignored. All 13 reviewed Silver inputs are also available in the small W3 offline reproduction ZIP; restore_silver.py verifies the frozen hashes.','',
        'Git commit/push and personal approval are not inferred. See the current plan/change log and Gold contract for limitations and reproduction.'])
    (folder/'EVIDENCE_REGISTER.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(proof,indent=2))


if __name__=='__main__':main()
