"""Seal the guide-aligned review package without commit, push or approval claims."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
W3 = ROOT / 'workshop_3'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    for delivery in ('01-workshop-1', '02-workshop-2'):
        manifest = read(ROOT / 'deliveries' / delivery / 'SUBMISSION_MANIFEST.json')
        for name, expected in manifest['artifacts'].items():
            assert sha(ROOT / name) == expected, name

    quality = read(W3 / 'evidence/guide_quality_notebook_execution.json')
    gold_nb = read(W3 / 'evidence/guide_gold_notebook_execution.json')
    for receipt in (quality, gold_nb):
        assert receipt['error_outputs'] == 0
        assert sha(ROOT / 'notebooks' / receipt['notebook']) == receipt['sha256']
    assert (quality['code_cells'], gold_nb['code_cells']) == (8, 6)
    report = W3 / 'Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf'
    qa = read(W3 / 'evidence/report_qa.json')
    assert qa['pages'] == 9 and qa['visual_review_passed'] and sha(report) == qa['pdf_sha256']
    text = read(W3 / 'evidence/text_quality.json')
    tests = read(W3 / 'evidence/guide_tests.json')
    assert tests['workshop3']['passed'] == 8 and tests['workshop3']['skipped'] == 3
    assert tests['workshop2_regression']['passed'] == 21 and tests['workshop2_regression']['skipped'] == 8
    assert text['source_rows'] == text['nonempty_selected_narratives'] == 1324
    reconciliation = read(W3 / 'evidence/guide_gold_reconciliation.json')
    assert reconciliation['gold_rows'] == {'governance': 650, 'storytelling': 607}
    assert reconciliation['text_checks']['text_records'] == 1324
    assert reconciliation['output_hashes_verified'] and reconciliation['unique_gold_keys']
    register = read(W3 / 'evidence/guide_gold_samples.json')
    assert register['kind'] == 'local_pyspark_verified_not_airflow'
    assert register['manifest_sha256'] == reconciliation['manifest_sha256']
    portable_manifest = W3 / 'samples/gold/guide_manifest.json'
    assert sha(portable_manifest) == register['manifest_sha256']
    portable_receipt = read(portable_manifest)
    for output in register['outputs'].values():
        assert sha(ROOT / output['path']) == output['sha256']
    for name, output in register['outputs'].items():
        assert portable_receipt['outputs'][name]['sha256'] == output['sha256']

    sample_zip = W3 / 'Workshop_3_Pipeline_Output_Samples.zip'
    sample_paths = sorted(p for p in (W3 / 'samples').rglob('*') if p.is_file())
    with zipfile.ZipFile(sample_zip, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sample_paths:
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(sample_zip) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(sample_paths)

    artifacts = [report, sample_zip, W3 / 'Workshop_3_Silver_Reproduction_Inputs.zip',
                 ROOT / 'notebooks/03_silver_quality_review.ipynb',
                 ROOT / 'notebooks/04_gold_review.ipynb',
                 *sorted((W3 / 'samples/gold').glob('*.parquet')),
                 *sorted((W3 / 'samples/silver_text').glob('*.parquet'))]
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT,
                                     text=True).strip()
    assert branch == 'feat/workshop-3-guide-alignment'
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    manifest = {
        'prepared_at_utc': datetime.now(timezone.utc).isoformat(),
        'branch': branch,
        'status': 'local_review_ready_approval_and_airflow_rerun_pending',
        'report_pages': qa['pages'],
        'artifacts': {p.relative_to(ROOT).as_posix(): sha(p) for p in artifacts},
        'repository': 'https://github.com/KevMasMas/multi-hazard-weather-monitoring',
        'limitations': ['Revised DAGs have not been rerun in Airflow.',
                        'Narrative evidence is limited to registered NOAA Oklahoma 2021.',
                        'Kevin and Pablo approval, commit, push and Moodle submission are not recorded.'],
    }
    manifest_path = ROOT / 'deliveries/03-workshop-3/SUBMISSION_MANIFEST.json'
    write(manifest_path, manifest)
    audit = {
        'verified_at_utc': datetime.now(timezone.utc).isoformat(),
        'branch': branch, 'prior_delivery_hashes_match': True,
        'report_pages': 9, 'visual_review_passed': True,
        'quality_notebook_cells': 8, 'gold_notebook_cells': 6,
        'gold_rows': reconciliation['gold_rows'],
        'text_rows': 1324, 'sample_zip_entries': len(sample_paths),
        'sample_zip_crc_passed': True, 'git_diff_check_passed': True,
        'current_local_tests': {'workshop3': {k: tests['workshop3'][k] for k in ('total', 'passed', 'skipped', 'failures')},
                                'workshop2': {k: tests['workshop2_regression'][k] for k in ('total', 'passed', 'skipped', 'failures')}},
        'new_airflow_run_verified': False, 'team_approval_recorded': False,
        'artifacts': manifest['artifacts'],
    }
    write(W3 / 'evidence/guide_final_audit.json', audit)

    existing = (W3 / 'EVIDENCE_REGISTER.md').read_text(encoding='utf-8')
    old_paths = re.findall(r'^\| `([^`]+)` \| `[A-F0-9]{64}` \|$', existing, re.M)
    additions = [manifest_path, ROOT / 'WORK_BOARD.md', ROOT / 'PROJECT_CONTEXT.md',
                 ROOT / 'src/multi_hazard_weather_monitoring/text_silver.py',
                 ROOT / 'tests/test_workshop3_text.py',
                 ROOT / 'airflow/dags/bronze_ingestion_dag.py',
                 W3 / 'evidence/guide_final_audit.json',
                 W3 / 'evidence/guide_gold_reconciliation.json',
                 W3 / 'evidence/guide_gold_samples.json',
                 W3 / 'evidence/guide_quality_notebook_execution.json',
                 W3 / 'evidence/guide_gold_notebook_execution.json',
                 W3 / 'evidence/text_quality.json',
                 W3 / 'evidence/guide_tests.json',
                 W3 / 'samples/silver_text/noaa_oklahoma_2021_text.parquet',
                 ROOT / 'scripts/workshop_3/finalize_guide_delivery.py',
                 ROOT / 'scripts/workshop_3/run_guide_tests.py',
                 ROOT / 'docker-compose.yml']
    paths = {ROOT / name for name in old_paths} | set(additions)
    lines = [
        '# Workshop 3 evidence register', '',
        '## Current guide-aligned package (2026-11-21)', '',
        'The supplied Workshop 3 PDF is the selected guide despite its 2026-I cover.',
        'The final local PySpark batch is `w3_guide_alignment_final_20261121`: '
        '650 governance and 607 storytelling rows, including 1,324 real NOAA 2021 '
        'narratives. Other years have no portable narrative evidence.',
        'See `evidence/guide_final_audit.json`, `guide_gold_reconciliation.json`, '
        '`text_quality.json`, `guide_tests.json`, the two guide notebook receipts '
        'and `report_qa.json`.',
        'The earlier 625-row Airflow run remains historical. The revised DAGs have '
        'not been rerun in Airflow; team approval, commit, push and submission are '
        'not recorded. `evidence/final_artifact_audit.json` belongs to that earlier '
        'eight-page revision; `guide_final_audit.json` is the current seal.',
        '', '## Current SHA-256 inventory', '',
        '| Repository path | SHA-256 |', '| --- | --- |',
    ]
    lines += [f'| `{path.relative_to(ROOT).as_posix()}` | `{sha(path)}` |'
              for path in sorted(paths) if path.is_file()]
    (W3 / 'EVIDENCE_REGISTER.md').write_text('\n'.join(lines) + '\n',
                                              encoding='utf-8', newline='\n')
    print(json.dumps({'branch': branch, 'artifacts': len(artifacts),
                      'zip_entries': len(sample_paths), 'pdf_pages': 9}))


if __name__ == '__main__':
    main()
