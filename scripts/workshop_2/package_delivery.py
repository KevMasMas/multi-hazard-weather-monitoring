"""Build and verify the actual sample ZIP with hashes of every packaged member."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[2]


def main():
    folder=ROOT/'workshop_2'
    files={p.relative_to(folder).as_posix():p for p in (folder/'samples').rglob('*') if p.is_file()}
    files['notebooks/02_historical_ingestion_review.ipynb']=ROOT/'notebooks/02_historical_ingestion_review.ipynb'
    evidence_names=['historical_acquisition.json','historical_airflow_runs.json',
                    'delivery_database.json','after_restart_database.json','replay_airflow_runs.json',
                    'wsl_test_results.json','notebook_execution.json','report_analysis.json',
                    'user_screenshot.json','compose_ps.json','persistence_verification.json']
    for name in evidence_names:
        p=folder/'evidence'/name
        if not p.exists():
            raise ValueError('required_evidence_missing:'+name)
        files['evidence/'+name]=p
    files['README.md']=folder/'samples/README.md'
    checks={name:dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest().upper(),bytes=path.stat().st_size)
            for name,path in sorted(files.items())}
    manifest=(json.dumps(dict(schema='pipeline-output-package-v1',files=checks),indent=2)+'\n').encode()
    target=folder/'Workshop_2_Pipeline_Output_Samples.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name,path in sorted(files.items()):
            archive.write(path,name)
        archive.writestr('PACKAGE_MANIFEST.json',manifest)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('zip_crc_failure')
        for name,expected in checks.items():
            body=archive.read(name)
            if hashlib.sha256(body).hexdigest().upper()!=expected['sha256'] or len(body)!=expected['bytes']:
                raise ValueError('zip_member_checksum_mismatch')
        bronze=[n for n in archive.namelist() if n.startswith('samples/bronze/') and n.endswith('.json')]
        silver=[n for n in archive.namelist() if n.startswith('samples/silver/') and n.endswith('.parquet')]
        assert len(bronze)==len(silver)==3
    proof=dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),path=target.relative_to(ROOT).as_posix(),
               sha256=hashlib.sha256(target.read_bytes()).hexdigest().upper(),bytes=target.stat().st_size,
               bronze_files=len(bronze),silver_files=len(silver),checked_members=len(checks),crc_and_hashes_passed=True)
    (folder/'evidence/package_verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))


if __name__=='__main__':
    main()
