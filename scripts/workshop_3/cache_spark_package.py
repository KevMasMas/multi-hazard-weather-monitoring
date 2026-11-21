"""Optional resumable, hash-verified PyPI cache for a slow build connection."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import time
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[2]

if __name__=='__main__':
    # Immutable release metadata verified against https://pypi.org/pypi/pyspark/3.5.7/json.
    release=dict(filename='pyspark-3.5.7.tar.gz',size=317370347,
        url='https://files.pythonhosted.org/packages/cb/65/2764b1840aa6ea5f7e668a36702c3128ac54d0b861d3d57669b2453469a6/pyspark-3.5.7.tar.gz',
        digests={'sha256':'80e36514e0c5c126d35a26adf4f405cd4a69de96a8ea8a3c1e9a65fce2fb4eaa'})
    folder=ROOT/'data/curated/spark_package_cache';folder.mkdir(parents=True,exist_ok=True)
    size=release['size'];chunk=2*1024*1024
    segments=[(start,min(start+chunk,size)-1) for start in range(0,size,chunk)]
    prefix=folder/'prefix.bin'
    if prefix.exists():
        with prefix.open('rb') as stream:
            for start,end in segments:
                if end>=prefix.stat().st_size:break
                target=folder/f'{start:012d}.part'
                body=stream.read(end-start+1)
                if not target.exists():target.write_bytes(body)
    def download(bounds):
        start,end=bounds;target=folder/f'{start:012d}.part'
        if target.exists() and target.stat().st_size==end-start+1:return target
        for attempt in range(3):
            try:
                request=Request(release['url'],headers={'Range':f'bytes={start}-{end}'})
                with urlopen(request,timeout=90) as response:
                    if response.status!=206 or not response.headers.get('Content-Range','').startswith(f'bytes {start}-{end}/'):
                        raise ValueError('range_response_required')
                    body=response.read(end-start+2)
                if len(body)!=end-start+1:raise ValueError('partial_segment')
                target.write_bytes(body)
                return target
            except Exception:
                if attempt==2:raise
                time.sleep(attempt+1)
    with ThreadPoolExecutor(max_workers=12) as pool:
        pending=[pool.submit(download,bounds) for bounds in segments]
        finished=0
        for task in as_completed(pending):
            task.result();finished+=1
            if finished%5==0:print(f'{finished}/{len(segments)} verified-length segments',flush=True)
    archive=folder/release['filename'];digest=hashlib.sha256()
    with archive.open('wb') as stream:
        for start,end in segments:
            body=(folder/f'{start:012d}.part').read_bytes();digest.update(body);stream.write(body)
    assert archive.stat().st_size==size and digest.hexdigest()==release['digests']['sha256']
    build_cache=ROOT/'docker/package-cache'
    build_cache.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(archive,build_cache/archive.name)
    (folder/'verified.json').write_text(json.dumps({'filename':archive.name,'sha256':digest.hexdigest(),
        'bytes':size,'registry':'https://pypi.org/pypi/pyspark/3.5.7/json'},indent=2)+'\n')
    print('Complete official package verified by SHA-256',flush=True)
