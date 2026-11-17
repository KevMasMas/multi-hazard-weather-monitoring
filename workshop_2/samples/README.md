# Pipeline output samples - Team 9

This package contains three real successful Airflow Bronze/Silver batches:

| Partition | Source | Parquet rows |
| --- | --- | ---: |
| `OK_2021` | NOAA Storm Events, Oklahoma subset | 1,324 |
| `USW00013967_2021_full` | NCEI GHCN-Daily, Oklahoma City | 1,095 |
| `USW00013967_2022_full` | NCEI GHCN-Daily, Oklahoma City | 1,095 |

`bronze/` contains original DAG-produced JSON files, `silver/` contains original
DAG-produced Parquet files, `native/` contains unchanged registered CSV inputs,
and `lineage/` links each output to its actual run/capture. No one batch was copied
to manufacture three runs. `manifest.json` records full SHA-256 hashes and sizes.

NOAA CSV is a documented Oklahoma subset of a preserved nationwide gzip archive,
not the entire original HTTP response. GHCN CSV is the original metric response.
`evidence/historical_acquisition.json` in the ZIP identifies the original URLs,
capture times and native/derived hashes. Full nationwide archives and other bulk
outputs remain in ignored local storage; they are not bundled here.

## Inspect without APIs or a running database

Extract the ZIP and open `notebooks/02_historical_ingestion_review.ipynb`.
It locates `samples/manifest.json`, verifies every file and uses `pd.read_parquet`.
Execute from a fresh Python kernel with Pandas, PyArrow, Matplotlib, nbformat,
nbclient and IPython installed. In the repository, use the Python 3.12 environment
from `requirements-workshop2.in`. Execution also needs the saved JSON receipts
under `evidence/`; these are included in the ZIP.

The notebook displays records, dtypes, nulls, grouped statistics, QC flags and
boxplots. IQR extremes remain in the data. It verifies lineage and reads the full
2021-2025 database audit without connecting to the database.

## Replay the three DAG batches from a clean clone

From the repository root, install its dependencies, then run:

```bash
python scripts/workshop_2/restore_sample_inputs.py
docker compose up -d --build --wait airflow-webserver airflow-scheduler airflow-triggerer
python scripts/workshop_2/run_airflow_verification.py \
  OK_2021 USW00013967_2021_full USW00013967_2022_full \
  --receipt workshop_2/evidence/local_demo_runs.json
```

The restore script validates checksums and copies only packaged CSV inputs into
ignored `data/raw/acquired/`. It makes no source request. New run IDs and Parquet
metadata will differ while canonical source keys and values remain stable.
The default API address is localhost:8080, with the documented local classroom
credentials; use environment overrides for other local settings.

To reproduce all five years, acquisition is an explicit separate operation:
`python scripts/workshop_2/acquire_historical.py --start-year 2021 --end-year 2025`.
This contacts NOAA/NCEI, uses cached responses and records hashes. Later provider
revisions can change responses; never silently replace the submitted evidence.

## Evidence limits

There is one GHCN station; no statewide station coverage is claimed. The full
semester target 2010-2025, county assignments, NWS incremental ingestion and CHI
remain outside this executed slice. Technical checks are not personal approval,
a pushed commit or a platform submission. The current Git branch is `workflow-2`.
