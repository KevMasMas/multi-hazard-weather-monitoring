"""Record exact local Workshop 3 and Workshop 2 regression test outcomes."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def run(pattern):
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([str(ROOT / '.venv/Lib/site-packages'),
                                         str(ROOT / 'src')])
    process = subprocess.run([sys.executable, '-m', 'unittest', 'discover',
                              '-s', 'tests', '-p', pattern, '-q'],
                             cwd=ROOT, env=env, text=True, capture_output=True)
    output = process.stdout + process.stderr
    match = re.search(r'Ran (\d+) tests?.*?OK(?: \(skipped=(\d+)\))?', output, re.S)
    if process.returncode or not match:
        raise RuntimeError(output)
    return {'total': int(match.group(1)), 'passed': int(match.group(1)) - int(match.group(2) or 0),
            'skipped': int(match.group(2) or 0), 'failures': 0,
            'output': output.strip()}


def main():
    result = {'verified_at_utc': datetime.now(timezone.utc).isoformat(),
              'workshop3': run('test_workshop3*.py'),
              'workshop2_regression': run('test_workshop2*.py'),
              'runtime_note': 'Native Windows skips Linux Hadoop Spark fixtures and unavailable PostgreSQL integration; separate full local PySpark Gold batch verified.',
              'weather_network': False}
    target = ROOT / 'workshop_3/evidence/guide_tests.json'
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: {x: value[x] for x in ('total', 'passed', 'skipped')}
                      for k, value in result.items() if isinstance(value, dict)}))


if __name__ == '__main__':
    main()
