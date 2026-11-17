"""Run Workshop 2 tests identically from Windows or WSL; no live weather calls."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT)]

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--receipt',type=Path,help='Optional JSON summary; database skips remain explicit.')
    args=parser.parse_args()
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_workshop2*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.receipt:
        files=[*ROOT.glob('tests/test_workshop2*.py'),ROOT/'src/multi_hazard_weather_monitoring/normalization/validation.py',
               *ROOT.glob('src/multi_hazard_weather_monitoring/storage/*.py'),
               *ROOT.glob('src/multi_hazard_weather_monitoring/sources/*.py'),
               ROOT/'src/multi_hazard_weather_monitoring/historical_pipeline.py',
               ROOT/'requirements-workshop2-pipeline.txt',ROOT/'Dockerfile',
               *ROOT.glob('sql/[0-9][0-9][0-9]_*.sql')]
        summary=dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),
                     discovered=result.testsRun,passed=result.testsRun-len(result.skipped)-len(result.errors)-len(result.failures),
                     failures=len(result.failures),errors=len(result.errors),skipped=[str(t) for t,_ in result.skipped],
                     successful=result.wasSuccessful(),weather_network=False,
                     file_sha256={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in files})
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
