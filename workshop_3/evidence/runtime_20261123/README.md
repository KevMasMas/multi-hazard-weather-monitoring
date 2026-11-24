# Updated Docker/Airflow verification - 2026-11-23

Local date: 23 November 2026, America/Bogota. Receipts use UTC, so the actual
execution IDs/timestamps are dated 24 November UTC. Reference pulled commit:
`6fa48a9`, on `feat/workshop-3-quality-gold`.

Kevin reported that the Workshop 3 document had already been submitted and
requested completing runtime verification for the Workshop 4 handoff. The PDF,
LaTeX/assets, notebooks, submitted ZIPs, samples and submission manifest were
not regenerated. All **20 baseline artifact hashes match** after verification.
No new personal approval, commit, push or platform upload was performed.

## Result

| Check | Observed result | Evidence |
| --- | --- | --- |
| Revised Bronze | NOAA `OK_2021` and GHCN `USW00013967_2021_full` succeeded, including `verify_text_coverage` | `historical_20261124T003243.json` |
| Revised Silver | Both source runs succeeded, including FileSensor/load and `publish_narrative` | Same receipt and source Silver manifests |
| Narrative output | 1,324 nonempty NOAA narratives: 632 event text / 692 episode fallback; GHCN text is not applicable | Narrative task XCom, text sidecar, independent reconciliation |
| Historical replay | NOAA 1,324 and GHCN 1,095 measurements unchanged; zero accepted/rejected new records | Source run metrics |
| Revised Gold | Manual DAG run `w3_runtime_gold_20261124T003408` succeeded, first attempt | `gold_20261124T003408.json` |
| Actual outputs | **650 governance / 607 storytelling rows** from 15 numeric Silver files and 2 text exports | Actual manifest and `gold_samples.json` |
| Numeric population | 24,972 snapshot rows -> 19,039 unique source records; 5,933 repeated snapshot rows | Gold manifest and independent Pandas comparison |
| Text population | 2,648 text snapshot rows -> 1,324 unique NOAA narratives | `gold_reconciliation.json` |
| Independent checks | 40 shape statistics, 180 station/month groups, 427 event groups; text/tone totals and 85 text-bearing story groups reconcile | `gold_reconciliation.json` |
| Linux tests | **54 passed, zero errors/failures/skips**: 13 W3, 29 historical/PostgreSQL, 12 incremental | `linux_tests.json` |
| Database preservation | 13,561 NOAA + 5,478 GHCN records; identical accepted-record hash and revision count; zero duplicate keys | `database-before.json` / `database-after.json` |
| Task logs | 15 actual task logs archived; four application DAGs left paused | `task_logs_index.json` and `task_log_*.json` |

The three Spark fixtures and eight PostGIS integration cases previously skipped
on Windows actually ran in the Linux stack. The W3 suite also includes two new
regression tests for repeated/conflicting text snapshots, hence 54 total tests
rather than the previous 52.

## Correction found during review

The Gold transformation already reconciled repeated narrative exports. Its
independent Pandas verifier assumed text keys never repeated across exports,
which stopped being valid after the new Silver task produced a second genuine
text snapshot. `verify_gold.py` now rejects conflicting same-key narrative content
and deterministically selects identical copies before comparing totals. Tests
cover both cases. No source narrative, Gold transformation or submitted artifact
was changed to manufacture agreement.

The first evidence collector also encountered the legitimate absence of a
GHCN narrative XCom: a successful non-applicable task returns `None`. This was
handled explicitly and the existing successful DAG receipt was completed using
`--resume`; no duplicate DAG run was needed to repair its evidence collection.

## Runtime and recovery

The existing Docker `sailor-ingest.sock` startup error was resolved by Kevin
closing/reopening Docker Desktop from Windows, preserving the socket and volumes.
The image was rebuilt with the pulled dependency contract. Actual runtime:
Airflow 2.10.4, PySpark 3.5.7, Java 17, VADER 3.3.2, Python 3.12.8,
Pandas 2.1.4, PyArrow 18.1.0 and psycopg2-binary 2.9.11; `pip check` passed.

Unpausing Gold also allowed its due weekly scheduled run to complete. The manual
verification then ran successfully. Both observed statuses are retained in
`task_logs_index.json`; the old 625-row receipt and earlier inconclusive receipt
remain historical and were not overwritten. The stack was left healthy and all
four application DAGs paused, with NWS live polling disabled.

To reproduce with the saved inputs, follow the main W3 demo guide and use:

```bash
python scripts/workshop_3/restore_silver.py
# Ubuntu WSL, Docker Desktop running:
docker compose build airflow-scheduler
docker compose up -d --wait airflow-webserver airflow-scheduler airflow-triggerer
docker compose exec -T airflow-scheduler python /opt/weather/scripts/workshop_3/verify_container_runtime.py --mode tests
# Host Python environment:
python scripts/workshop_3/verify_airflow_runtime.py --stage historical
python scripts/workshop_3/verify_airflow_runtime.py --stage gold
```

The initial baseline is intentionally not overwritten. Repeated verification
creates new dated DAG receipts; retain earlier evidence. Reconcile a selected
actual manifest with `verify_gold.py --manifest <path> --receipt <new-path>`.
Do not run submitted-artifact finalization scripts to record this supplement.

## Workshop 4 handoff

Use `runtime_verification.json` and `gold_samples.json` to select this successful
batch. Portable Parquet copies are in `workshop_3/samples/runtime_20261123/`;
original working output is under the manifest's `datalake_gold/` directory.
Do not sum batches or text snapshots as independent weather events. VADER labels
describe lexical tone, not severity or validated public opinion.

This closes the revised-DAG/Linux-test execution gap. It does not implement
Workshop 4, validate a CHI, supply a county crosswalk, expand the historical
years/stations or certify current live-source freshness. No weather API query
was made during this verification. Hashes are indexed in `sha256.json`.
