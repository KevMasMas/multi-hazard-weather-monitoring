"""Seal review artifacts and hashes; never commit, push or infer team approval."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[2]
W3=ROOT/'workshop_3'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def write(path,obj):path.write_text(json.dumps(obj,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')


def main():
    incremental=read(W3/'evidence/incremental_tests.json')
    assert incremental['successful'] and incremental['tests']==12 and not incremental['skipped']
    for name,checksum in incremental['input_sha256'].items():assert sha(ROOT/name)==checksum,name
    gold=read(W3/'evidence/gold_artifact_audit.json')
    regression=read(W3/'evidence/workshop2_regression.json')
    for name,checksum in regression['file_sha256'].items():assert sha(ROOT/name)==checksum,name
    assert gold['spark_tests_passed']==8 and regression['passed']==29
    for name,checksum in read(W3/'evidence/spark_tests.json')['input_sha256'].items():assert sha(ROOT/name)==checksum,name
    run=read(W3/'evidence/incremental_airflow_run.json')
    assert run['state']=='success' and run['paused_after_verification']
    assert {t['task_id'] for t in run['tasks']}=={'poll_alerts','poll_station','group_candidates'}
    assert all(t['state']=='success' for t in run['tasks'])
    live=read(W3/'evidence/incremental_live.json');assert live['success']
    assert [r['query']['read'] for r in live['runs']]==[0,903]
    window=read(W3/'evidence/nws_window_review.json')
    assert (window['within_requested_interval'],window['before_requested_start'],window['after_requested_end'])==(902,1,0)
    db=read(W3/'evidence/incremental_database_audit.json')
    assert db['database_counts']['integrated_weather_record']==19942
    restart=read(W3/'evidence/incremental_restart.json')
    assert restart['database_restarted'] and restart['persisted_rows_and_hashes_unchanged']
    qa=read(W3/'evidence/report_qa.json')
    report=W3/'Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf'
    assert sha(report)==qa['pdf_sha256'] and qa['pages']==8 and qa['visual_review_passed']
    preserved=0
    for delivery in ['01-workshop-1','02-workshop-2']:
        for name,checksum in read(ROOT/'deliveries'/delivery/'SUBMISSION_MANIFEST.json')['artifacts'].items():
            assert sha(ROOT/name)==checksum,name
            preserved+=1
    from restore_silver import restore
    with tempfile.TemporaryDirectory() as directory:
        assert restore(Path(directory))==restore(Path(directory))==13
    # Read-only review inventory includes new untracked files, excludes ignored data/secrets.
    files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode('utf-8').split('\0')
    findings=[]
    patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    for name in files:
        path=ROOT/name
        if not name or not path.is_file():continue
        if name=='.env' or path.stat().st_size>50_000_000:findings.append(name)
        if path.suffix in ('.py','.json','.md','.ipynb','.yml','.yaml','.txt','.in'):
            text=path.read_text(encoding='utf-8',errors='replace')
            if any(re.search(p,text) for p in patterns):findings.append(name)
    assert not findings,findings
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()
    assert branch=='feat/workshop-3-quality-gold'
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True,capture_output=True)
    sample_zip=W3/'Workshop_3_Pipeline_Output_Samples.zip'
    with zipfile.ZipFile(sample_zip,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((W3/'samples').rglob('*')):
            if path.is_file():archive.write(path,path.relative_to(ROOT).as_posix())
    artifacts=[report,sample_zip,W3/'Workshop_3_Silver_Reproduction_Inputs.zip',
               ROOT/'notebooks/03_silver_quality_review.ipynb',ROOT/'notebooks/04_gold_review.ipynb',
               *sorted((W3/'samples/gold').glob('*.parquet'))]
    artifact_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts}
    manifest={'prepared_at_utc':datetime.now(timezone.utc).isoformat(),'branch':branch,
              'status':'technical_review_ready_not_personally_approved_or_submitted',
              'report_pages':qa['pages'],'artifacts':artifact_hashes,
              'repository':'https://github.com/KevMasMas/multi-hazard-weather-monitoring',
              'remote_branch_upload':'Student must commit/push this local branch before supplying its review URL.',
              'limitations':['County allocation and labelled match evaluation pending.',
                             'Professor specification discrepancy and exact class-formula comparison unresolved.',
                             'W3 Kevin/Pablo review, commit/push and submission not recorded.',
                             'Dashboard/CHI and wider baseline/stations remain later work.']}
    manifest_path=ROOT/'deliveries/03-workshop-3/SUBMISSION_MANIFEST.json';write(manifest_path,manifest)
    audit={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'branch':branch,
           'tests_passed':{'spark':8,'incremental':12,'historical_regression':29},
           'total_tests_passed':49,'tests_failed':0,'tests_skipped':0,
           'prior_delivery_artifacts_preserved':preserved,'restored_silver_files_verified':13,
           'clean_temporary_restore_and_repeat_verified':True,'source_fingerprints_verified':True,
           'actual_incremental_dag':run['dag_run_id'],'incremental_dag_left_paused':True,
           'actual_live_validation_recorded':True,'database_restart_state_preserved':True,
           'recognized_secret_findings':findings,'secret_scan_scope':'Recognizable GitHub/AWS/private-key patterns and ignored .env check; not exhaustive.',
           'pdf_pages':qa['pages'],'pdf_visual_review_passed':True,
           'git_diff_check_passed':True,'commit_push_or_approval':False,
           'artifacts':artifact_hashes,'limits':manifest['limitations']}
    write(W3/'evidence/final_artifact_audit.json',audit)
    paths=set(artifacts+[manifest_path])
    for pattern in ['workshop_3/evidence/*.json','workshop_3/evidence/*.csv','workshop_3/samples/**/*',
                    'workshop_3/report/**/*','scripts/workshop_3/*.py','config/workshop3*',
                    'airflow/dags/*processing_dag.py','airflow/dags/incremental_ingestion_dag.py']:
        paths.update(p for p in ROOT.glob(pattern) if p.is_file() and p.suffix not in ('.log','.xdv','.aux','.out') and p.name!='main.pdf')
    paths.update(ROOT/p for p in ['ingest.py','sql/005_incremental_ingestion.sql',
        'src/multi_hazard_weather_monitoring/incremental.py','src/multi_hazard_weather_monitoring/event_candidates.py',
        'src/multi_hazard_weather_monitoring/gold.py','tests/test_incremental.py',
        'workshop_3/INCREMENTAL_CONTRACT.md','workshop_3/GOLD_CONTRACT.md','workshop_3/architecture.mmd'])
    lines=['# Workshop 3 evidence register','',
        'Current scope: verified historical quality/Gold, incremental replay/state/recovery, announced bounded live validation and an eight-page review PDF. No W3 personal approval or platform submission is inferred.','',
        '## Read first','',
        '- `evidence/final_artifact_audit.json`: 49 passing tests across three suites, preserved prior artifacts, current source fingerprints, offline restoration, PDF and review-file scan.',
        '- `evidence/gold_airflow_run.json`, `gold_reconciliation.json`, `gold_retry_verification.json`: actual successful Gold run, independent aggregates and unchanged batch retry.',
        '- `evidence/incremental_replay.json`: original first/unchanged second saved passes; partial KOKC coverage is explicit.',
        '- `evidence/incremental_live.json`: announced real query URLs, UTC times, page hashes and zero/903 source counts; raw original bytes remain ignored.',
        '- `evidence/nws_window_review.json`: 902 observations within the requested interval, one before its start, none after its end. All returned records are preserved; analytics must filter timestamps.',
        '- `evidence/incremental_airflow_run.json`: three actual successful replay tasks, DAG paused afterward.',
        '- `evidence/incremental_restart.json` and `incremental_database_audit.json`: persisted hashes across DB restart, 19,039 preserved historical records and 19,942 unique operational rows.',
        '- `evidence/incremental_disabled_schedule.json` and Gold permission-failure receipts: earlier failures retained with corrections, not silently removed.',
        '- `evidence/report_qa.json`: compiled PDF, eight pages, rendered/visually inspected, no overfull TeX boxes.',
        '- The Silver reproduction ZIP restores all 13 frozen inputs offline. Notebook execution used fresh kernels in the existing environment, not a newly installed dependency environment.','',
        'Five saved-data candidate associations are intra-NWS and unconfirmed. Five W1 NOAA/GHCN wind rows are reused historical context, not new W3 matches. Live validation produced zero candidates. County allocation, labelled match evaluation and professor clarification remain open.','',
        '## SHA-256','', '| Repository path | SHA-256 |','| --- | --- |']
    lines += ['| `'+p.relative_to(ROOT).as_posix()+'` | `'+sha(p)+'` |' for p in sorted(paths) if p.is_file()]
    (W3/'EVIDENCE_REGISTER.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'branch':branch,'tests_passed':49,'pdf_pages':qa['pages'],'preserved_artifacts':preserved,'review_package_ready':True}))


if __name__=='__main__':main()
