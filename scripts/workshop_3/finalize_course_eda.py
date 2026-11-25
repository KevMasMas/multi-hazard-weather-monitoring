"""Seal the reopened W3 review package after course-method verification."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
W3=ROOT/'workshop_3'
EVIDENCE=W3/'evidence/eda_20261124'


def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def write(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')


def main():
    archive=W3/'archive/Workshop_3_Pre_EDA_20261124.zip'
    with zipfile.ZipFile(archive) as previous:
        assert previous.testzip() is None
        context=json.loads(previous.read('ARCHIVE_CONTEXT.json'))
        for name,expected in context['artifacts'].items():
            assert hashlib.sha256(previous.read(name)).hexdigest().upper()==expected,name
    for delivery in ['01-workshop-1','02-workshop-2']:
        for name,expected in load(ROOT/'deliveries'/delivery/'SUBMISSION_MANIFEST.json')['artifacts'].items():
            assert sha(ROOT/name)==expected,name
    tests=load(EVIDENCE/'runtime/linux_tests.json')
    assert tests['all_passed_without_skips']
    assert sum(v['passed'] for v in tests['suites'].values())==55
    for name,expected in tests['input_sha256'].items():assert sha(ROOT/name)==expected,name
    notebooks=[]
    for name in ['quality_notebook_execution.json','gold_notebook_execution.json']:
        receipt=load(EVIDENCE/name)
        assert receipt['successful'] and not receipt['error_outputs']
        assert receipt['executed_cells']==receipt['code_cells']
        assert sha(ROOT/receipt['notebook'])==receipt['sha256']
        notebooks.append(receipt)
    review=load(EVIDENCE/'course_eda_review.json')
    assert review['unique_source_records']==19039 and review['station_dates']==1826
    assert sha(W3/'evidence/silver_review.json')==review['frozen_input_register_sha256']
    for name,expected in review['input_sha256'].items():assert sha(ROOT/name)==expected,name
    for profile in review['profiles'].values():assert sha(ROOT/profile['path'])==profile['sha256']
    run=load(sorted((EVIDENCE/'runtime').glob('gold_*.json'))[-1])
    assert run['state']=='success' and all(t['state']=='success' for t in run['tasks'])
    assert all(run['paused_after_verification'].values())
    register=load(EVIDENCE/'gold_samples.json')
    manifest=load(W3/'samples/eda_20261124/gold_manifest.json')
    assert sha(W3/'samples/eda_20261124/gold_manifest.json')==run['manifest_sha256']==register['manifest_sha256']
    assert manifest['identity']['config']['schema_version']=='weather-gold-v2-course-eda'
    assert sha(ROOT/'src/multi_hazard_weather_monitoring/gold.py')==manifest['identity']['implementation_sha256']
    assert sha(ROOT/'config/workshop3_gold.json')==manifest['identity']['config_sha256']
    for field in ['inputs','text_inputs']:
        for name,expected in manifest['identity'][field].items():assert sha(ROOT/name)==expected,name
    for item in register['outputs'].values():assert sha(ROOT/item['sample_path'])==item['sha256']
    reconciliation=load(EVIDENCE/'gold_reconciliation.json')
    assert reconciliation['manifest_sha256']==run['manifest_sha256']
    assert reconciliation['gold_rows']=={'governance':650,'storytelling':607}
    assert reconciliation['text_checks']['text_records']==1324
    governance=pd.read_parquet(ROOT/register['outputs']['governance']['sample_path'])
    assert not governance.metric.isin(['sample_skewness','sample_excess_kurtosis']).any()
    summary=pd.read_csv(EVIDENCE/'distribution_review.csv')
    for row in summary.to_dict(orient='records'):
        selected=governance[(governance.variable==row['element']) & (governance.population==row['population']) & (governance.period=='all')].set_index('metric')
        for metric in ['skewness','excess_kurtosis']:
            np.testing.assert_allclose(selected.loc[metric,'value'],row[metric],rtol=1e-9)
    qa=load(EVIDENCE/'report_qa.json')
    report=W3/'Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf'
    assert sha(report)==qa['pdf_sha256'] and qa['pages']==10 and qa['visual_review_passed']
    assert qa['overfull_tex_boxes']==0
    inventory=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode('utf-8').split('\0')
    findings=[]
    patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    for name in inventory:
        path=ROOT/name
        if not name or not path.is_file():continue
        if path.stat().st_size>50_000_000:findings.append(name)
        if path.suffix in ['.py','.md','.json','.ipynb','.txt','.in','.yml','.yaml']:
            text=path.read_text(encoding='utf-8',errors='replace')
            if any(re.search(pattern,text) for pattern in patterns):findings.append(name)
    assert not findings,findings
    subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,check=True)
    sample_files=[p for p in (W3/'samples/eda_20261124').rglob('*') if p.is_file()]
    sample_files += [p for p in (W3/'samples/silver_text').glob('*') if p.is_file()]
    sample_files += [EVIDENCE/name for name in ['distribution_review.csv','missingness.csv','quality_checks.csv','class_statistics.csv','clipping_experiment.csv','curation_decisions.csv','gold_samples.json']]
    sample_files += list((W3/'profiling').glob('*.html'))
    sample_zip=W3/'Workshop_3_Pipeline_Output_Samples.zip'
    with zipfile.ZipFile(sample_zip,'w',compression=zipfile.ZIP_DEFLATED) as package:
        for path in sorted(set(sample_files)):package.write(path,path.relative_to(ROOT).as_posix())
    source_zip=W3/'Workshop_3_LaTeX_Source.zip'
    with zipfile.ZipFile(source_zip,'w',compression=zipfile.ZIP_DEFLATED) as package:
        for path in sorted((W3/'report').rglob('*')):
            if path.is_file() and path.suffix in ['.tex','.png']:
                package.write(path,path.relative_to(W3/'report').as_posix())
    artifacts=[report,sample_zip,source_zip,W3/'Workshop_3_Silver_Reproduction_Inputs.zip',
               ROOT/'notebooks/03_silver_quality_review.ipynb',ROOT/'notebooks/04_gold_review.ipynb',
               *sorted((W3/'samples/eda_20261124').glob('*.parquet')),*sorted((W3/'profiling').glob('*.html'))]
    artifact_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts}
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()
    manifest_current={'prepared_at_utc':datetime.now(timezone.utc).isoformat(),'branch':branch,
                      'status':'course_aligned_review_ready_not_personally_approved_or_uploaded',
                      'report_pages':10,'artifacts':artifact_hashes,
                      'actual_gold_dag_run':run['dag_run_id'],'gold_contract':'weather-gold-v2-course-eda',
                      'previous_delivery_archive':{'path':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'preserved_artifacts':len(context['artifacts'])},
                      'repository':'https://github.com/KevMasMas/multi-hazard-weather-monitoring',
                      'limits':['2021-only narrative coverage; one GHCN station and 2021-2025 historical slice.',
                                'No W4 dashboard, model training, validated CHI or county crosswalk.',
                                'Final Kevin/Pablo review, commit/push and resubmission remain student actions.']}
    write(ROOT/'deliveries/03-workshop-3/SUBMISSION_MANIFEST.json',manifest_current)
    audit={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'branch':branch,
           'tests_passed':55,'tests_skipped':0,'quality_code_cells':notebooks[0]['code_cells'],
           'gold_code_cells':notebooks[1]['code_cells'],'notebook_errors':0,
           'real_gold_dag_run':run['dag_run_id'],'gold_rows':reconciliation['gold_rows'],
           'profiles_verified':review['profiles'],'report_pages':10,'report_visual_qa_passed':True,
           'class_method_comparison_removed':True,'gold_matches_course_notebook':True,
           'frozen_silver_register_unchanged':True,'prior_delivery_archived':len(context['artifacts']),
           'prior_W1_W2_manifests_match':True,'recognized_secret_findings':findings,
           'secret_scan_scope':'Recognizable GitHub/AWS/private-key patterns; not exhaustive.',
           'git_diff_check_passed':True,'weather_network':False,'commit_push_or_personal_approval':False,
           'artifacts':artifact_hashes}
    write(EVIDENCE/'final_review.json',audit)
    paths=[p for p in EVIDENCE.rglob('*') if p.is_file() and p.name!='sha256.json']
    paths += artifacts+[ROOT/'deliveries/03-workshop-3/SUBMISSION_MANIFEST.json',archive]
    paths += [ROOT/name for name in ['src/multi_hazard_weather_monitoring/gold.py','config/workshop3_gold.json',
        'scripts/workshop_3/create_quality_notebook.py','scripts/workshop_3/course_eda_cells.py',
        'scripts/workshop_3/create_gold_notebook.py','scripts/workshop_3/execute_eda_notebooks.py',
        'requirements-workshop3-eda.in','requirements-workshop3-eda.txt']]
    write(EVIDENCE/'sha256.json',{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))})
    lines=['# Workshop 3 evidence register','','## Current course EDA review - 2026-11-24','',
           'Kevin reopened W3 preparation after the reported extension and selected the instructor\'s methods. Extra estimator comparison is removed; no W4 model/dashboard/CHI is introduced.','',
           '- `evidence/eda_20261124/academic_materials.json`: reviewed instructor commit/URLs/file hashes.',
           '- `evidence/eda_20261124/course_eda_review.json`: real source counts, checks, clipping experiment and HTML profile hashes.',
           '- `evidence/eda_20261124/*notebook_execution.json`: 16/6 executed code cells, zero errors, fresh isolated kernels.',
           '- `evidence/eda_20261124/runtime/`: 55 Linux tests with no skips and the actual successful v2 Gold DAG.',
           '- `evidence/eda_20261124/gold_reconciliation.json`: independent Pandas/SciPy checks against the class method.',
           '- `evidence/eda_20261124/report_qa.json`: current 10-page PDF, rendered and visually reviewed.',
           '- `evidence/eda_20261124/final_review.json` and `sha256.json`: current review/package/source verification.',
           '- `archive/Workshop_3_Pre_EDA_20261124.zip`: 20 previous-delivery artifacts preserved exactly.',
           '- Earlier dated receipts and v1 outputs remain historical; current v2 samples are indexed by `evidence/eda_20261124/gold_samples.json`.','',
           'No new weather query, personal approval, commit/push or resubmission is inferred.','',
           '## Current artifacts','','| Repository path | SHA-256 |','| --- | --- |']
    lines += ['| `'+name+'` | `'+digest+'` |' for name,digest in artifact_hashes.items()]
    (W3/'EVIDENCE_REGISTER.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'report_pages':10,'tests_passed':55,'notebook_cells':[16,6],
                      'gold_rows':reconciliation['gold_rows'],'previous_artifacts_archived':len(context['artifacts']),
                      'review_package_ready':True}))


if __name__=='__main__':main()
