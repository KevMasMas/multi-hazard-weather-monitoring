FROM apache/airflow:2.10.4-python3.12
USER root
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless && apt-get clean && rm -rf /var/lib/apt/lists/*
USER airflow
COPY requirements-workshop2-runtime.txt requirements-workshop2-pipeline.txt requirements-workshop3-runtime.txt /tmp/weather-dependencies/
RUN --mount=type=bind,source=docker/package-cache,target=/tmp/weather-package-cache,readonly \
    if [ -f /tmp/weather-package-cache/pyspark-3.5.7.tar.gz ]; then \
      echo "80e36514e0c5c126d35a26adf4f405cd4a69de96a8ea8a3c1e9a65fce2fb4eaa  /tmp/weather-package-cache/pyspark-3.5.7.tar.gz" | sha256sum --check && \
      pip install --no-cache-dir --no-index --no-deps --no-build-isolation /tmp/weather-package-cache/pyspark-3.5.7.tar.gz; \
    fi && pip install --no-cache-dir "apache-airflow==2.10.4" -r /tmp/weather-dependencies/requirements-workshop3-runtime.txt && pip check
