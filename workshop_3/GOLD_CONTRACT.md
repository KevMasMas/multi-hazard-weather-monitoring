# Gold datasets and dashboard questions

Implementation: `src/multi_hazard_weather_monitoring/gold.py`.
Configuration: `config/workshop3_gold.json`. This is a versioned historical
snapshot, not a live NWS feed or a forecast.

## Guide correspondence

The supplied `Airflow-PostgreSQL-ETL.pdf` separates acquisition, curation and
Gold summaries, persistent mounts, scheduled DAGs and Parquet outputs. Its Gold
example reads database rows; the Workshop 3 handout specifically asks for local
PySpark consolidation of multiple Silver Parquet files. This implementation uses
the handout's Silver-to-Gold input path while preserving the guide's separation
of stages. It does not claim the guide itself uses PySpark.

The review notebook and Gold share the frozen set of 13 successful historical
and replay exports recorded in `workshop_3/evidence/silver_review.json`.
Spark reads all those paths together as one DataFrame. Reading an unfiltered
folder would also pick up older pilot exports not in that reviewed population.
Adding input files requires an explicitly reviewed register update; the weekly
schedule does not automatically acquire new data or expand the input list.
No upstream time-window sensor is added to this frozen historical DAG: all
registered exports must already exist and pass validation. This differs from
the guide's live scheduled-curation dependency and must be revisited before
connecting automatically changing incremental sources.

Every input is hash-checked, its 18 field names/types are checked, required
identities and date/instant exclusivity are validated, and conflicting copies
fail. Same-key observations are selected by descending successful local run ID,
then input path after content consistency checks. This order is meaningful only
within the same database's run history. Repeated export rows are not new events.

## Governance - long-form metric rows

Key: `(source, station, population, period, variable, unit, metric)` within a
batch. Nullable key dimensions mean the metric does not use that dimension;
they must not be replaced with invented station/region values.

| Column | Meaning |
| --- | --- |
| `source`, `station` | Source and station where applicable; storm metrics have no station. |
| `population` | Unique source records, all daily values, positive reported rain, or calendar-month group. |
| `period` | `all`, year-month for volume, or month number for seasonal shape. |
| `variable`, `unit` | Column under review or GHCN element and its physical unit. |
| `metric`, `value` | Metric identity and nullable double result. Fractions are 0-1, not percentages. |
| `numerator`, `denominator` | Counts behind fraction metrics where applicable. |
| `method`, `status` | Computation convention and availability reason. Undefined is null, not zero. |
| `batch_id` | Actual Airflow/CLI batch identity; manifest records input/code/config hashes. |

Metrics include snapshot volume, unique records, repeated snapshot fraction,
post-selection duplicate business-key fraction,
source-specific null fractions, checked structural-schema compliance, monthly
record volume, provider QC flags, distribution statistics and review flags.
No ingestion-frequency compliance is invented for the historical manual backfill.
No language/sentiment metric is added to the weather project.

Schema compliance means the implemented structural checks passed; it is not a
claim that all source-quality or meteorological validity tests passed. Daily
missing UTC instants and missing storm dates are expected record semantics.
Nonempty GHCN QC flags are retained and reported, not silently certified valid.

Distribution metrics use exact interpolated quartiles, sample standard deviation
(ddof=1), bias-corrected sample skewness and sample excess kurtosis (normal
reference zero). Spark's population skewness/kurtosis are transformed to the
sample conventions used in the Pandas notebook:

```text
sample_skew = sqrt(n*(n-1))/(n-2) * spark_skew
sample_excess_kurtosis = (n-1)/((n-2)*(n-3)) * ((n+1)*spark_excess_kurtosis + 6)
```

Insufficient/constant groups return unavailable shape statistics. IQR review
uses 1.5 times the IQR only when IQR > 0. Z-score > 3 uses sample standard
deviation only when positive. The zero-heavy all-day PRCP series has zero IQR,
so its IQR rate is unavailable; positive reported rain (`PRCP > 0 mm`) is a
separate exploratory population. It is not a provider-defined wet-day threshold.
Temperatures also have month-specific context. No flags delete or modify data.
These thresholds are explicit project review choices, pending exact class-example
comparison, not a verified instruction to discard weather extremes.

## Storytelling - monthly weather summaries

Key: `(source, station, period, event_type, severity_unit)` within a batch.
`geographic_scope` distinguishes `Oklahoma_state` reported events from
`station_only` measurements; county/station crosswalks remain unimplemented.

| Column | Interpretation |
| --- | --- |
| `record_count` | Unique source records in that month/type; measurement count is not event count. |
| `measured_count` | Records with a reported magnitude/value; distinguishes zero from missing. |
| `mean_value`, `min_value`, `max_value` | Within the same source/type/unit only. No magnitude is invented for unmeasured events. |
| `observed_dates` | Distinct dates with records; not a storm-frequency denominator or population exposure. |
| `missing_point_count` | Records without source point coordinates; does not drop zone-based events. |
| `precipitation_total_mm` | Sum only for GHCN PRCP/mm, null for temperatures and storm magnitudes. |
| `analysis_type` | `descriptive_not_forecast`; no causal, predictive or prescriptive inference. |

