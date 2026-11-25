# Workshop 3 demonstration

## Current 24 November course revision

Use the v2 current index at `workshop_3/README.md`; old dated runs below remain
historical. Restore the saved Silver with `restore_silver.py`, create the separate
EDA environment described in `workshop_3/profiling/README.md`, and execute both
notebooks with `execute_eda_notebooks.py`. No notebook installs packages or calls
weather services. The quality notebook runs 16 code cells; the Gold preview runs 6.

Current exact Parquet samples come from actual successful Airflow run
`w3_runtime_gold_20261125T000455`. Current evidence is under
`workshop_3/evidence/eda_20261124/`; do not run old finalization scripts that target
previous 8/9-page, v1 or Windows-skipped-test packages. Use
`finalize_course_eda.py` only after executing notebooks and verifying the current
PDF/rendered pages. The previous delivery ZIP archive must remain unchanged.

The current PDF source can be edited in `workshop_3/report/main.tex`, or upload
`Workshop_3_LaTeX_Source.zip` to Overleaf. Review the report, notebooks, sample
ZIP and GitHub branch before resubmitting; no final approval/upload is inferred.


## Current guide-aligned offline reproduction

Use the supplied Workshop 3 handout despite its 2026-I cover. From the repository
root, install `requirements-workshop3-runtime.txt` in a suitable Python/Java 17
environment, then run:

```bash
python scripts/workshop_3/restore_silver.py
python scripts/workshop_3/audit_text.py
python scripts/workshop_3/run_gold.py --batch-id your_unique_review_id --logical-time 2026-11-21T17:00:00+00:00
python scripts/workshop_3/verify_gold.py --manifest datalake_gold/ACTUAL_BATCH/manifest.json --receipt workshop_3/evidence/guide_gold_reconciliation.json
```

Replace `ACTUAL_BATCH` with the path printed by `run_gold.py`. Restoration puts
the 13 checked numerical files in `datalake_silver/` and copies the committed
2021 narrative Silver sample into its `text/` subfolder. Gold checks all files
and writes `datalake_gold/`. The verified local batch in this package has 650
governance and 607 storytelling rows. The two executed notebooks are
`notebooks/03_silver_quality_review.ipynb` and `04_gold_review.ipynb`.
`workshop_3/evidence/guide_final_audit.json` and the submission manifest identify
the exact review artifacts. VADER tone is not hazard severity.

The revised Bronze/Silver and Gold DAG code still needs a fresh Airflow run. The
old 625-row Airflow evidence and instructions below refer to the prior revision;
do not treat them as proof that the new DAGs ran. Kevin/Pablo approval and push
remain separate actions after review. Docker Compose now mounts both datalake
folders. It must be rebuilt for the VADER runtime dependency.

Branch: `feat/workshop-3-quality-gold`. Use the actual execution receipts for
verification status; this runbook alone does not establish a successful run.
No commit or push is performed by these commands.

## Review package

The PDF is `workshop_3/Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf`.
Open `workshop_3/report/main.tex` in LaTeX Workshop, or upload that folder's
contents (main, cover and assets) to Overleaf with `main.tex` as root document.
Technical evidence is not Kevin/Pablo approval; record their review separately.

## Incremental replay and status - no weather network

Run from the repository in Ubuntu WSL with the stack already healthy:

```bash
docker compose exec -T airflow-scheduler python /opt/weather/ingest.py \
  --mode incremental --replay config/workshop3_nws_replay.json
docker compose exec -T airflow-scheduler python /opt/weather/ingest.py --mode status
docker compose exec -T airflow-scheduler python /opt/weather/scripts/workshop_3/verify_incremental.py --tests-only
```

Expected saved counts are 238 alerts and 700 KOKC observations. If already loaded,
all are unchanged; do not reset the database to manufacture a first-run demo.
Station pages are partial, so their replay coverage watermark remains absent.
Use host `python scripts/workshop_3/verify_incremental_airflow.py` to trigger a
recorded replay run. It enables the DAG temporarily, sends `{"mode":"replay"}`,
observes source tasks plus grouping and pauses it again. It makes no weather calls.
The disabled-mode scheduled attempt and correction are preserved separately.

The latest successful replay DAG is recorded in
`workshop_3/evidence/incremental_airflow_run.json`; its ID is not hardcoded here.
`incremental_replay.json` preserves the original first and unchanged second passes.
The five replay associations are intra-NWS candidates, not confirmed impacts.

## Live validation and operational activation

The announced validation on 2026-11-21 returned zero active Oklahoma alerts and
903 KOKC observations. Details and page hashes are in `incremental_live.json`.
The repeat database passes reused captured bytes, not additional source queries.
Current responses will differ; these are capture-time facts, not permanent counts.

The following commands make new weather queries; they are not offline reproduction
steps and require the team's source-access instruction and announcement:

```bash
docker compose exec -T airflow-scheduler python /opt/weather/ingest.py \
  --mode incremental --source nws_alerts --scope OK
docker compose exec -T airflow-scheduler python /opt/weather/ingest.py \
  --mode incremental --source nws_station_observations --scope KOKC
```

Configure an identifying `NWS_USER_AGENT` locally in untracked `.env` first.
For an ongoing hourly schedule, also set `NWS_POLL_MODE=live`, recreate the
Airflow webserver/scheduler/triggerer services without deleting volumes, and
explicitly unpause `weather_incremental_ingestion`. Default `disabled` gives
no automatic schedule. The DAG remains paused after our demonstration.
It performs source tasks followed by versioned candidate grouping. Older-than-
seven-day gaps cannot be recovered through the station API and remain flagged.

