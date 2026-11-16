# Workshop 2 work in progress

The report PDF, Docker/Airflow run evidence, database load and Silver Parquet
outputs are not available yet. This folder currently contains a bounded,
reproducible offline review of three historical Workshop 1 CSV captures.

From the repository root, run:

```powershell
python scripts/workshop_2/review_offline_captures.py
```

The command verifies three saved capture bodies, lands their unchanged bytes
under the ignored `data/raw/` directory, writes a deterministic JSON manifest
beside each body, parses NOAA and GHCN records, checks duplicate source keys,
and writes `samples/offline_capture_review.json`. The JSON file is an audit
summary, **not** one of the Bronze JSON files or Silver Parquet files requested
by the standalone Workshop 2 handout. It is not an Airflow DAG run. The source
CSV captures remain the evidence and were not changed.

The current implementation and academic limitations are tracked in
`../deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md` and `CHANGE_LOG.md`.
The initial unexecuted PostgreSQL/PostGIS schema is in
`../sql/001_historical_schema.sql`.
