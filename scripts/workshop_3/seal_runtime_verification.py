"""Publish post-submission runtime evidence without changing delivered files."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'workshop_3/evidence/runtime_20261123'


def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def write(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')


def latest_success(prefix):
    for path in sorted(EVIDENCE.glob(prefix+'_*.json'),reverse=True):
        proof=load(path)
        if prefix=='historical':
            if proof.get('updated_tasks_verified') and all(r[layer]['state']=='success' for r in proof['runs'] for layer in ['bronze','silver']):return path,proof
        elif proof.get('state')=='success' and proof.get('manifest_path'):return path,proof
    raise ValueError('No verified successful '+prefix+' receipt')


def main():
    baseline=load(EVIDENCE/'submitted_artifacts_before.json')
    for name,expected in baseline['sha256'].items():assert sha(ROOT/name)==expected,name
    tests=load(EVIDENCE/'linux_tests.json')
    assert tests['all_passed_without_skips'] and all(s['successful'] and not s['skipped'] for s in tests['suites'].values())
    for name,expected in tests['input_sha256'].items():assert sha(ROOT/name)==expected,name
    historical_path,historical=latest_success('historical')
    gold_path,gold=latest_success('gold')
    manifest_path=ROOT/gold['manifest_path'];manifest=load(manifest_path)
    assert sha(manifest_path)==gold['manifest_sha256']
    sys.path.insert(0,str(ROOT/'src'))
    from multi_hazard_weather_monitoring.gold import verified_inputs,verified_text_inputs
    config=load(ROOT/'config/workshop3_gold.json')
    assert dict(verified_inputs(ROOT,config))==manifest['identity']['inputs']
    assert dict(verified_text_inputs(ROOT,config))==manifest['identity']['text_inputs']
    assert sha(ROOT/'src/multi_hazard_weather_monitoring/gold.py')==manifest['identity']['implementation_sha256']
    reconciliation=load(EVIDENCE/'gold_reconciliation.json')
    assert reconciliation['manifest_sha256']==gold['manifest_sha256']
    before,after=(load(EVIDENCE/(name+'.json')) for name in ['database-before','database-after'])
    assert before['source_counts']==after['source_counts']=={'ghcn_daily':5478,'noaa_storm_events':13561}
    assert before['accepted_records_sha256']==after['accepted_records_sha256']
    assert before['historical_revisions']==after['historical_revisions'] and not after['duplicate_source_keys']
    samples=ROOT/'workshop_3/samples/runtime_20261123';samples.mkdir(parents=True,exist_ok=True)
    outputs={}
    for name,item in manifest['outputs'].items():
        source=ROOT/item['path'];assert sha(source)==item['sha256']
        target=samples/source.name
        if target.exists() and sha(target)!=sha(source):raise ValueError('Existing runtime sample conflict')
        if not target.exists():shutil.copyfile(source,target)
        outputs[name]={**item,'sample_path':target.relative_to(ROOT).as_posix()}
    write(samples/'gold_manifest.json',manifest)
    write(EVIDENCE/'gold_samples.json',{'manifest_path':gold['manifest_path'],
                                      'manifest_sha256':gold['manifest_sha256'],'outputs':outputs})
    # Preserve only small exact native-pipeline receipts, not bulk capture bodies.
    for run in historical['runs']:
        path=ROOT/run['output_manifest']
        target=EVIDENCE/(run['partition']+'_silver_manifest.json')
        if target.exists() and target.read_bytes()!=path.read_bytes():raise ValueError('Runtime receipt conflict')
        if not target.exists():shutil.copyfile(path,target)
    summary={'verified_at_utc':datetime.now(timezone.utc).isoformat(),
             'reference_commit':'6fa48a9','historical_run_receipt':historical_path.relative_to(ROOT).as_posix(),
             'gold_run_receipt':gold_path.relative_to(ROOT).as_posix(),'gold_dag_run':gold['dag_run_id'],
             'all_revised_dags_succeeded':True,'test_counts':{k:v['passed'] for k,v in tests['suites'].items()},
             'total_tests_passed':sum(v['passed'] for v in tests['suites'].values()),'tests_skipped':0,
             'source_counts_preserved':after['source_counts'],'accepted_records_hash_unchanged':True,
             'historical_revisions_unchanged':True,'gold_counts':manifest['counts'],
             'gold_output_rows':{name:item['rows'] for name,item in outputs.items()},
             'gold_manifest_path':gold['manifest_path'],'portable_outputs':outputs,
             'submitted_artifacts_unchanged':baseline['sha256'],
             'weather_network':False,'commit_push_or_personal_approval':False,
             'limits':['650-row Gold now has actual Airflow evidence; the previous 625-row run remains historical.',
                       'Narrative coverage is the recorded 2021 subset; lexical tone is not hazard severity or public opinion.',
                       'W4 dashboard/CHI, county allocation and broader baseline/station coverage are not implemented here.']}
    write(EVIDENCE/'runtime_verification.json',summary)
    paths=[p for p in EVIDENCE.iterdir() if p.is_file() and p.name!='sha256.json']
    paths += [p for p in samples.iterdir() if p.is_file()]
    write(EVIDENCE/'sha256.json',{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)})
    print(json.dumps({'tests_passed':summary['total_tests_passed'],'gold_dag':gold['dag_run_id'],
                      'gold_rows':summary['gold_output_rows'],'submitted_artifacts_unchanged':len(baseline['sha256'])}))


if __name__=='__main__':main()