## Start the runtime in Ubuntu WSL

Docker Desktop must be running with Ubuntu integration enabled.

```bash
cd '/mnt/d/usuarios/Monitores/Desktop/Documentos Kevin/Universidad/Programacion para analisis de datos/Multi-Hazard Weather Impact Monitoring'
docker compose build airflow-scheduler
docker compose up -d --wait airflow-webserver airflow-scheduler airflow-triggerer
docker compose ps
docker compose exec -T airflow-scheduler java -version
docker compose exec -T airflow-scheduler python -c 'import pyspark; print(pyspark.__version__)'
```

The shared image includes Java 17 and PySpark 3.5.7. Rebuilding downloads packages,
not weather data. PostgreSQL remains on the existing volume; do not remove it.
For a slow package connection, the optional
`python scripts/workshop_3/cache_spark_package.py` command downloads/resumes the
official PySpark 3.5.7 source package in segments and verifies its complete
official SHA-256. It caches only software under ignored storage and
`docker/package-cache/`; no package archive is committed. The BuildKit read-only
cache mount avoids retaining the source archive in the final image. With an empty
cache, the normal Docker build obtains PySpark from PyPI instead.

## Input scope

The frozen `workshop_3/evidence/silver_review.json` register identifies the 13
previously reviewed successful Silver exports. They must be present under
`data/curated/silver/` with matching hashes. It is a full 2021-2025 historical
snapshot including replays; the same register drives the quality notebook.
Missing files fail explicitly. A clean clone now includes the small
`workshop_3/Workshop_3_Silver_Reproduction_Inputs.zip` containing all 13 exact
reviewed Silver exports. Before notebooks or Gold, restore them offline:

```bash
python scripts/workshop_3/restore_silver.py
python scripts/workshop_3/restore_silver.py --verify-in-temp
```

Both archive entries and restored bytes are checked against the frozen register.
Different existing files fail instead of being overwritten. No raw weather
download, database reconstruction or API access is needed for Gold reproduction.

## Execute and inspect Gold

Open <http://localhost:8080>, enable `weather_gold_processing`, then trigger it.
It runs one TaskFlow task `summarize_silver` which verifies, consolidates and
publishes governance/storytelling together. Weekly schedule is Monday 06:00 UTC
without catchup. That schedule rebuilds the entire frozen historical snapshot;
it does not fetch sources or filter data to a one-week event window.

For recorded local API verification, run with the host Python environment:

```bash
python scripts/workshop_3/verify_airflow_gold.py
```

The command records actual DAG/task state in
`workshop_3/evidence/guide_gold_airflow_run.json` and prints the committed
manifest path. The earlier `gold_airflow_run.json` stays as historical evidence.
No weather requests are made. For a direct CLI run inside Docker, use your own
explicit batch ID and timezone-aware timestamp:

```bash
docker compose exec -T airflow-scheduler python /opt/weather/scripts/workshop_3/run_gold.py \
  --batch-id manual_review --logical-time 2026-11-20T19:00:00-05:00
```

Reusing exactly the same identity verifies/reuses a committed output. Do not
change its inputs/config/code and expect it to overwrite the earlier batch.
The current revision publishes under ignored `datalake_gold/`, containing
two actual `.parquet` files and `manifest.json`. Do not combine all dated Gold
snapshots to count events; select one successfully committed manifest.

## Verify and preview

```bash
docker compose exec -T airflow-scheduler python /opt/weather/scripts/workshop_3/run_tests.py
python scripts/workshop_3/verify_gold.py --manifest datalake_gold/ACTUAL_BATCH/manifest.json
python scripts/workshop_3/prepare_guide_samples.py --manifest datalake_gold/ACTUAL_BATCH/manifest.json
python scripts/workshop_3/create_gold_notebook.py
python scripts/workshop_2/execute_review_notebook.py \
  --notebook notebooks/04_gold_review.ipynb \
  --receipt workshop_3/evidence/guide_gold_notebook_execution.json
```

Replace the example manifest placeholder with the actual committed path from the
run receipt. The fixture tests are synthetic and isolated in temporary storage;
they are not source observations. Independent Pandas verification checks
deduplication/source totals, sample shape estimators, undefined IQR and monthly
station aggregates against the same unchanged Silver.

For a failed run, inspect the `summarize_silver` task logs first. Missing input,
hash/schema conflicts and undefined statistical scales are distinct conditions:
the first two fail the task, while unavailable statistics are explicitly null
with a status in governance. Do not invent successful output to bypass a failure.

## What to explain

- Governance: source-specific missingness, unique versus repeated snapshots,
  structural checks and method-labelled review rates.
- Storytelling: monthly reported event records and one-station temperatures/rain.
- IQR zero for all-day precipitation means that flag is unavailable, not zero
  outliers and not a reason to delete all rain.
- Sample skewness/excess kurtosis match the notebook convention after correcting
  Spark's population moments. Seasonal and positive-rain groups stay explicit.
- Gold prepares descriptive/diagnostic dashboard inputs; it is not a forecast,
  CHI implementation, statewide station inventory or completed dashboard.

The report and incremental core are now prepared for review. Team approval,
commit/push and submission are recorded only when received. County allocation
and labelled match evaluation remain explicit integration boundaries.
