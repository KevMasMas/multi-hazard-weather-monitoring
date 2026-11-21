"""Hourly NWS ingestion. Remains paused until operational activation is reviewed."""
from datetime import datetime, timedelta, timezone
import os
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context


@dag(dag_id='weather_incremental_ingestion',
     schedule='0 * * * *' if os.environ.get('NWS_POLL_MODE')=='live' else None,
     start_date=datetime(2026,11,21,tzinfo=timezone.utc), catchup=False,
     is_paused_upon_creation=True, max_active_runs=1,
     default_args={'retries':2,'retry_delay':timedelta(seconds=30),
                   'retry_exponential_backoff':True,'max_retry_delay':timedelta(minutes=5)},
     tags=['workshop-3','incremental','nws'])
def incremental_ingestion():
    @task(execution_timeout=timedelta(minutes=15))
    def poll_source(source, scope):
        import os
        from pathlib import Path
        import psycopg2
        from multi_hazard_weather_monitoring.incremental import live, replay
        from multi_hazard_weather_monitoring.storage.migrations import migrate
        from contextlib import closing
        context=get_current_context()
        mode=(context['dag_run'].conf or {}).get('mode') or os.environ.get('NWS_POLL_MODE','disabled')
        with closing(psycopg2.connect(os.environ['DATABASE_URL'])) as connection:
            migrate(connection)
            if mode=='replay':
                # Filter manifest so tasks keep independent source transactions.
                import json
                from tempfile import TemporaryDirectory
                manifest=json.loads(Path('/opt/weather/config/workshop3_nws_replay.json').read_text())
                manifest['polls']=[p for p in manifest['polls'] if p['source']==source]
                with TemporaryDirectory() as directory:
                    path=Path(directory)/'replay.json'
                    path.write_text(json.dumps(manifest))
                    return replay(connection,Path('/opt/weather'),path)
            if mode!='live':
                raise ValueError('Explicit dag_run.conf mode replay or live required; no implicit network calls')
            return live(connection,Path('/opt/weather'),source,scope)

    @task(execution_timeout=timedelta(minutes=5))
    def group_candidates():
        from contextlib import closing
        import psycopg2
        from multi_hazard_weather_monitoring.event_candidates import build_candidates
        context=get_current_context()
        mode=(context['dag_run'].conf or {}).get('mode') or os.environ.get('NWS_POLL_MODE','disabled')
        if mode not in ('replay','live'):
            raise ValueError('Candidate grouping requires an explicit data namespace')
        with closing(psycopg2.connect(os.environ['DATABASE_URL'])) as connection:
            return {'namespace':mode,'candidates':len(build_candidates(connection,mode)),
                    'review_status':'candidate_not_confirmed'}

    alerts=poll_source.override(task_id='poll_alerts')('nws_alerts','OK')
    station=poll_source.override(task_id='poll_station')('nws_station_observations','KOKC')
    [alerts,station] >> group_candidates()


incremental_ingestion()
