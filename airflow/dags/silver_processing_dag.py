"""Exact-file FileSensor and TaskFlow canonical load/Parquet publication."""
from datetime import datetime, timedelta, timezone
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.sensors.filesystem import FileSensor


@dag(dag_id='weather_silver_processing',schedule=None,start_date=datetime(2026,1,1,tzinfo=timezone.utc),
     catchup=False,max_active_runs=1,default_args={'retries':1,'retry_delay':timedelta(seconds=10)},
     tags=['workshop-2','silver','historical'])
def silver_processing():
    @task
    def validate_manifest_path():
        from multi_hazard_weather_monitoring.historical_pipeline import checked_bronze_path
        return str(checked_bronze_path(get_current_context()['dag_run'].conf['manifest_path']))

    path=validate_manifest_path()
    wait=FileSensor(task_id='wait_for_exact_bronze',fs_conn_id='fs_default',
        filepath="{{ ti.xcom_pull(task_ids='validate_manifest_path') }}",
        mode='reschedule',poke_interval=5,timeout=180)

    @task
    def load_and_export(manifest_path):
        from multi_hazard_weather_monitoring.historical_pipeline import process_bronze
        return process_bronze(manifest_path)

    output=load_and_export(path)
    @task
    def publish_narrative(bronze_path):
        from multi_hazard_weather_monitoring.text_silver import publish_narrative_from_bronze
        return publish_narrative_from_bronze(bronze_path)

    narrative=publish_narrative(path)
    path >> wait >> output
    output >> narrative


silver_processing()
