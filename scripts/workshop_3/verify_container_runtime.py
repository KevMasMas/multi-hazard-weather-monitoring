"""Post-submission W3 checks in Linux Docker; never reseals submitted artifacts."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'workshop_3/evidence/runtime_20261123'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT)]


def write(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(value, indent=2, default=str) + '\n', encoding='utf-8', newline='\n')


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['baseline', 'tests', 'runtime','database-before','database-after'], required=True)
    parser.add_argument('--evidence-dir',default='workshop_3/evidence/runtime_20261123')
    args = parser.parse_args()
    EVIDENCE=(ROOT/args.evidence_dir).resolve()
    if not EVIDENCE.is_relative_to((ROOT/'workshop_3/evidence').resolve()):
        raise ValueError('Evidence directory outside Workshop 3')
    if args.mode == 'baseline':
        if (EVIDENCE/'submitted_artifacts_before.json').exists():
            raise ValueError('Preserve the original baseline; do not replace it')
        manifest = ROOT/'deliveries/03-workshop-3/SUBMISSION_MANIFEST.json'
        paths = list(json.loads(manifest.read_text(encoding='utf-8'))['artifacts'])
        paths += ['deliveries/03-workshop-3/SUBMISSION_MANIFEST.json']
        paths += [p.relative_to(ROOT).as_posix() for p in (ROOT/'workshop_3/report').rglob('*')
                  if p.is_file() and p.suffix in ('.tex', '.png')]
        write('submitted_artifacts_before.json', {
            'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
            'reference_commit': '6fa48a9', 'weather_network': False,
            'sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper() for p in sorted(set(paths))}})
        print('Recorded submitted document/package hashes; no artifact changed.')
        return
    if args.mode == 'runtime':
        java = subprocess.run(['java', '-version'], text=True, capture_output=True, check=True)
        pip = subprocess.run([sys.executable, '-m', 'pip', 'check'], text=True, capture_output=True)
        write('container_runtime.json', {
            'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
            'python': platform.python_version(), 'platform': platform.platform(),
            'packages': {p: importlib.metadata.version(p) for p in
                         ['apache-airflow','pyspark','pyarrow','pandas','vaderSentiment','psycopg2-binary']},
            'java': (java.stderr+java.stdout).strip(), 'pip_check': pip.stdout.strip(),
            'pip_check_exit_code': pip.returncode, 'weather_network': False})
        if pip.returncode: raise RuntimeError('Container dependency check failed')
        print('Recorded actual container runtime and successful pip check.')
        return
    if args.mode.startswith('database-'):
        import psycopg2
        from contextlib import closing
        with closing(psycopg2.connect(os.environ['DATABASE_URL'])) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT source_id,count(*) FROM historical_record GROUP BY source_id ORDER BY source_id')
                counts=dict(cursor.fetchall())
                cursor.execute('SELECT count(*) FROM (SELECT source_id,source_key FROM historical_record GROUP BY 1,2 HAVING count(*)>1) d')
                duplicates=cursor.fetchone()[0]
                cursor.execute('SELECT record_id,source_id,source_key,source_content_sha256 FROM historical_record ORDER BY record_id')
                records_sha=hashlib.sha256(json.dumps(cursor.fetchall(),default=str).encode()).hexdigest().upper()
                cursor.execute('SELECT count(*) FROM historical_record_revision')
                revisions=cursor.fetchone()[0]
        write(args.mode+'.json', {'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
                                  'source_counts':counts,'duplicate_source_keys':duplicates,
                                  'accepted_records_sha256':records_sha,'historical_revisions':revisions,
                                  'weather_network':False})
        print(json.dumps({'source_counts':counts,'duplicates':duplicates,'revisions':revisions}))
        return
    os.environ['WORKSHOP2_TEST_DATABASE_URL'] = os.environ['DATABASE_URL']
    result = {}
    for name, pattern in [('workshop3','test_workshop3*.py'),
                          ('postgres_and_historical','test_workshop2*.py'),
                          ('incremental','test_incremental.py')]:
        suite = unittest.defaultTestLoader.discover(str(ROOT/'tests'), pattern=pattern)
        run = unittest.TextTestRunner(verbosity=2).run(suite)
        result[name] = {'total': run.testsRun,
                        'passed': run.testsRun-len(run.failures)-len(run.errors)-len(run.skipped),
                        'failures':len(run.failures), 'errors':len(run.errors),
                        'skipped':[{'test':str(t),'reason':why} for t,why in run.skipped],
                        'successful':run.wasSuccessful()}
        write('linux_tests.json', {'executed_at_utc':datetime.now(timezone.utc).isoformat(),
                                   'weather_network':False,'suites':result,
                                   'fixtures':'Synthetic Spark fixtures and disposable UUID PostGIS schemas; not weather observations.'})
        if not run.wasSuccessful() or run.skipped:
            raise RuntimeError('All Linux tests must pass without skipped cases: '+name)
    paths = [*ROOT.glob('tests/test_*.py'), *ROOT.glob('src/multi_hazard_weather_monitoring/**/*.py'),
             *ROOT.glob('airflow/dags/*.py'), *ROOT.glob('sql/[0-9][0-9][0-9]_*.sql'),
             ROOT/'scripts/workshop_3/verify_gold.py']
    receipt = json.loads((EVIDENCE/'linux_tests.json').read_text())
    receipt['input_sha256'] = {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest().upper()
                              for p in sorted(paths)}
    receipt['all_passed_without_skips'] = True
    write('linux_tests.json', receipt)
    print(json.dumps({name:{k:v for k,v in value.items() if k in ('total','passed','skipped')}
                      for name,value in result.items()}))


if __name__ == '__main__': main()
