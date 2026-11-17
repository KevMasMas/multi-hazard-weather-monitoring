FROM apache/airflow:2.10.4-python3.12
COPY requirements-workshop2-runtime.txt requirements-workshop2-pipeline.txt /tmp/weather-dependencies/
RUN pip install --no-cache-dir "apache-airflow==2.10.4" -r /tmp/weather-dependencies/requirements-workshop2-pipeline.txt && pip check
