# Workshop 2 demonstration

Working branch: `workflow-2`. This guide describes executed functionality;
personal review, commit/push and Moodle upload remain separate actions.

## 1. Start the local stack in Ubuntu WSL

Docker Desktop must show Engine running, with Ubuntu WSL integration enabled.

```bash
cd '/mnt/d/usuarios/Monitores/Desktop/Documentos Kevin/Universidad/Programacion para analisis de datos/Multi-Hazard Weather Impact Monitoring'
docker compose up -d --build --wait airflow-webserver airflow-scheduler airflow-triggerer
docker compose ps
```

Postgres, webserver, scheduler and triggerer should be healthy. Initialization
services normally exit successfully. LocalExecutor runs task subprocesses;
there is no separate Celery worker. Do not delete volumes to fix a login issue.

## 2. Show a genuine run

Open <http://localhost:8080> (local defaults: user/password `airflow`). Enable
both DAGs, trigger only `weather_bronze_ingestion`, and use:

```json
{"partition": "OK_2021"}
```

The Bronze task returns a path, triggers Silver, and its exact-file sensor
precedes canonical load/export. Inspect both DAG states: Bronze success alone
does not prove Silver success. Earlier failed Silver runs are retained and
documented; do not hide them or present them as successes.

From a fresh clone, restore the three packaged CSVs without source requests:

```bash
python scripts/workshop_2/restore_sample_inputs.py
python scripts/workshop_2/run_airflow_verification.py \
  OK_2021 USW00013967_2021_full USW00013967_2022_full \
  --receipt workshop_2/evidence/local_demo_runs.json
```

Run the commands with a Python environment containing the project dependencies.
The API runner itself uses only Python's standard library. Airflow uses its
container dependencies. Never re-run acquisition merely to view saved results.

## 3. Show PostgreSQL in pgAdmin

Use host `127.0.0.1`, port **55432**, database `weather_monitoring`, username
`weather`, and configured local password (default `weather`). Host port 5432
belongs to a separate Windows installation. Internal Compose connections still
use `postgres:5432`.

```sql
SELECT source_id, count(*) FROM historical_record GROUP BY source_id;
SELECT source_id, source_key, count(*) FROM historical_record
GROUP BY source_id, source_key HAVING count(*) > 1;
SELECT source_id, partition_key, rows_read, rows_accepted,
       rows_rejected, rows_unchanged, status
FROM ingestion_run ORDER BY run_id DESC LIMIT 15;
SELECT * FROM rejected_record ORDER BY rejected_id DESC LIMIT 10;
```

Captured counts: 13,561 NOAA + 5,478 GHCN = 19,039 canonical rows and zero duplicate
business-key groups. A fresh three-sample database will contain fewer records;
do not expect the full five-year counts without all acquired inputs.
Zero real rejected rows is compatible with tested quarantine: isolated synthetic
integration fixtures verify that path and are not loaded as weather evidence.

## 4. Show the notebook and deliverables

- `notebooks/02_historical_ingestion_review.ipynb`: execute from the top with a
  fresh kernel; the packaged samples and saved receipts are sufficient.
- `workshop_2/report/Workshop_2_Report.pdf`: English technical report.
- `workshop_2/Workshop_2_Pipeline_Output_Samples.zip`: three real JSON/Parquet
  pairs, original registered CSVs, lineage, manifest, executed notebook and audit.
- `workshop_2/EVIDENCE_REGISTER.md`: evidence scope and hashes.

Explain daily dates versus event instants, wind/hail units, missing point
coordinates, no imputation and why IQR extremes are retained. A daily station
measurement is not a confirmed event match.

## 5. Final submission checks

Kevin and Pablo review the PDF, sample notebook, interpretation and limitations.
Record their actual review; do not inherit Workshop 1 approval. Review `git diff`,
commit on `workflow-2`, push manually and submit the PDF/ZIP/GitHub link. Record
the selected commit and platform receipt after those actions occur.

The 2010-2025 target beyond this 2021-2025 slice, broader station inventory and
reviewed county assignments remain open. NWS incremental work and CHI are later
workshops. No professor clarification is claimed for the handout's domain conflict.
