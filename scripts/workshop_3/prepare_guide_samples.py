"""Copy a real locally computed guide-aligned Gold pair into reviewable samples."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',required=True)
    args=parser.parse_args()
    manifest=(ROOT/args.manifest).resolve()
    if not manifest.is_relative_to((ROOT/'datalake_gold').resolve()):
        raise ValueError('unexpected_gold_manifest_path')
    receipt=json.loads(manifest.read_text(encoding='utf-8'))
    samples=ROOT/'workshop_3/samples/gold'
    samples.mkdir(parents=True,exist_ok=True)
    record={'kind':'local_pyspark_verified_not_airflow','batch_id':receipt['identity']['batch_id'],
            'manifest_source':manifest.relative_to(ROOT).as_posix(),
            'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest().upper(),
            'outputs':{}}
    shutil.copyfile(manifest,samples/'guide_manifest.json')
    for name,item in receipt['outputs'].items():
        source=(ROOT/item['path']).resolve()
        if not source.is_relative_to((ROOT/'datalake_gold').resolve()):raise ValueError('unexpected_gold_output_path')
        if hashlib.sha256(source.read_bytes()).hexdigest().upper()!=item['sha256']:
            raise ValueError('gold_output_hash_mismatch')
        target=samples/source.name
        shutil.copyfile(source,target)
        record['outputs'][name]={**item,'path':target.relative_to(ROOT).as_posix()}
    proof=ROOT/'workshop_3/evidence/guide_gold_samples.json'
    proof.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'batch_id':record['batch_id'],
                      'rows':{k:v['rows'] for k,v in record['outputs'].items()}}))


if __name__=='__main__':main()
