# Workshop 2 pulled foundation review

- **Date:** 2026-11-16, America/Bogota
- **Reviewed revision:** `c2380c9`, including Pablo's `c507a19` foundation and merge `39844db`
- **Reviewer:** coding assistant at Kevin's request; not a personal approval by either student
- **Disposition:** relevant and useful offline foundation; not a completed or validated end-to-end Workshop 2 pipeline

## Reproduced observations

The current review command runs successfully against the real saved captures:

```powershell
.\.venv\Scripts\python.exe scripts/workshop_2/review_offline_captures.py
```

| Capture | Parsed records | Rejected | Distinct keys |
| --- | ---: | ---: | ---: |
| NOAA 2024 saved sample | 250 | 0 | 250 |
| GHCN 2025 station/year | 1,095 measurements | 0 | 1,095 |
| GHCN 2026 six-day overlap | 18 measurements | 0 | 18 |

The total 1,363 is normalized records, not original CSV rows or separate DAG
runs. The three inputs contain 621 CSV rows; wide GHCN rows expand by element.
The JSON is an offline audit, not Silver Parquet or three Airflow outputs.
The inherited Workshop 1 submission manifest still matches all six artifacts;
no approved Workshop 1 PDF, mapping, notebook or sample was changed in this review.

## What is already aligned

- Reusable source parsers under `src/`, separate from landing and a script entry point.
- Native response bodies remain unchanged, with content-addressed paths and hashes.
- NOAA source-local instants use explicit CST-6 conversion; GHCN dates stay dates.
- Nullable coordinate pairs, source IDs, raw parsed fields and GHCN attributes are retained.
- SQL proposes source/capture/run/state/rejection relationships and PostGIS coordinates.
- Current documentation correctly labels SQL unexecuted and the pipeline incomplete.

## Confirmed defects and prerequisite gaps

### R1 - P1: magnitude category is stored as a physical unit

`historical_samples.py:66` uses `MAGNITUDE_TYPE` as `severity_unit`.
The real sample event `1155308` yields value `51.0`, unit `MG`. NOAA defines MG
as a measured gust category; the wind magnitude unit is knots. Keep the category
separately and record/convert the physical unit according to the source mapping.
This must be corrected before database/Parquet normalization is treated as valid.

### R2 - P1: input capture identity is calculated, not checked against the register

`review_offline_captures.py:32-35` reads the file and passes it to landing without
comparing its hash with the expected Workshop 1 registration. A synthetic copy
with one field changed was processed successfully into a new hash, without an
integrity error. This does not mean real samples are corrupt: their registered
hashes match. It means the runner does not enforce that evidence contract.
Check expected bytes/hash before landing/parsing; distinguish trusted captures
from explicitly new source revisions. Narrow the README's verification claim
until implemented.

### R3 - P2: failure cleanup masks the original error on Windows

`raw_landing.py:38-40` attempts to unlink the temporary file while its stream is
still open. Injecting an `os.fsync` failure produced `PermissionError` rather
than the injected I/O exception and left one temporary file. Close the stream
before cleanup and retain the original failure. This was tested with a synthetic
temporary fixture, not with an actual weather capture failure.

### R4 - P2: parser acceptance is not canonical validation

A synthetic `PRCP=-3` row produces an accepted `-3.0 mm` record. There is no
physical-range validator, schema/element-quality policy or stable rejection
taxonomy yet. The parser module describes itself as source-specific preparation,
so this is a missing W2-07 layer, not evidence of negative precipitation in NOAA.
Do not interpret zero parser rejects as complete data-quality validation.

### R5 - raw landing is currently CSV-only and metadata is provisional

The target extension and `raw_format` are hardcoded to CSV (`raw_landing.py:27,53`).
A synthetic gzip body with gzip content type retains its bytes but is labelled
CSV. Explicitly restrict the function to CSV or accept/validate a native format
before adding the annual NOAA gzip adapter. Repeating an identical body reuses
one file, which is good; changing `origin` overwrites its manifest. Capture/run
provenance must be separated from the shared blob. Manifest publication also
needs an atomic strategy before a sensor can use it as a ready signal.

