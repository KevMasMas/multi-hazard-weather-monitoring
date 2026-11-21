"""Weekly reviewed historical Silver-to-Gold snapshot using local PySpark."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context

CONFIG=Path('/opt/weather/config/workshop3_gold.json')
if not CONFIG.exists():
    CONFIG=Path(__file__).resolve().parents[2]/'config/workshop3_gold.json'
GOLD_SCHEDULE=json.loads(CONFIG.read_text())['schedule']

@dag(dag_id='weather_gold_processing',schedule=GOLD_SCHEDULE,
     start_date=datetime(2026,11,16,tzinfo=timezone.utc),catchup=False,max_active_runs=1,
     default_args={'retries':1,'retry_delay':timedelta(seconds=30)},
     tags=['workshop-3','gold','pyspark'])
def gold_processing():
    @task(execution_timeout=timedelta(minutes=20))
    def summarize_silver():
        from multi_hazard_weather_monitoring.gold import build_gold
        context=get_current_context()
        return build_gold(Path('/opt/weather'),context['run_id'],context['logical_date'].isoformat())

    summarize_silver()


gold_processing()
