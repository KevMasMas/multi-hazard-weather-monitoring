"""Export one successful database run; no network weather access or DAG claim."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from ingest import _connect
from multi_hazard_weather_monitoring.storage.silver_export import export_run

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-id',required=True,type=int)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    with closing(_connect()) as connection:
        print(json.dumps(export_run(connection,args.run_id,args.output)))
