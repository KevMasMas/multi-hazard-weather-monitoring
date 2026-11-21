"""TaskFlow Bronze capture followed by exact-batch Silver triggering."""
from datetime import datetime, timedelta, timezone
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


@dag(dag_id='weather_bronze_ingestion',schedule=None,start_date=datetime(2026,1,1,tzinfo=timezone.utc),
     catchup=False,max_active_runs=1,default_args={'retries':1,'retry_delay':timedelta(seconds=10)},
     tags=['workshop-2','bronze','historical'])
def bronze_ingestion():
    @task
    def publish_bronze():
        from multi_hazard_weather_monitoring.historical_pipeline import publish_bronze as publish
        context=get_current_context()
        partition=context['dag_run'].conf.get('partition','sample_2024')
        return publish(partition,context['run_id'],context['logical_date'].isoformat())

    ready=publish_bronze()
    @task
    def verify_text_coverage(manifest_path):
        from multi_hazard_weather_monitoring.historical_pipeline import verify_bronze_profile
        return verify_bronze_profile(manifest_path)

    checked=verify_text_coverage(ready)
    trigger=TriggerDagRunOperator(task_id='trigger_silver',trigger_dag_id='weather_silver_processing',
        trigger_run_id='silver__{{ run_id }}',
        conf={'manifest_path':"{{ ti.xcom_pull(task_ids='verify_text_coverage') }}"},
        reset_dag_run=True,wait_for_completion=False)
    checked >> trigger


bronze_ingestion()
