# Current W3 course EDA evidence - 2026-11-24

This revision follows Kevin's instruction to use the professor's EDA approach
after the reported delivery extension. The previous delivery is preserved in
`workshop_3/archive/Workshop_3_Pre_EDA_20261124.zip` (20 baseline artifacts).
No precise new deadline, personal approval, commit/push or upload is invented.

## Read first

- `academic_materials.json`: instructor update/HEAD, exact reviewed URLs and hashes.
- `course_eda_review.json`: saved-input hashes, quality checks, class methods,
  two HTML profile hashes, treatment experiment and package versions.
- `quality_notebook_execution.json` / `gold_notebook_execution.json`: 16/6 code
  cells, fresh explicit isolated kernels, zero errors.
- `runtime/linux_tests.json`: 55 passed, no failures/errors/skips; synthetic
  fixtures and disposable PostGIS schemas, not weather observations.
- `runtime/gold_20261125T000455.json`: actual successful first-attempt Airflow
  Gold run (24 November America/Bogota, 25 November UTC); DAG left paused.
- `gold_samples.json` / `gold_reconciliation.json`: exact current 650/607 outputs
  and independent numerical/text checks. Current schema: `weather-gold-v2-course-eda`.
- `report_qa.json` / `final_review.json` / `sha256.json`: current PDF, reviewed
  package and source/evidence integrity.

The method is the class sequence: DataFrame inspection, source-aware missingness
and duplicates, descriptive statistics, SciPy skewness/excess kurtosis, IQR/Z-score,
correlation, documented curation decisions and `ProfileReport`. The extra
estimator comparison was removed. No model, feature selector or dashboard was
introduced. W4 boundaries are documented in the course-review report.

Automatic projection-duplicate warnings do not override source-key identity.
The clipping/log1p experiment is performed on a copy; raw/Silver observations
are preserved. Historical Gold inputs contain replay snapshots, not additional
independent weather events. No new weather API call was made.

## Reproduce the current review

Restore saved Silver with `scripts/workshop_3/restore_silver.py`. Use the separate
Python 3.12 EDA environment in `workshop_3/profiling/README.md`, then execute both
notebooks using `execute_eda_notebooks.py` with their explicit current receipts.
The notebook does not install packages. Regenerate report figures with
`create_report_assets.py`, compile `workshop_3/report/main.tex`, render/inspect
all pages, run `check_report.py --expected-pages 10 --receipt
workshop_3/evidence/eda_20261124/report_qa.json --confirm-visual-review`, then use
`finalize_course_eda.py` to seal this revision. Older finalizers target their
historical revisions and must not reseal the current package.

An actual new pipeline verification, when needed, can use the existing tested
Docker image and the dated evidence parameter:

```bash
docker compose exec -T airflow-scheduler python /opt/weather/scripts/workshop_3/verify_container_runtime.py --mode tests --evidence-dir workshop_3/evidence/eda_20261124/runtime
python scripts/workshop_3/verify_airflow_runtime.py --stage gold --evidence-dir workshop_3/evidence/eda_20261124/runtime
python scripts/workshop_3/prepare_course_samples.py
```

New executions create new run IDs/hashes. Preserve earlier receipts and choose
one committed batch; do not combine snapshot totals or replace source evidence.
