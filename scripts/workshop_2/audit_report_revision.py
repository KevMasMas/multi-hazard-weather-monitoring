"""Verify a documentation-only revision without replacing prior run receipts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    folder=ROOT/'workshop_2'
    def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
    sample=load(folder/'samples/manifest.json')
    for path,item in sample['files'].items():assert sha(folder/'samples'/path)==item['sha256']
    assert len({e['bronze_run_id'] for e in sample['entries']})>=3
    assert len({e['silver_run_id'] for e in sample['entries']})>=3
    archive=folder/'Workshop_2_Pipeline_Output_Samples.zip'
    assert sha(archive)==load(folder/'evidence/package_verification.json')['sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        members=load(folder/'samples/manifest.json')
        for path,item in members['files'].items():
            assert hashlib.sha256(z.read('samples/'+path)).hexdigest().upper()==item['sha256']
        bronze=sum(n.startswith('samples/bronze/') and n.endswith('.json') for n in z.namelist())
        silver=sum(n.startswith('samples/silver/') and n.endswith('.parquet') for n in z.namelist())
        assert bronze>=3 and silver>=3
    notebook=ROOT/'notebooks/02_historical_ingestion_review.ipynb'
    assert sha(notebook)==load(folder/'evidence/notebook_execution.json')['sha256']
    nb=load(notebook);cells=[c for c in nb['cells'] if c['cell_type']=='code']
    assert len(cells)==9 and all(c['execution_count'] is not None for c in cells)
    assert not any(o['output_type']=='error' for c in cells for o in c['outputs'])
    tests=load(folder/'evidence/wsl_test_results.json')
    assert tests['successful'] and not tests['skipped']
    for path,digest in tests['file_sha256'].items():assert sha(ROOT/path)==digest
    database=load(folder/'evidence/delivery_database.json')
    assert {s['source_id']:s['records'] for s in database['sources']}=={'ghcn_daily':5478,'noaa_storm_events':13561}
    assert not database['duplicate_business_keys']
    for path,digest in load(ROOT/'deliveries/01-workshop-1/SUBMISSION_MANIFEST.json')['artifacts'].items():
        assert sha(ROOT/path)==digest
    provenance=load(folder/'evidence/layer_excerpt_provenance.json')
    for path,digest in provenance['inputs'].items():assert sha(ROOT/path)==digest
    for name,digest in provenance['fragments'].items():assert sha(folder/'report/assets'/name)==digest
    # The fragment must contain all fields; only documented narrative suffixes may differ.
    entry=next(e for e in sample['entries'] if e['partition']=='OK_2021')
    original=load(folder/'samples'/entry['bronze'])['rows'][:2]
    excerpt=load(folder/'report/assets/bronze_excerpt.json')
    for expected,actual in zip(original,excerpt):
        assert expected.keys()==actual.keys()
        for key,value in expected.items():
            assert actual[key]==(value[:72]+'...' if key in ['EPISODE_NARRATIVE','EVENT_NARRATIVE'] and len(value)>72 else value)
    pdf=folder/'report/Workshop_2_Report.pdf'
    pages=len(PdfReader(pdf).pages)
    log=(folder/'report/main.log').read_text(errors='replace')
    assert 'Overfull' not in log and 'Undefined control sequence' not in log
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    remote=subprocess.check_output(['git','ls-remote','--heads','origin','workflow-2'],cwd=ROOT).decode().split()[0]
    proof=dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),scope='Offline documentation and existing evidence verification; no pipeline runs or weather requests.',
        pdf_pages=pages,notebook_code_cells=len(cells),notebook_error_outputs=0,
        recorded_tests_passed=tests['passed'],tested_file_hashes_unchanged=True,
        sample_json_files=bronze,sample_parquet_files=silver,distinct_real_runs_verified=True,
        sample_zip_unchanged=True,source_samples_and_notebook_unchanged=True,workshop1_artifacts_unchanged=True,
        literal_silver_outputs_reused=True,bronze_only_documented_narrative_suffixes_omitted=True,
        canonical_counts={s['source_id']:s['records'] for s in database['sources']},
        git_head=head,remote_workflow_2=remote,prior_commit_is_pushed=head==remote,
        current_documentation_changes_pushed=False,
        limitations=['No fresh pipeline execution performed for this documentation-only change.',
                     'No new teacher clarification found; existing interpretation retained.',
                     'Full semester years, statewide station inventory and county assignments remain open.'])
    audit=folder/'evidence/report_revision_audit.json'
    audit.write_text(json.dumps(proof,indent=2)+'\n')
    paths=[pdf,folder/'report/main.tex',folder/'report/layer_appendix.tex',
           folder/'report/assets/bronze_excerpt.json',folder/'report/assets/silver_head.txt',
           folder/'report/assets/silver_info.txt',folder/'evidence/layer_excerpt_provenance.json',audit]
    register=folder/'EVIDENCE_REGISTER.md'
    text=register.read_text()
    # Refresh current deliverable hashes; earlier run receipts remain untouched.
    for path in paths:
        relative=path.relative_to(ROOT).as_posix()
        prefix='| `'+relative+'` | `'
        lines=text.splitlines()
        existing=next((i for i,line in enumerate(lines) if line.startswith(prefix)),None)
        row=prefix+sha(path)+'` |'
        if existing is None:
            section=next(i for i,line in enumerate(lines) if line=='## Sample hashes')
            lines.insert(section-1,row)
        else:lines[existing]=row
        text='\n'.join(lines)+'\n'
    if '## Documentation revision' not in text:
        text=text.replace('## Evidence boundaries',
            '## Documentation revision\n\nCurrent PDF: '+str(pages)+' pages, including Appendix A with literal layer excerpts. '
            'The current documentation audit is `evidence/report_revision_audit.json`. Earlier nine-page PDF/package audits remain preserved historical records; pipeline samples, notebook and run results are unchanged. '
            'Git remote `workflow-2` was checked: '+head[:7]+' is pushed; this new documentation revision is local and requires another commit/push.\n\n## Evidence boundaries')
    register.write_text(text)
    manifest_path=ROOT/'deliveries/02-workshop-2/SUBMISSION_MANIFEST.json'
    manifest=load(manifest_path);manifest['base_head']=head
    manifest['artifacts'].update({p.relative_to(ROOT).as_posix():sha(p) for p in [pdf,folder/'report/main.tex',folder/'report/layer_appendix.tex']})
    manifest['selected_submission_commit']=None;manifest['working_tree_changes']=True
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(proof,indent=2))


if __name__=='__main__':main()
