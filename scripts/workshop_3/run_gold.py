"""Run a real Spark Gold snapshot without weather requests."""
import argparse
import logging
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from multi_hazard_weather_monitoring.gold import build_gold


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--batch-id',required=True)
    parser.add_argument('--logical-time',required=True)
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    print(build_gold(ROOT,args.batch_id,args.logical_time))
