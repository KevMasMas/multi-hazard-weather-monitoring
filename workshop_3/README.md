# Workshop 3 - Silver quality and Gold preparation

## Post-submission runtime verification - 2026-11-23

The pulled revision `6fa48a9` now has actual successful revised Bronze/Silver/Gold
runs in Docker/Airflow, including the new text tasks. Gold run
`w3_runtime_gold_20261124T003408` produced **650 governance / 607 storytelling
rows**, independently reconciled. All **54 Linux tests passed without skips**,
including three Spark fixtures and eight real PostGIS integration cases skipped
previously on Windows. The extra two tests cover repeated/conflicting text exports.

The delivered PDF, LaTeX/assets, notebooks, package ZIPs and submission manifest
remain unchanged (20 baseline hashes checked). Kevin reported the document was
already submitted; no platform receipt or new personal approval is inferred.
See the [runtime evidence and W4 handoff](evidence/runtime_20261123/README.md)
and [portable current Airflow outputs](samples/runtime_20261123/README.md).
Earlier dated results below describe their original revisions.

## Current guide-aligned result (2026-11-21)

The team selected the supplied Workshop 3 PDF as this delivery's guide despite
the 2026-I cover. A verified local PySpark run now reads every checked numerical
Parquet in `datalake_silver/` plus the 2021 NOAA narrative sidecar, and publishes
650 governance / 607 storytelling rows to `datalake_gold/`. Text coverage is
bounded to 1,324 genuine NOAA Oklahoma 2021 narratives; 2022-2025 text is
unavailable in the portable evidence. VADER lexical tone is descriptive, not
hazard severity. Both notebooks were regenerated and executed in fresh kernels
(8/6 code cells, zero errors). The report PDF and exact samples are linked below.

At the 21 November checkpoint the revised DAGs had not run in Airflow. This gap
was closed by the 23 November supplement above; the earlier 625-row result remains
historical. Personal approval is not inferred. Package evidence: `evidence/text_quality.json`,
`evidence/guide_gold_reconciliation.json`, `evidence/guide_gold_samples.json`.

Current branch: `feat/workshop-3-quality-gold`, based on Workshop 2 commit
`f35c75c`. The quality/Gold pipeline, incremental core and report are prepared
for team review. No commit, push, personal approval or platform submission is
inferred. County allocation, match evaluation, dashboard and CHI remain open.

## Review and delivery files

- [English report PDF](Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf),
  with editable [LaTeX source/assets](report/).
- Executed notebooks: `notebooks/03_silver_quality_review.ipynb` and
  `notebooks/04_gold_review.ipynb` in the repository root.
- [Actual Gold samples](samples/gold/) and [incremental sample excerpts](samples/incremental/).
- [Incremental state/source contract](INCREMENTAL_CONTRACT.md),
  [Gold/quality contract](GOLD_CONTRACT.md), [evidence register](EVIDENCE_REGISTER.md)
  and [reproduction guide](../deliveries/03-workshop-3/DEMO_GUIDE.md).
- `Workshop_3_Silver_Reproduction_Inputs.zip`: all 13 reviewed Silver files,
  1,965,977 uncompressed bytes. Restore offline with
  `python scripts/workshop_3/restore_silver.py`; exact hashes are checked before
  any write. Existing different files fail rather than being overwritten.

## Verified incremental result - 2026-11-21

- 12 synthetic/fault and real isolated-PostGIS tests passed, with no skips.
- Saved replay: 238 new alerts and 700 new KOKC observations; second pass all
  unchanged. Saved KOKC pages are partial and cannot advance coverage state.
- Announced live validation: zero active OK alerts and 903 KOKC observations,
  complete returned pagination, zero rejects. Captured-byte reruns added no
  records/revisions. Raw responses are ignored; committed excerpts are labelled
  parsed derivatives. This was bounded validation, not continuous operation.
- The real incremental replay DAG completed `poll_alerts`, `poll_station` and
  `group_candidates`; it was left paused. Automatic scheduling defaults disabled.
- Five saved-data polygon/time associations are intra-NWS and unconfirmed.
  Zero live associations were produced. Five W1 NOAA/GHCN wind candidates remain
  reused historical context, not newly discovered W3 matches.

## Verified Gold result - 2026-11-21

- Real Airflow run: `w3_gold_20261121T144317`, successful on its first attempt.
- PySpark 3.5.7 / Java 17 / Airflow 2.10.4, local[2], 1 GiB driver, UTC.
- 13 verified Silver exports: 22,553 snapshot rows -> 19,039 unique source/key
  records (13,561 NOAA and 5,478 GHCN); 3,514 extra snapshot rows are replay copies.