### R6 - SQL is a draft and nullable rejection keys need a decision

The schema was not applied: Docker and psql are not resolved on this session's
PATH. No database acceptance, transaction rollback or SQL idempotency is claimed.
Domain-specific Storm Events/GHCN/station tables and the transactional loader
are absent. An approved model-to-DDL mapping is still needed.

At `001_historical_schema.sql:88`, a nullable `element_code` is part of a UNIQUE
constraint. PostgreSQL 16 permits repeated NULL-containing keys by default;
that constraint alone cannot deduplicate repeated same-run NOAA rejections with
NULL element. Select `NULLS NOT DISTINCT` or an explicit equivalent if same-run
rejection uniqueness is intended, and test it in PostgreSQL. This is a static
documentation-backed finding, not a simulated SQL execution.

## Contrast with professor material checked today

The guide uses Bronze original JSON, Silver PostgreSQL and Gold Parquet. The
current practice uses Airflow 2.10.4/LocalExecutor and PostgreSQL 16. Its ingestion
DAG uses `PythonOperator`, daily intervals and `TriggerDagRunOperator`; curation
uses interval-selected files and a transactional versioned table; analysis writes
weekly Gold Parquet. It contains no TaskFlow decorator or FileSensor.

The standalone Workshop 2 PDF remains the same SHA-256
`48012A30DF3709607717929B5CA0F2C94694B76BAF8669E4321AF9283132AE77` and requests
TaskFlow, a Silver FileSensor and three Bronze/three Silver outputs, with
public-opinion wording. Keep weather-native captures and the canonical DB;
TaskFlow/FileSensor/Parquet compatibility should be explicit in the implementation
decision, not represented as already present in this pull. NLP/scraping does not
become a Group 9 requirement by copying the example.

Observed current source SHA-256 values:

| Academic file | SHA-256 |
| --- | --- |
| Guide Airflow-PostgreSQL-ETL.pdf | `96F53D0088DB3A21A8FB77AF4CA5D13515F3BFA328F8573F49010D4FF041A96E` |
| Practice docker-compose.yml | `16A1BE30F6BC3518C0C424407CBE7F2F43F32DB74EF787DBC53230C9374EFBE2` |
| earthquake_ingestion.py | `119E81C8EDE759F82D86B0A1C022932814E915443F6FD968E7F768E879AF6E0F` |
| earthquake_curation.py | `F209CD8BAA21B645412D11A3B1BFE921B17DFA3EA787CB4248C5F60BE6506ECF` |
| earthquake_analysis.py | `EB6DBA77D9B2112787AD09883EC3C6147274C82E1B5CF74856F6A8A4255F0033` |

## Order to continue

1. Correct R1-R3 and add meaningful fixture/failure tests; establish canonical validation and reason codes (R4).
2. Finalize native-format/capture provenance and schema/domain choices, including NULL rejection keys.
3. Implement the transactional historical/status CLI path and database rerun/rollback tests on saved data.
4. Add Docker/PostGIS/Airflow and thin DAGs using that same application logic.
5. Produce genuine traceable Silver Parquet, the review notebook, successful-run evidence and Workshop 2 PDF/runbook.
6. Expand to bounded station/year historical acquisition with explicit coverage evidence and authorized downloads.

The pull need not be discarded. It is the preparation for the first real vertical
slice; no container, database run, Parquet export or completed Workshop 2 is
established by the current 1,363-record audit. Permanent task ownership stays in
`WORK_BOARD.md`. Findings here were documented, not silently fixed or approved.

## Sources and review boundary

- https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming/practices/airflow_etl
- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/guides/Airflow-PostgreSQL-ETL.pdf
- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf
- https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Bulk-csv-Format.pdf
- https://www.postgresql.org/docs/16/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS

Python probes ran against the existing local environment; invalid values, gzip
payloads, changed captures and injected failures were isolated synthetic fixtures
in temporary directories. They are not source data/results. No weather request,
database run, push or personal teammate approval occurred during this review.
