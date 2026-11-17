# Workshop 2 pull review and WSL database milestone

- **Date:** 2026-11-16 America/Bogota
- **Reviewed pull:** `f7d7c55`; clean tree at start, `workflow-2`
- **Scope:** retain teammate corrections and execute saved-data pilot; no weather
  query, Workshop 1 artifact change, commit, push or personal approval

## Review and implementation

The pull fixes R1 magnitude unit/type, R2 expected capture hashes and R3 Windows
failure cleanup. Gzip preservation, manifest conflicts and initial validation
are present. Its ten tests passed with PYTHONPATH; plain discovery failed to
import the package. `scripts/workshop_2/run_tests.py` now sets both import paths
and optionally writes a test receipt, working on Windows and Ubuntu WSL.

Expanded validation rejects missing identity/type, malformed line/hash,
ambiguous/invalid time grain, non-UTC instants, incomplete/nonfinite/out-of-range
coordinates and wrong/missing daily units/value before SQL. Missing zone points
remain permitted. Seven added offline tests cover these boundaries. No source
QC interpretation or mean imputation is invented.

Historical loads acquire a transaction-scoped advisory lock per source before
key comparisons; end/state times use clock_timestamp rather than transaction
start time. No concurrency stress result is claimed. Domain/geography/revision
history remains unfinished; current canonical rows still use upsert.

## Runtime recovery and exact checks

Ubuntu starts with WSL 2 kernel 6.18.33.2, Python 3.14.4. Docker initially had
no engine pipe; app-context Desktop launch failed with sailor-ingest.sock access.
Kevin manually reopened Desktop through Windows Start and the engine became
available. No socket/data reset was attempted; this observation is not proof of
root cause. Verified Server 29.7.2 and Compose 5.4.0; Desktop server reports
4.87.0, superseding earlier installation-only version reports.

Installed Ubuntu python3.14-venv because ensurepip was absent. Created the
separate temporary Linux environment `/tmp/team9-workshop2-venv`. Driver 2.9.10
had no 3.14 binary wheel; minimal runtime now pins 2.9.11, which installed and
passed pip check. Full notebook lock remains a separate Python 3.12 reference.
Compose config/up --wait succeeded; PostGIS image 16-3.7 is healthy and its named
volume remains available. No separate Docker Engine was installed in Ubuntu.

The final WSL receipt records **20 passed, zero failed, zero skipped** tests:
17 offline and three actual PostGIS tests. Real tests create/drop only a random
UUID schema, not public application data. They verify load/quarantine and rerun,
mid-insertion rollback, and preserving prior values/checkpoint after failure.
Their invalid records are synthetic fixtures, not real source quality findings.
An intermediate receipt had three skips because host-shell interpolation emptied
the DB URL; explicit assignment reran all 20 and replaced the receipt.

The actual saved-capture historical path and CLI historical/status commands ran:

| Source | First accepted | Rerun accepted | Rerun unchanged | Canonical rows |
| --- | ---: | ---: | ---: | ---: |
| NOAA 2024 sample | 250 | 0 | 250 | 250 |
| GHCN 2025 measurements | 1,095 | 0 | 1,095 | 1,095 |

Zero duplicate source/key groups were found. The 2026 capture remains a smoke
fixture outside the baseline. Receipts:
`workshop_2/evidence/database_verification.json` and `wsl_test_results.json`.
Credentials are not stored in them. See `docs/WSL_SETUP.md` for reproduction.

## Remaining work

G0 runtime verified; G1 validation expanded/tested; G2 minimal transaction pilot
verified but domain/station/geography schema and revision/replay design incomplete.
Airflow services/two TaskFlow DAGs/exact-batch FileSensor, genuine JSON/Parquet
outputs, multi-year coverage, review notebook, PDF/ZIP and team delivery review
remain pending. The pilot is not five historical years, statewide completeness
or end-to-end DAG/Silver evidence. No complete Workshop 2 acceptance is claimed.

## Primary references

- https://docs.docker.com/desktop/features/wsl/
- https://github.com/docker/desktop-feedback/issues/676 (reported similar socket error, not proof of this machine's cause)
- https://pypi.org/project/psycopg2-binary/2.9.11/
- https://www.postgresql.org/docs/16/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS
- Professor guide/practice references remain in the dated course-material review.
