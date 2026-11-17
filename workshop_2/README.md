# Workshop 2 - Technical architecture and historical pipeline

## Submission index

| Moodle item | File / reference |
| --- | --- |
| Technical Architecture and Pipeline Report | [PDF](report/Workshop_2_Report.pdf); [portable LaTeX](report/) |
| Pipeline Output Samples | [ZIP](Workshop_2_Pipeline_Output_Samples.zip); [manifest](samples/manifest.json) |
| GitHub link | [workflow-2](https://github.com/KevMasMas/multi-hazard-weather-monitoring/tree/workflow-2), after Kevin reviews and pushes |

Supporting files: [executed notebook](../notebooks/02_historical_ingestion_review.ipynb),
[demo guide](../deliveries/02-workshop-2/DEMO_GUIDE.md),
[evidence register](EVIDENCE_REGISTER.md), [plan](../deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md)
and [change log](../deliveries/02-workshop-2/CHANGE_LOG.md).
Technical checks do not establish personal approval, commit/push or upload.

## Verified result - November 16, 2026

- Ten real Bronze/Silver batches cover 2021-2025 from both sources; each exact-file
  FileSensor succeeded.
- 13,561 Oklahoma Storm Events + 5,478 GHCN measurements = 19,039 canonical rows.
  One station is represented, not statewide station coverage.
- Historical CLI rerun and three post-restart DAG replays retained unchanged
  records. Zero duplicate business-key groups were found.
- All 29 WSL tests passed without skips, including real database checks.
- Three real JSON/Parquet pairs are packaged with CSV inputs, lineage and hashes.
- The Pandas notebook executed all nine code cells with zero error outputs.
- The report includes Kevin's actual unchanged Airflow screenshot; earlier Silver
  failures are retained and explained.

Current receipts are in `evidence/`: `historical_acquisition.json`,
`historical_airflow_runs.json`, `delivery_database.json`,
`replay_airflow_runs.json`, `after_restart_database.json`,
`wsl_test_results.json` and `notebook_execution.json`.
Earlier pilot receipts remain historical evidence.

## Reproduce the packaged demonstration

From the repository root in Ubuntu WSL, with Docker Desktop running:

```bash
python scripts/workshop_2/restore_sample_inputs.py
docker compose up -d --build --wait airflow-webserver airflow-scheduler airflow-triggerer
python scripts/workshop_2/run_airflow_verification.py \
  OK_2021 USW00013967_2021_full USW00013967_2022_full \
  --receipt workshop_2/evidence/local_demo_runs.json
```

The restore/API runner uses Python's standard library; Docker supplies the
pipeline runtime. Open localhost:8080 with local defaults `airflow`/`airflow`.
Trigger only Bronze. Host PostgreSQL port is **55432**, internal port 5432.

For notebook execution, use Python 3.12 and `requirements-workshop2.in`.
The fresh-kernel notebook reads packaged files and receipts without source/DB
calls. Full acquisition and CLI instructions are in the demo guide and
[WSL setup](../docs/WSL_SETUP.md).

## Scope

Original NOAA gzip responses and NCEI CSVs are cached before transformation.
NOAA inputs are explicitly derived Oklahoma subsets. Bronze JSON is a parsed
view, not an invented original JSON response.

The semester target remains 2010-2025. Additional years, station inventory and
reviewed county assignments remain open. NWS incremental ingestion and Gold/CHI
are later work. The handout's public-opinion conflict remains documented; no
professor clarification or Workshop 2 personal approval is claimed.
