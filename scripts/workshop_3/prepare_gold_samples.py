"""Copy a real committed Gold pair and manifest; never fabricate sample outputs."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]


def main():
    evidence=ROOT/'workshop_3/evidence'
    run=json.loads((evidence/'gold_airflow_run.json').read_text())
    if run['state']!='success':raise ValueError('successful_gold_dag_required')
    manifest_path=ROOT/run['manifest_path']
    manifest=json.loads(manifest_path.read_text())
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest().upper()!=run['manifest_sha256']:
        raise ValueError('gold_manifest_hash_mismatch')
    samples=ROOT/'workshop_3/samples/gold';samples.mkdir(parents=True,exist_ok=True)
    record=dict(dag_run_id=run['dag_run_id'],manifest_source=run['manifest_path'],outputs={})
    shutil.copyfile(manifest_path,samples/'manifest.json')
    for name,item in manifest['outputs'].items():
        original=ROOT/item['path']
        if hashlib.sha256(original.read_bytes()).hexdigest().upper()!=item['sha256']:
            raise ValueError('gold_sample_checksum_mismatch')
        target=samples/original.name;shutil.copyfile(original,target)
        record['outputs'][name]=dict(path=target.relative_to(ROOT).as_posix(),sha256=item['sha256'],
                                    rows=item['rows'],bytes=target.stat().st_size)
    (evidence/'gold_samples.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
