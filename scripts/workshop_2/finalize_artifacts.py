"""Verify delivery files, scoped secret patterns and preserved W1 artifacts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import zipfile
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    folder=ROOT/'workshop_2'
    pdf=folder/'report/Workshop_2_Report.pdf'
    notebook=ROOT/'notebooks/02_historical_ingestion_review.ipynb'
    archive=folder/'Workshop_2_Pipeline_Output_Samples.zip'
    reader=PdfReader(pdf)
    text=unicodedata.normalize('NFKC','\n'.join(page.extract_text() or '' for page in reader.pages))
    for required in ['Executive summary','Technical architecture','Preprocessing','Docker stack',
                     'DAG implementation','Results and verification','Challenges','References']:
        if required.lower() not in text.lower():
            raise ValueError('missing_report_section:'+required)
    nb=json.loads(notebook.read_text())
    cells=[c for c in nb['cells'] if c['cell_type']=='code']
    if any(c['execution_count'] is None or any(o['output_type']=='error' for o in c['outputs']) for c in cells):
        raise ValueError('notebook_not_cleanly_executed')
    execution=json.loads((folder/'evidence/notebook_execution.json').read_text())
    if execution['sha256']!=sha(notebook):
        raise ValueError('notebook_receipt_hash_mismatch')
    tests=json.loads((folder/'evidence/wsl_test_results.json').read_text())
    if not tests['successful'] or tests['skipped']:
        raise ValueError('tests_not_complete')
    for path,digest in tests['file_sha256'].items():
        if sha(ROOT/path)!=digest:
            raise ValueError('test_receipt_stale:'+path)
    sample=json.loads((folder/'samples/manifest.json').read_text())
    for path,expected in sample['files'].items():
        if sha(folder/'samples'/path)!=expected['sha256']:
            raise ValueError('sample_hash_mismatch:'+path)
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None:
            raise ValueError('zip_corrupt')
        packaged=json.loads(package.read('PACKAGE_MANIFEST.json'))
        for path,expected in packaged['files'].items():
            if hashlib.sha256(package.read(path)).hexdigest().upper()!=expected['sha256']:
                raise ValueError('zip_member_mismatch:'+path)
        if package.read('notebooks/02_historical_ingestion_review.ipynb')!=notebook.read_bytes():
            raise ValueError('packaged_notebook_stale')
    w1=json.loads((ROOT/'deliveries/01-workshop-1/SUBMISSION_MANIFEST.json').read_text())
    for path,digest in w1['artifacts'].items():
        if sha(ROOT/path)!=digest:
            raise ValueError('workshop1_artifact_changed:'+path)
    screenshot=json.loads((folder/'evidence/user_screenshot.json').read_text(encoding='utf-8-sig'))
    if sha(ROOT/screenshot['path'])!=screenshot['sha256']:
        raise ValueError('screenshot_changed')
    files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    patterns={'github_token':r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}',
              'aws_access_key':r'AKIA[0-9A-Z]{16}',
              'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'}
    findings=[]; scanned=0
    for name in files:
        path=ROOT/name
        if not name or not path.is_file() or path.suffix.lower() not in ['.py','.md','.json','.ipynb','.tex','.yaml','.yml','.txt','.sql','.in','.lock']:
            continue
        body=path.read_text(encoding='utf-8',errors='replace');scanned+=1
        for label,pattern in patterns.items():
            if re.search(pattern,body):findings.append(dict(path=name,pattern=label))
    if findings:
        raise ValueError('potential_secret_patterns_found:'+str(findings))
    if subprocess.check_output(['git','ls-files','.env'],cwd=ROOT).strip():
        raise ValueError('env_file_is_tracked')
    oversized=[name for name in files if name and (ROOT/name).is_file() and (ROOT/name).stat().st_size>50_000_000]
    if oversized:raise ValueError('oversized_review_files:'+str(oversized))
    proof=dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),pdf_pages=len(reader.pages),
        notebook_code_cells=len(cells),notebook_error_outputs=0,sample_pairs=len(sample['entries']),
        tests_passed=tests['passed'],test_receipt_fingerprints_verified=True,
        workshop1_artifacts_unchanged=len(w1['artifacts']),zip_crc_and_hashes_passed=True,
        screenshot_unchanged=True,secret_scan=dict(files=scanned,patterns=list(patterns),findings=findings,
        limitation='Scoped recognized-token/private-key pattern scan, not a guarantee that all possible secrets are absent.'),
        oversized_files=oversized,personal_approval='Not recorded for Workshop 2',push_or_upload=False)
    (folder/'evidence/final_artifact_audit.json').write_text(json.dumps(proof,indent=2)+'\n')
    artifacts=[pdf,archive,notebook,folder/'samples/manifest.json',folder/'report/main.tex']
    delivery=dict(purpose='Prepared local review artifacts, not approval or upload evidence.',
        branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip(),
        base_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
        selected_submission_commit=None,working_tree_changes=True,
        artifacts={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts})
    (ROOT/'deliveries/02-workshop-2/SUBMISSION_MANIFEST.json').write_text(json.dumps(delivery,indent=2)+'\n')
    references=[*artifacts,*sorted((folder/'evidence').glob('*.json'))]
    lines=['# Workshop 2 evidence register','',
        'Current executed slice: 2021-2025; Oklahoma Storm Events and one GHCN station.',
        'Personal approval, selected commit, push and platform upload are not inferred.','',
        '## Evidence boundaries','',
        '- `historical_acquisition.json`: original NOAA gzip/NCEI CSV responses, request URLs, UTC captures, native/input SHA-256 and subset derivation.',
        '- `historical_airflow_runs.json`: ten actual successful source/year DAG pairs, real tasks and output metrics.',
        '- `delivery_database.json`: 19,039 canonical rows, zero duplicate keys and five-year/date coverage.',
        '- `after_restart_database.json`, `persistence_verification.json`, `replay_airflow_runs.json`: persisted state and three successful unchanged replays.',
        '- `wsl_test_results.json`: current 29-test receipt and tested-file hashes; synthetic integration fixtures remain separate from weather evidence.',
        '- `notebook_execution.json`: fresh kernel in the existing Python environment, not a newly installed isolated environment.',
        '- `user_screenshot.json`: contributor-supplied unchanged UI overview; earlier failures remain visible.',
        '- `package_verification.json` / `final_artifact_audit.json`: actual ZIP/hash/receipt/W1-preservation checks.',
        '- Earlier `airflow_verification.json` / `database_verification.json` are historical bounded-pilot receipts, not the current five-year totals.','',
        'Full original archives/bulk outputs stay in ignored storage. Three reviewable registered CSV inputs, original DAG JSON/Parquet and lineage manifests are packaged. The NOAA CSV is a documented subset, not an original nationwide response.','',
        '## Artifact and receipt hashes','', '| Repository path | SHA-256 |','| --- | --- |']
    lines.extend('| `'+p.relative_to(ROOT).as_posix()+'` | `'+sha(p)+'` |' for p in references)
    lines.extend(['','## Sample hashes','', 'Full per-file hashes and sizes: `samples/manifest.json`. ZIP members are independently indexed by `PACKAGE_MANIFEST.json` inside the archive.','',
        '## Open items','', 'Remaining semester years (2010-2020), broader station inventory and reviewed county assignments remain open. Professor clarification of the conflicting source-domain wording is unrecorded. Kevin and Pablo must review and select the submission commit, then perform push/upload.'])
    (folder/'EVIDENCE_REGISTER.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(proof,indent=2))


if __name__=='__main__':
    main()