Monthly event dates are derived from UTC event instants; GHCN retains its source
daily date. These calendars are not assumed identical daily observation windows.
Storm Events often contains county/zone records belonging to one episode;
`record_count` must be labelled reported event records, not independent storms.

## Plotly Dash handoff

| View / analysis | User question | Gold inputs |
| --- | --- | --- |
| Data health / descriptive | What coverage and missingness do we have? | Governance unique volume, source nulls and monthly volume. |
| Replay audit / descriptive | How much folder volume is repeated snapshots? | Snapshot/unique counts and repeated snapshot fraction. |
| Weather timeline / descriptive | Which event types were reported, and when? | Storytelling event type/month counts, explicit statewide scope. |
| Station history / descriptive | How do temperature/rain vary through the observed years? | Station monthly means/min/max and PRCP totals, with sample counts/units. |
| Distribution review / exploratory diagnostic | Which groups deserve closer inspection? | Method-labelled shape and IQR/Z-score flags; null availability shown. |

Filter by source, period and element; do not compare unlike units or present a
single station as statewide measured weather. Association is not causality.
The dashboard itself, CHI validation, predictions and safety advice are not
implemented by these summaries. The course project's database/analytical-view
versus handout Gold-only dashboard source discrepancy remains documented; do not
silently remove the relational system.

### Workshop 1 story correspondence

Source: `workshop_1/report/content.tex`, "Functional user and user stories".
The accepted table has priorities and text, not numbered story IDs; no new IDs
are attributed to it here.

| Existing story | Gold support now | Remaining work |
| --- | --- | --- |
| Must: compare measurements with a seasonal baseline | Station distributions by calendar month and monthly temperature/rain summaries. | Formal baseline/current anomaly comparison and broader historical/station coverage. |
| Must: trace records to source and capture | Batch manifest retains input/code/config hashes and source/run lineage; existing Silver retains record provenance. | Dashboard drill-down to individual source records. |
| Must: review recent observations, alerts and events by county | Historical source/type/month context only. | NWS incremental sources, reviewed county assignment and current map/list. |
| Should: filter hazard, time and county | Source/type/month/station dimensions are available. | County filters cannot be implemented faithfully until allocation is reviewed. |
| Should: see freshness and completeness | Source missingness, volume, sample counts and repeated-snapshot metrics. | Live-source freshness/state metrics; historical run time must not be presented as current weather freshness. |
| Could: export filtered evidence | Typed Parquet summaries and traceable manifests. | User-facing filtered export in the later dashboard. |

Workshop 1 explicitly excludes prediction, automated emergency recommendations
and replacing official warnings. The descriptive/diagnostic direction preserves
that boundary rather than inventing predictive or prescriptive model results.

## Execution and publication

`weather_gold_processing` has one TaskFlow task, `summarize_silver`, with a
20-minute timeout and one retry after 30 seconds. Weekly schedule: Monday 06:00
UTC; `catchup=False`, one active run. Each run rebuilds the full configured
2021-2025 snapshot; it is not a weekly event-window query. The DAG starts paused
under the common Airflow configuration until explicitly enabled.

Spark runs `local[2]`, UTC session, 1 GiB driver memory, two shuffle partitions,
no Spark UI port and no Spark Connect/Pandas-on-Spark/Arrow interchange. This
bounded local setting is a resource-conscious instance of the handout's local
mode; it is not a cluster benchmark. Java 17 and PySpark 3.5.7 are in the custom
Airflow image; `pip check` is part of its build.

Both small summaries are computed with Spark DataFrame/SQL operations, written
as one actual Parquet file per dataset, read back for count/column verification,
and published together by renaming a staged batch directory. Names retain UTC
batch time plus a run hash to avoid collisions. Full bulk output is ignored under
`data/gold/`; selected small real samples are copied for review separately.
Spark/Hadoop writes its temporary part directories on Linux `/tmp`. The finished
Parquet file is copied to the host-mounted staging directory without copying
POSIX permissions, then read back and included in atomic batch publication.
Writing Hadoop part directories directly to the Windows bind mount failed with
`chmod: Operation not permitted` in the first real DAG run; that failed run is
preserved separately. Linux-only fixture tests did not reveal this host-filesystem
boundary, which required the real end-to-end run.

Retry with the same run/time/input/code/config verifies and reuses the committed
manifest/output hashes. Changed identity or corrupt output fails instead of
overwriting a completed batch. A new run is a separately traceable snapshot.
The manifest is the readiness marker; dashboards must not combine every dated
Gold file as if each were new observations.

## References

- Course handout: `../Project/Workshop_3.pdf` in the supplied local course folder;
  [published reference](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_3.pdf).
- [Airflow/PostgreSQL guide](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/guides/Airflow-PostgreSQL-ETL.pdf).
- [PySpark 3.5.7 installation](https://spark.apache.org/docs/3.5.7/api/python/getting_started/install.html).
- [Spark multi-path Parquet reader](https://spark.apache.org/docs/3.5.7/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.parquet.html).

Actual execution and verification evidence is recorded separately; this contract
does not establish personal approval or successful runtime execution by itself.
