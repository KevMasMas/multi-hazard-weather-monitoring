# ADR 0010 - Course EDA methods for the revised W3 delivery

Date: 2026-11-24. Status: implemented at Kevin's instruction; final team review
and resubmission remain unrecorded.

## Context

Kevin reported a delivery extension, requested the instructor's updated EDA
material and explicitly asked to use the professor's code approach, removing
additional comparisons not taught in class. The prior delivered revision and
its 20 baseline artifacts were archived before changing the review package.

## Decision

Use the instructor's SciPy `skew()` and `kurtosis()` calls, Pandas `std()` and
`quantile()`, IQR 1.5 and absolute Z-score >3, source-aware profiling and simple
descriptive/bivariate figures. Spark Gold uses the equivalent moments. Rename
the two shape metric keys to `skewness` and `excess_kurtosis`, and identify the
contract as `weather-gold-v2-course-eda`. The extra estimator comparison is
removed; original v1 artifacts are not silently relabelled.

The class treatment example is an experiment on a copy, used to justify retaining
real weather extremes. No clipping/imputation changes the saved source/Silver
or production Gold. Use `ydata-profiling` in a separate, pinned analysis environment.
Model training, feature selection and dashboard construction are not added to W3.

## Evidence and consequences

The 16-cell quality and six-cell Gold notebooks execute without errors. Current
Gold Airflow run `w3_runtime_gold_20261125T000455` succeeded with 650/607 rows;
55 Linux tests passed without skips. Full kernel, source, output and profiling
hashes are in `workshop_3/evidence/eda_20261124/`. Classroom source links, reviewed
commit/file hashes and the W3/W4 method boundary are in the course-review report.

Consumers should select the new v2 manifest and keys. The archived submission,
old sample files and dated runtime receipts remain evidence of their own versions.
No professor statement about additional statistical corrections, final team
approval, commit, push or platform acceptance is invented.
