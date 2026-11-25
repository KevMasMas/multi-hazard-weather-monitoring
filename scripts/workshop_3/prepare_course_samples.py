"""Copy exact outputs of the successful course-aligned Gold run for review."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]


def main():
    evidence=ROOT/'workshop_3/evidence/eda_20261124'
    receipt=json.loads(sorted((evidence/'runtime').glob('gold_*.json'))[-1].read_text(encoding='utf-8'))
    assert receipt['state']=='success'
    path=ROOT/receipt['manifest_path']
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
    assert digest(path)==receipt['manifest_sha256']
    manifest=json.loads(path.read_text(encoding='utf-8'))
    assert manifest['identity']['config']['schema_version']=='weather-gold-v2-course-eda'
    assert digest(ROOT/'src/multi_hazard_weather_monitoring/gold.py')==manifest['identity']['implementation_sha256']
    destination=ROOT/'workshop_3/samples/eda_20261124';destination.mkdir(parents=True,exist_ok=True)
    outputs={}
    for name,item in manifest['outputs'].items():
        original=ROOT/item['path'];assert digest(original)==item['sha256']
        target=destination/original.name
        if target.exists() and digest(target)!=item['sha256']:raise ValueError('Current sample hash conflict')
        shutil.copyfile(original,target)
        outputs[name]={**item,'sample_path':target.relative_to(ROOT).as_posix()}
    (destination/'gold_manifest.json').write_bytes(path.read_bytes())
    register={'dag_run_id':receipt['dag_run_id'],'manifest_path':receipt['manifest_path'],
              'manifest_sha256':receipt['manifest_sha256'],'outputs':outputs}
    (evidence/'gold_samples.json').write_text(json.dumps(register,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v['rows'] for k,v in outputs.items()}))


if __name__=='__main__':main()