- Governance: **625 rows**. Storytelling: **607 rows**.
- Independent Pandas reconciliation: 40 shape statistics, 180 station/month and
  427 storm/month/type/unit groups matched; output hashes and totals checked.
- **8 new tests and 29 regression tests passed**, no failures/errors/skips.
- The quality notebook executes 7 code cells and the Gold notebook 5, no errors.
- Same batch replay reuses the committed files with identical hashes and no new
  batch directory. Earlier failed permission-boundary run is retained separately.

Review [actual output samples](samples/gold/),
[executed Gold notebook](../notebooks/04_gold_review.ipynb),
[field/method/dashboard contract](GOLD_CONTRACT.md),
[evidence register](EVIDENCE_REGISTER.md) and
[runbook](../deliveries/03-workshop-3/DEMO_GUIDE.md).
The Parquet files are generated by Spark; the notebook reads them with Pandas.

The first real run failed when Hadoop tried chmod on a Windows-mounted output
directory. Spark now writes part files on Linux `/tmp`, copies the finished
Parquet to host staging without changing permissions, verifies it and publishes
both datasets together. No existing source file or SQL migration was modified.

## Executed quality review

Open `notebooks/03_silver_quality_review.ipynb` from the repository. The seven
code cells ran successfully in a fresh Python 3.12 kernel using the existing
Workshop 2 environment. No weather API or database connection is used.

The notebook verifies 13 original/replayed successful exports referenced by the
Workshop 2 historical/replay receipts, including their hashes. Local ignored
Silver files are required; it fails if they are missing rather than silently
substituting a smaller population. It does not indiscriminately read every file
in the folder, including unrelated pilot exports.

It reconciles 22,553 snapshot rows into 19,039 source/key records before computing
statistics. The 3,514 additional snapshot rows represent repeated exports, not
3,514 duplicated real events. Run ordering is local to the same database history.

## Findings and initial decisions

- GHCN has 1,826 dates per element, 2021-2025, from one station.
- PRCP has 78.64% reported zeros: its all-day IQR is zero. That IQR rule is
  marked unavailable for this population rather than flagging all positive rain.
- Positive reported precipitation (`PRCP > 0 mm`) has 390 measurements. This is
  an explicit exploratory subset, not a formally validated wet-day definition.
  Its 1.5-IQR rule flags 25 measurements for review; no records are removed.
- All-day precipitation sample skewness is approximately 7.30 and sample excess
  kurtosis 89.64. These describe this station/window, not incorrect records or a
  statewide climatology. Z-score flags are a comparison, not a normality claim.
- Temperature distributions are also reviewed by calendar month. Pooled-year
  thresholds alone do not establish anomalies after accounting for seasonality.
- Raw values, physical-invalidity quarantine policies and Workshop 2 exports are
  unchanged. Statistical review flags are not deletions or imputation.

Exact values, sample sizes, estimator conventions and unavailable-method reasons
are in `evidence/distribution_review.csv` and `seasonal_review.csv`.
The class-example formula conventions still require verification; these are
explicit Pandas conventions and proposed review thresholds.

## Reproduce

Use the Python 3.12 environment described by `requirements-workshop2.in`:

```bash
python scripts/workshop_2/execute_review_notebook.py \
  --notebook notebooks/03_silver_quality_review.ipynb \
  --receipt workshop_3/evidence/notebook_execution.json
```

Regenerate the notebook source only when intentionally editing it with
`python scripts/workshop_3/create_quality_notebook.py`; then execute it again.
The generator replaces outputs, so it is not needed for routine review.

## Run Gold

With the 13 registered bulk Silver files available locally:

```bash
docker compose build airflow-scheduler
docker compose up -d --wait airflow-webserver airflow-scheduler airflow-triggerer
python scripts/workshop_3/verify_airflow_gold.py
```

The optional package cache command in the runbook handles a slow PyPI connection;
software archives remain ignored. A clean clone includes the Gold samples and
the exact 13-file Silver reproduction ZIP described above.
Do not silently substitute a smaller population if inputs are missing.

## Remaining work

1. Team review of metric definitions, threshold conventions and guide alignment.
2. Review of incremental state/lifecycle rules, candidate uncertainty and the PDF.
3. Resolve the professor's specification discrepancy and compare exact classroom
   formula conventions; no written clarification is currently recorded.
4. Later dashboard implementation using the documented descriptive/diagnostic
   questions; wider station/year coverage and county allocation remain open.

Initial dashboard scope is descriptive and exploratory diagnostic analysis.
Forecasting and prescriptive interventions are not implied. The active plan/log
remain in `deliveries/03-workshop-3/`; ownership stays in `WORK_BOARD.md`.
