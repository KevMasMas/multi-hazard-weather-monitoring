"""Restore the 13 exact reviewed Silver files, offline and without overwrites."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[2]
ARCHIVE=ROOT/'workshop_3/Workshop_3_Silver_Reproduction_Inputs.zip'


def restore(destination):
    expected=json.loads((ROOT/'workshop_3/evidence/silver_review.json').read_text())['input_sha256']
    with zipfile.ZipFile(ARCHIVE) as archive:
        if set(archive.namelist())!=set(expected):raise ValueError('unexpected_archive_entries')
        bodies={}
        for name,checksum in expected.items():
            if not name.startswith('data/curated/silver/') or '..' in Path(name).parts:
                raise ValueError('unexpected_silver_path')
            body=archive.read(name)
            if hashlib.sha256(body).hexdigest().upper()!=checksum.upper():raise ValueError('archive_hash_mismatch:'+name)
            target=destination/name
            if target.exists() and target.read_bytes()!=body:raise ValueError('existing_silver_differs:'+name)
            bodies[name]=body
    # Verify the whole input set before writing any missing file.
    for name,body in bodies.items():
        target=destination/name
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(body)
        lake=destination/'datalake_silver'/Path(name).name
        if lake.exists() and lake.read_bytes()!=body:raise ValueError('existing_lake_silver_differs:'+name)
        if not lake.exists():
            lake.parent.mkdir(parents=True,exist_ok=True)
            with lake.open('xb') as stream:stream.write(body)
    text_manifest=ROOT/'workshop_3/samples/silver_text/noaa_oklahoma_2021_text.manifest.json'
    if text_manifest.exists():
        text=json.loads(text_manifest.read_text(encoding='utf-8'))
        body=(ROOT/text['path']).read_bytes()
        if hashlib.sha256(body).hexdigest().upper()!=text['sha256']:
            raise ValueError('text_silver_sample_hash_mismatch')
        target=destination/text['lake_path']
        if target.exists() and target.read_bytes()!=body:
            raise ValueError('existing_text_silver_differs')
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(body)
        sidecar=target.with_suffix('.manifest.json')
        if not sidecar.exists():sidecar.write_bytes(text_manifest.read_bytes())
        elif sidecar.read_bytes()!=text_manifest.read_bytes():raise ValueError('text_silver_manifest_differs')
    return len(bodies)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--build-archive',action='store_true')
    parser.add_argument('--verify-in-temp',action='store_true')
    args=parser.parse_args()
    if args.build_archive:
        expected=json.loads((ROOT/'workshop_3/evidence/silver_review.json').read_text())['input_sha256']
        with zipfile.ZipFile(ARCHIVE,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for name,checksum in sorted(expected.items()):
                body=(ROOT/name).read_bytes()
                if hashlib.sha256(body).hexdigest().upper()!=checksum.upper():raise ValueError('source_hash_mismatch')
                info=zipfile.ZipInfo(name,date_time=(2026,11,21,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,body)
        print('Archived 13 existing reviewed Silver exports; no new source data.')
    elif args.verify_in_temp:
        with tempfile.TemporaryDirectory() as directory:
            count=restore(Path(directory))
            assert restore(Path(directory))==count
        print(f'Clean temporary restore and unchanged second restore: {count} files.')
    else:
        print(f'Verified/restored {restore(ROOT)} reviewed Silver files; no network.')


if __name__=='__main__':main()
