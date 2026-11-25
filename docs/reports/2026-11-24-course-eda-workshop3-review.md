# Course EDA update and Workshop 3 scope - 2026-11-24

Kevin reported that the professor extended the delivery window and requested
using the updated EDA material, then explicitly selected the instructor's method
and removal of additions outside the class scope. This reopens the current W3
review package. Previous delivery artifacts are archived byte-for-byte in
`workshop_3/archive/Workshop_3_Pre_EDA_20261124.zip` before revision.

## Reviewed academic sources

Requested update commit: [`d938aa2`](https://github.com/EngAndres/ud-public/commit/d938aa2acb2d33067588aece5bb9e10f6951a692),
24 November 2026, 13:07 UTC. Its changed files are the three EDA notebooks and
the EDA presentation. The latest downloaded head was `626b7090f349e01b8df9941a611be1ceb2234b8c`
(Cloud examples). Exact reviewed file URLs and SHA-256 are in
`workshop_3/evidence/eda_20261124/academic_materials.json`; academic files are
cached in ignored storage and are not copied into the project repository.

| Material | W3 use | Kept for later / not adopted |
| --- | --- | --- |
| [ExploratoryDataAnalysis.pdf](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/slides/ExploratoryDataAnalysis.pdf) | Slide 12 (physical PDF page 24) explicitly places EDA before Gold as a Silver quality gate. Slides 14-17 cover quality dimensions, outlier context, treatment and missing-data decisions. | Feature selection/training examples do not become W3 requirements. Slide annotations do not establish a new deadline. |
| [eda_data_curation.ipynb](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/notebooks/eda_data_curation.ipynb) | DataFrame/head/info/describe, null map, duplicate checks, descriptive tables, SciPy shape statistics, sample-std Z-score, 1.5-IQR, Pearson/Spearman, curation experiment on a copy. | Do not transfer the toy Australian dataset's hardcoded physical cutoffs or imputation assumptions to Oklahoma. No Isolation Forest, feature selector or classifier added. |
| [eda_visualizations.ipynb](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/notebooks/eda_visualizations.ipynb) | Histograms, boxplots, readable comparison/correlation displays supporting quality findings. Real source dates are used. | Dashboard layout, interactive filters and broader visualization design remain W4. The gallery's row-bin monthly proxy is unnecessary because our records have real dates. |
| [eda_ydata_profiling.ipynb](https://github.com/EngAndres/ud-public/blob/d938aa2acb2d33067588aece5bb9e10f6951a692/courses/data-analysis-programming/notebooks/eda_ydata_profiling.ipynb) | `ProfileReport`, declared correlation/missingness settings and saved standalone HTML. | Automatic warnings are reviewed, not accepted as proven errors. Dependency installation is a separate reproducible environment, rather than notebook-side package mutation. |

Notebook cell references below are zero-based for the downloaded version:
curation 5-8 profiling; 14 descriptive table; 17 SciPy moments; 20 correlations;
23 quality ledger; 25 Z-score/IQR; 29 treatment experiment. Profiling notebook
11 constructs `ProfileReport`, 13 displays it and 15 saves HTML.

## Method selection and field mapping

Use the instructor's `scipy.stats.skew()` / `scipy.stats.kurtosis()` calls and
Pandas `std()` / `quantile()`. The revised Spark Gold uses equivalent moments;
the additional comparison of alternative estimators was removed at Kevin's
instruction. Metric names become `skewness` and `excess_kurtosis` under
`weather-gold-v2-course-eda`. Existing v1 samples/receipts are historical, not
silently reinterpreted. Constant or insufficient groups remain unavailable.

Class `Rainfall`, `MaxTemp`, `MinTemp` map to our PRCP/mm, TMAX/degC, TMIN/degC
from actual station/date rows. No `RainTomorrow` target, synthetic Australian
data issues, imaginary current observation or new source query is introduced.
Provider time-grain nulls, storm magnitudes and geometry remain source-aware.

## Observed additions to the quality notebook

- 19,039 unique reviewed records remain unchanged; the 13-file quality snapshot
  contains 22,553 exported rows. Later replay exports are tracked separately in
  actual Gold runs, not counted as additional events.
- 1,826 aligned station dates; zero missing expected dates, negative PRCP or
  same-date TMIN>TMAX findings in this selected population. These checks do not
  certify every possible data-quality dimension.
- Pearson TMAX/TMIN 0.9028 and Spearman 0.9064 describe association on the same
  dates; neither is a forecast or justification for deleting either variable.
- P5-P95 clipping on a copy changes 91 PRCP measurements, caps the maximum from
  167.4 to 16.3 mm, and changes total rainfall from 4,373.7 to 2,819.6 mm. The
  experiment supports retaining extremes for monitoring; clipping is not applied.
- The station profile contains 1,826 rows/four columns; the source-quality
  projection contains 19,039 rows/seven columns. A reported 501 duplicates in
  that reduced projection are not duplicate canonical source keys. The original
  key uniqueness check is zero; no rows are removed based on that warning.
- Unique dates and 78.6% zero PRCP are legitimate profile alerts to interpret.
  Source-inapplicable date fields remain null without median/KNN imputation.

Exact new tables, profile hashes, kernel execution and method/version metadata
are under `workshop_3/evidence/eda_20261124/`. HTML reports are in
`workshop_3/profiling/`. The archive preserves the previous delivered revision;
the current PDF/package can now be revised under the reported extension.

## Boundary and handoff

No W4 app, model training, future-weather target, CHI or automatic emergency
recommendation is introduced. The handoff is quality evidence and typed Gold
inputs. The professor's workshop guide remains the requirement source; the EDA
examples guide implementation without making every classroom technique mandatory.
No professor statement about estimator correction is invented, and no new
Kevin/Pablo approval, deadline timestamp, upload, commit or push is inferred.
