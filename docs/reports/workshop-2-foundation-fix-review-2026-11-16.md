# Workshop 2 foundation correction review

- **Date:** 2026-11-16 America/Bogota
- **Branch:** `workflow-2`
- **Scope:** follow-up to `workshop-2-pull-review-2026-11-16.md`; no Docker, database or DAG execution is claimed.

## Findings disposition

| Finding | Change | Verification | Remaining limit |
| --- | --- | --- | --- |
| R1, NOAA `MG` as unit | Preserve `MAGNITUDE_TYPE` separately; wind magnitude uses `kn` as physical unit. SQL has a separate `magnitude_type` column. | Synthetic measured-gust fixture yields `(51.0, kn, MG)`; saved NOAA sample still parses 250 records. | No conversion to a common wind speed is stored yet. Other magnitude dimensions need source-specific mapping. |
| R2, unregistered source bytes | Offline runner requires the SHA-256 in Workshop 1's saved evidence audit before landing/parsing. | Altered synthetic body raises `registered_capture_hash_mismatch`; three saved inputs pass. | New official captures need their own registered identity and retrieval metadata. |
| R3, Windows temporary cleanup | Close temporary streams before deleting them; publish capture and manifest via atomic replacement. | Injected fsync failure preserves its original exception and leaves no temporary file in the test directory. | Crash durability and multi-process concurrent writers are not demonstrated. |
| R4, canonical validation absent | First source-aware validation layer rejects negative PRCP, impossible sub-absolute-zero temperature, negative/unknown-unit magnitude and nonfinite values with reason codes. | Negative PRCP fixture yields `negative_precipitation`; saved samples retain 1,363 accepted parsed records. | This is an initial validator, not the full domain schema or database quarantine. |
| R5, CSV-only landing/manifest overwrite | Accept explicit CSV or gzip content type; preserve gzip bytes and native extension. Reject conflicting manifest origin for the same blob. | Gzip fixture remains byte-identical with `.gz` path; repeat identical landing reuses one body; changed origin raises `capture_manifest_conflict`. | Per-run receipt/history, concurrent publication and ready-signal semantics remain to implement. |
| R6, nullable SQL uniqueness | `rejected_record` uses PostgreSQL 16 `UNIQUE NULLS NOT DISTINCT`; magnitude type is separate. | Static SQL review only. | Migration, domain tables and transactional rerun/rollback require PostgreSQL/PostGIS execution. |

`python -m unittest discover -s tests -p test_workshop2_foundation.py -v`
passed six tests when the workspace test directory was accessible. The first
sandboxed attempt failed while creating temporary directories with Windows
access denied; the authorized execution passed all six tests. This was an
environment permission issue, not an observed data failure.

`python scripts/workshop_2/review_offline_captures.py` again produced three
capture summaries and 1,363 accepted parsed records; the small summary SHA-256
remained `47491AE61A721B82B10B6AAAAA470B6DB58EF10D14298C2D9126035AE265FC9E`.
The output is an offline parser audit, not a DAG-produced Bronze/Silver sample.

Docker and `psql` were not resolved on this session's PATH; the standard Docker
Desktop executable path and uninstall registry probe also did not locate Docker.
This does not disprove a separate WSL installation or a different user install.
The next runtime gate is to locate a working Docker CLI/daemon, then apply the
PostGIS migration and implement the transactional historical loader.
