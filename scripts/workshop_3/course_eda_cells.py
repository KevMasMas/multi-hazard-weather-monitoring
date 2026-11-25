"""Course-aligned additions to the saved-data quality notebook.

Adapted from EngAndres/ud-public EDA notebooks, reviewed 2026-11-24.
The academic-material register pins the reviewed source commit and hashes.
"""
import nbformat as nbf


def md(text): return nbf.v4.new_markdown_cell(text)
def code(text,figure=None):
    cell=nbf.v4.new_code_cell(text)
    if figure:cell.metadata['report_figure']=figure
    return cell


def extend_course_review(cells):
    result=[]
    for cell in cells:
        source=cell.source
        if cell.cell_type=='markdown' and source.startswith('# Workshop 3 -'):
            cell.source='''# Workshop 3 - Silver data quality review

Kevin David Rincon Valencia and Pablo Garzon Gomez - Team 9.

We follow the course EDA sequence: inspect a DataFrame, check types and missing
values, describe distributions, compare outlier methods, inspect relationships,
and document curation decisions before Gold. All data comes from saved files.

The quality population is the frozen 13-export review (2021-2025, one GHCN station).
The current Airflow Gold batch also includes two later replay exports; both
selections reconcile to the same 19,039 source records. Repeated exports do not
represent additional weather events. Raw and Silver values are preserved.

Course sources: [EDA and curation](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/notebooks/eda_data_curation.ipynb),
[visualizations](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/notebooks/eda_visualizations.ipynb),
and [automatic profiling](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/notebooks/eda_ydata_profiling.ipynb).
The reviewed latest-file hashes are recorded in `academic_materials.json`.
Run using the separate `requirements-workshop3-eda.in` environment; this notebook
does not install packages or run weather requests.'''
        if cell.cell_type=='code' and source.startswith('from pathlib import Path'):
            cell.source=source.replace('import math','import math\nimport numpy as np\nfrom scipy import stats as sp_stats')
            cell.source=cell.source.replace('root / "workshop_3/evidence"','root / "workshop_3/evidence/eda_20261124"')
            cell.source=cell.source.replace('frames, hashes = [], {}','frames, hashes = [], {}\nfrozen_register_path = root / "workshop_3/evidence/silver_review.json"\nfrozen_register_sha256 = hashlib.sha256(frozen_register_path.read_bytes()).hexdigest().upper()')
        if cell.cell_type=='markdown' and source.startswith('## 5. Decisions'):
            continue
        if cell.cell_type=='code' and source.startswith('summary.to_csv'):
            continue
        if cell.cell_type=='markdown' and source.startswith('## 7.'):
            cell.source=source.replace('## 7.','## 6.',1)
        if cell.cell_type=='code' and 'fig, axes = plt.subplots(2, 3' in source:
            cell.metadata['report_figure']='quality_1'
        if cell.cell_type=='code' and 'One-station seasonal context' in source:
            cell.metadata['report_figure']='quality_2'
        if cell.cell_type=='code' and 'Selected narrative length' in source:
            cell.metadata['report_figure']='quality_3'
        result.append(cell)
        if cell.cell_type=='code' and 'Verified exports:' in source:
            result.extend([
                md('''## 0. Inspect the loaded DataFrame

These are saved Silver snapshots. Numeric record/run IDs are identifiers, so
they are excluded from weather distribution summaries.'''),
                code('''df_raw = raw
print("Rows and columns:", df_raw.shape)
df_raw.info()
display(df_raw[["source", "event_type", "observed_at_utc", "observed_date",
                "severity_value", "severity_unit"]].head())
display(df_raw.dtypes.to_frame("dtype"))
print("Fully repeated rows:", int(df_raw.duplicated().sum()))
print("Repeated source/key rows:", int(df_raw.duplicated(["source", "source_key"]).sum()))
# Snapshot lineage is reconciled in the next section before counting source records.''')])
        if cell.cell_type=='code' and source.startswith('fields = ['):
            result.extend([
                code('''null_rows = []
for source_name, group in canonical.groupby("source"):
    for field in fields:
        null_rows.append({"source": source_name, "field": field,
                          "null_count": int(group[field].isna().sum()),
                          "records": len(group), "null_percent": group[field].isna().mean() * 100})
null_report = pd.DataFrame(null_rows)
display(null_report)
ordered = canonical.sort_values("source")
fig, ax = plt.subplots(figsize=(11, 3))
image = ax.imshow(ordered[fields].isna().astype(int).T, aspect="auto", cmap="Reds", vmin=0, vmax=1)
ax.set_yticks(range(len(fields)), fields)
ax.set(xlabel="Source records ordered by source", title="Missing-value map: source semantics remain visible")
plt.colorbar(image, ax=ax, label="1 = missing / not applicable")
plt.tight_layout(); plt.show()''','quality_missing'),
                md('''## 2.1 Station table and quality checks

We align measurements by their actual daily date before comparing PRCP, TMAX
and TMIN. No synthetic date labels or row-position joins are used. An apparent
gap or an outlier is a review finding; it is not automatically an invalid record.'''),
                code('''assert not daily.duplicated(["station", "date", "event_type"]).any()
assert daily.station.nunique() == 1
wide = daily.pivot(index="date", columns="event_type", values="severity_value").sort_index()
wide = wide[["PRCP", "TMAX", "TMIN"]]
display(wide.head())
display(wide.describe().round(3))
expected_dates = pd.date_range("2021-01-01", "2025-12-31", freq="D")
missing_dates = expected_dates.difference(wide.index)
checks = pd.DataFrame([
    {"dimension": "Uniqueness", "check": "Duplicate canonical source/key groups",
     "count": int(canonical.duplicated(["source", "source_key"]).sum()), "denominator": len(canonical), "handling": "Reject conflicting snapshots; retain one reviewed record"},
    {"dimension": "Completeness", "check": "Missing station dates in 2021-2025",
     "count": len(missing_dates), "denominator": len(expected_dates), "handling": "Report gaps; do not fabricate measurements"},
    {"dimension": "Validity", "check": "Negative recorded precipitation",
     "count": int(wide.PRCP.lt(0).sum()), "denominator": int(wide.PRCP.notna().sum()), "handling": "Review/quarantine physical invalidity"},
    {"dimension": "Consistency", "check": "TMIN exceeds TMAX on the same source date",
     "count": int(wide.TMIN.gt(wide.TMAX).sum()), "denominator": int(wide[["TMIN", "TMAX"]].notna().all(axis=1).sum()), "handling": "Review paired source values"},
])
display(checks)
# Missingness mechanisms cannot be inferred from a percentage alone.
# Source-inapplicable dates and missing storm magnitudes are retained without imputation.''')])
        if cell.cell_type=='code' and source.startswith('def profile('):
            result.extend([
                md('''### Descriptive statistics as in class

We add variance, range, P95 and the mean-median difference, then calculate
skewness and excess kurtosis with SciPy as the instructor does. Gold uses the
equivalent Spark moments. Values remain separated by variable and unit.'''),
                code('''shape_rows = []
for element in ["PRCP", "TMAX", "TMIN"]:
    values = wide[element].dropna()
    shape_rows.append({"element": element, "n": len(values),
                       "variance_ddof1": values.var(ddof=1), "range": values.max() - values.min(),
                       "p95": values.quantile(0.95), "mean_median_gap": abs(values.mean() - values.median()),
                       "skewness": sp_stats.skew(values),
                       "excess_kurtosis": sp_stats.kurtosis(values)})
class_statistics = pd.DataFrame(shape_rows)
display(class_statistics.round(4))''')])
        if cell.cell_type=='code' and 'One-station seasonal context' in source:
            result.extend([
                md('''## 5. Relationships and curation decisions

Pearson and Spearman are calculated on the same complete station dates.
Correlation is an association, not causation, prediction or evidence that an
extreme value should be removed. No feature selection or model is fitted.'''),
                code('''paired = wide.dropna()
pearson = paired.corr(method="pearson")
spearman = paired.corr(method="spearman")
print("Aligned complete dates:", len(paired))
fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
for ax, matrix, title in zip(axes, [pearson, spearman], ["Pearson", "Spearman"]):
    image = ax.imshow(matrix, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(3), matrix.columns); ax.set_yticks(range(3), matrix.index)
    for row in range(3):
        for col in range(3): ax.text(col, row, f"{matrix.iloc[row, col]:.2f}", ha="center", va="center")
    ax.set_title(title)
fig.colorbar(image, ax=axes.ravel().tolist(), shrink=0.8)
fig.suptitle("One-station daily associations, 2021-2025")
plt.show()
display(pearson); display(spearman)''','quality_correlations'),
                md('''### Treatment experiment on a copy

The class demonstrates P5-P95 clipping and log1p. For hazard monitoring, clipping
may suppress the extremes we want to retain. We quantify that effect on a copy,
then retain the original values. The transformation below is an analytical
experiment, not a new source capture, a replacement Silver dataset or a model.'''),
                code('''precipitation = wide["PRCP"].dropna()
p5, p95 = precipitation.quantile([0.05, 0.95])
clipped_trial = precipitation.clip(lower=p5, upper=p95)
log_trial = np.log1p(precipitation)
clipping_review = pd.DataFrame([{
    "experiment": "P5-P95 clipping on a copy", "p5_mm": p5, "p95_mm": p95,
    "changed_measurements": int(clipped_trial.ne(precipitation).sum()),
    "measurements": len(precipitation), "original_max_mm": precipitation.max(),
    "trial_max_mm": clipped_trial.max(), "original_total_mm": precipitation.sum(),
    "trial_total_mm": clipped_trial.sum(),
    "decision": "Not applied: retain recorded extremes and physical totals"}])
display(clipping_review)
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
axes[0].hist(precipitation, bins=35, alpha=0.6, label="Original")
axes[0].hist(clipped_trial, bins=35, alpha=0.6, label="Clipping experiment")
axes[0].set(xlabel="mm", title="Recorded rain and clipping trial"); axes[0].legend()
axes[1].hist(log_trial, bins=35)
axes[1].set(xlabel="log1p(PRCP / 1 mm), dimensionless", title="Shape inspection only; not Gold input")
plt.tight_layout(); plt.show()
pd.testing.assert_series_equal(wide["PRCP"].dropna(), precipitation)
curation_decisions = pd.DataFrame([
    {"finding": "Repeated exports", "decision": "Reconcile by source/key and reviewed lineage; do not count snapshots twice"},
    {"finding": "Source-inapplicable nulls", "decision": "Keep explicit time grain; no global median/KNN filling"},
    {"finding": "Missing storm point/magnitude", "decision": "Keep source evidence and completeness metrics; no invented point or zero"},
    {"finding": "Zero-heavy and right-skewed PRCP", "decision": "Separate all-day and positive-rain review; zero-IQR method unavailable"},
    {"finding": "Seasonal temperature / rare extremes", "decision": "Use monthly context; retain flags without removal"},
    {"finding": "Automatic profiling warnings", "decision": "Review with source/unit/key semantics; warnings are not validated errors"},
])
display(curation_decisions)''','quality_curation')])
    result.extend([
        md('''## 7. Automatic profiling as in class

`ProfileReport` complements the manual audit. The station report uses actual
daily dates and three measurements. A separate source-quality projection shows
missingness without pooling incompatible event magnitudes or profiling numeric
database IDs. Duplicate warnings in that projection do not define source identity.
Open the saved HTML reports; findings still require a source-aware decision.'''),
        code('''from ydata_profiling import ProfileReport
from IPython.display import FileLink
profile_dir = root / "workshop_3/profiling"
profile_dir.mkdir(parents=True, exist_ok=True)
station_profile = ProfileReport(
    wide.reset_index(), title="GHCN USW00013967 - daily Silver quality, 2021-2025",
    explorative=True, pool_size=1, progress_bar=False,
    correlations={"pearson": {"calculate": True}, "spearman": {"calculate": True},
                  "kendall": {"calculate": False}, "phi_k": {"calculate": False},
                  "cramers": {"calculate": True}},
    missing_diagrams={"bar": True, "matrix": True, "heatmap": True})
station_profile_path = profile_dir / "ghcn_station_quality.html"
station_profile.to_file(station_profile_path)
station_description = json.loads(station_profile.to_json())
assert station_description["table"]["n"] == len(wide)
display(FileLink("../workshop_3/profiling/ghcn_station_quality.html"))'''),
        code('''quality_projection = canonical[["source", "event_type", "observed_date", "observed_at_utc",
                                "latitude", "longitude"]].copy()
quality_projection["observed_date"] = pd.to_datetime(quality_projection["observed_date"])
quality_projection["observed_at_utc"] = pd.to_datetime(quality_projection["observed_at_utc"], utc=True).dt.tz_localize(None)
quality_projection["magnitude_missing"] = canonical["severity_value"].isna()
source_profile = ProfileReport(
    quality_projection, title="Silver source/time/point completeness - reviewed canonical records",
    explorative=True, pool_size=1, progress_bar=False,
    correlations={"auto": {"calculate": False}, "pearson": {"calculate": False},
                  "spearman": {"calculate": False}, "cramers": {"calculate": False}},
    interactions={"continuous": False},
    missing_diagrams={"bar": True, "matrix": True, "heatmap": True})
source_profile_path = profile_dir / "silver_source_quality.html"
source_profile.to_file(source_profile_path)
source_description = json.loads(source_profile.to_json())
assert source_description["table"]["n"] == len(canonical)
display(FileLink("../workshop_3/profiling/silver_source_quality.html"))'''),
        md('''## 8. Save the evidence and hand off

The reviewed Silver register and production Gold remain unchanged. The new
tables, profiling reports and figures document the course-aligned quality review.
Dashboard layout, interactive filters, forecasting/feature-selection experiments,
CHI and model evaluation are outside this notebook. No classroom toy-data result
is presented as a finding about Oklahoma.'''),
        code('''import importlib.metadata
for name, frame in {"distribution_review": summary, "seasonal_review": seasonal,
                    "missingness": null_report, "quality_checks": checks,
                    "class_statistics": class_statistics, "pearson": pearson,
                    "spearman": spearman, "clipping_experiment": clipping_review,
                    "curation_decisions": curation_decisions}.items():
    frame.to_csv(out / (name + ".csv"), index=name in ["pearson", "spearman"], lineterminator=chr(10))
assert hashlib.sha256(frozen_register_path.read_bytes()).hexdigest().upper() == frozen_register_sha256
profiles = {}
for name, path, description in [("station", station_profile_path, station_description),
                                ("source_quality", source_profile_path, source_description)]:
    profiles[name] = {"path": path.relative_to(root).as_posix(),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
                      "rows": description["table"]["n"], "columns": description["table"]["n_var"],
                      "alerts": [str(alert) for alert in description.get("alerts", [])]}
audit = {"input_sha256": hashes, "frozen_input_register_sha256": frozen_register_sha256,
         "verified_exports": len(files), "snapshot_rows": len(raw),
         "unique_source_records": len(canonical), "source_counts": {str(k): int(v) for k,v in canonical.groupby("source").size().items()},
         "station_dates": len(wide), "complete_paired_dates": len(paired),
         "quality_checks": checks.to_dict(orient="records"), "clipping_experiment": clipping_review.to_dict(orient="records"),
         "profiles": profiles, "weather_requests": False, "raw_or_silver_changed": False,
         "class_methods": "scipy.stats.skew(), scipy.stats.kurtosis(), Pandas std() and quantile(); IQR 1.5 and absolute Z-score >3",
         "gold_methods": "Equivalent Spark skewness/excess kurtosis; sample std and linear quartiles",
         "versions": {name: importlib.metadata.version(name) for name in ["pandas", "numpy", "scipy", "matplotlib", "ydata-profiling"]}}
(out / "course_eda_review.json").write_text(json.dumps(audit, indent=2) + "\\n", encoding="utf-8", newline="\\n")
print("Evidence saved:", out)
print("Original source records preserved:", len(canonical))''')])
    return result
