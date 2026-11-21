# Workshop 3 technical review - 2026-11-21

Branch: `feat/workshop-3-quality-gold`, based on `f35c75c`. Local changes only;
no commit, push, merge, platform submission or W3 personal approval is recorded.

## Prepared artifacts

- English PDF: `workshop_3/Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf`;
  editable LaTeX, cover/logo and figures in `workshop_3/report/`.
- Executed quality and Gold-preview notebooks: `notebooks/03_silver_quality_review.ipynb`
  and `notebooks/04_gold_review.ipynb` (7/5 code cells, zero execution errors).
- Two actual Spark Gold samples and their manifest in `workshop_3/samples/gold/`;
  labelled incremental sample excerpts in `workshop_3/samples/incremental/`.
- Exact offline Silver restoration archive and `scripts/workshop_3/restore_silver.py`;
  13 files, 1,965,977 uncompressed bytes, all frozen hashes verified.
- Source/state and analytical contracts, Mermaid architecture, current plan/log,
  runbook, submission manifest and SHA-256 evidence register.

## Observed verification

| Scope | Observed result | Evidence |
| --- | --- | --- |
| Gold | 13 inputs, 22,553 snapshot rows -> 19,039 unique records; 625 governance / 607 storytelling rows | Gold manifest, reconciliation and actual successful DAG receipt |
| Tests | 8 Spark/offline tests + 12 incremental tests + 29 historical regressions; zero failures/errors/skips | `workshop_3/evidence/*tests.json`, `workshop2_regression.json` |
| Saved NWS replay | 238 new alerts / 700 new observations; unchanged second pass; no new versions | `incremental_replay.json` |
| Live validation | Announced query scope: active OK alerts plus paginated KOKC observations; zero / 903 records, zero rejects; unchanged captured-byte replay | `incremental_live.json` |
| Incremental DAG | Two source tasks followed by grouping succeeded, first attempts; left paused | `incremental_airflow_run.json` |
| Persistence | Real PostgreSQL restart preserves state/record/revision/candidate row hashes | `incremental_restart.json` |
| Database | 19,039 historical records preserved; integrated view 19,942 unique source/key rows, excluding replay/test | `incremental_database_audit.json` |
| Candidates | Five unconfirmed intra-NWS associations; zero current live associations; five reused W1 NOAA/GHCN context rows | Candidate samples, rule version, source IDs/hashes |
| Offline restoration | Clean temporary extraction and unchanged second extraction verify all 13 exact Silver files | Restoration script and final artifact audit |

The earlier Windows-bind chmod failure and disabled-mode scheduled-run rejection
remain in evidence. The latter made no weather calls; the corrected DAG schedules
automatically only after explicit live configuration. Empty active alerts are
successful source evidence, not invented event matches or an all-clear statement.

## Remaining gates

Kevin reviews the report/source semantics and Pablo cross-reviews orchestration,
replay/recovery and outputs as assigned on `WORK_BOARD.md`. Neither's W3 approval
is inferred from implementation. County allocation and labelled candidate-match
evaluation remain open, as do exact classroom formula comparison and the
cross-semester/domain/dashboard-source specification conflict. No professor
clarification is recorded. Wider years/stations, CHI and dashboard remain later
work. Five candidates do not establish five independent events or ground truth.

The complete Gold population can now be reproduced offline after cloning; live
2026-11-21 HTTP bodies remain in ignored local storage, with committed metadata
and clearly labelled excerpts. Repeating a live query later will return a new
source state and is not exact historical response reproduction.

The final offline timestamp-boundary audit found 902 live station records within
the requested interval and one before its start, zero after its end. All 903 are
preserved; later analytical windows must filter timestamps explicitly. This is
an observed response/request discrepancy, not a diagnosed provider fault.
See `workshop_3/evidence/nws_window_review.json` for exact IDs, times and hashes.
