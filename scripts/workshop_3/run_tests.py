"""Run Spark fixture tests in the real Docker runtime and record the outcome."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))

if __name__=='__main__':
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_workshop3*.py')
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    paths=[ROOT/'src/multi_hazard_weather_monitoring/gold.py',ROOT/'tests/test_workshop3_gold.py',
           ROOT/'config/workshop3_gold.json',ROOT/'airflow/dags/gold_processing_dag.py']
    record=dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),tests=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        successful=result.wasSuccessful(),fixtures='Synthetic Spark fixtures, not weather evidence.',
        input_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in paths})
    (ROOT/'workshop_3/evidence/spark_tests.json').write_text(json.dumps(record,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
