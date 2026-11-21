"""Record the actual Java/Python/Spark runtime and dependency consistency."""
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess
import sys
import airflow
import pandas
import pyarrow
import pyspark

ROOT=Path(__file__).resolve().parents[2]

if __name__=='__main__':
    java=subprocess.run(['java','-version'],capture_output=True,text=True,check=True)
    packages=subprocess.run([sys.executable,'-m','pip','check'],capture_output=True,text=True,check=True)
    record=dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
        airflow=airflow.__version__,pyspark=pyspark.__version__,pandas=pandas.__version__,
        pyarrow=pyarrow.__version__,java_version=(java.stdout+java.stderr).strip(),
        pip_check=packages.stdout.strip(),weather_network=False)
    (ROOT/'workshop_3/evidence/runtime.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
