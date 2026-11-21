# ADR 0007 - Reviewed Silver snapshots and weather Gold summaries

- Date: 2026-11-20, America/Bogota
- Status: implementation decision for reciprocal team review; runtime evidence
  is recorded separately, not established by this document
- Context: Workshop 3 Gold/PySpark target and the executed Silver quality review

## Decision

Use a frozen register of the 13 successful historical/replay Silver exports
reviewed in the quality notebook. Read them together with Spark, validate hashes
and schemas, then select the latest observed successful local run for each
source/key. Reject conflicting versions before aggregation. Do not treat dated
exports as independent observations or apply cross-database run ordering.

Produce two typed Parquet summaries in one committed batch:

- Governance: source/field quality and volume, distribution statistics and
  availability-aware review rates, with method/denominator fields.
- Storytelling: monthly source/type/unit/station counts and measured-value
  summaries, with explicit statewide-event versus station-only scope.

Keep all-day and positive-rain distributions separate. A zero IQR does not
justify classifying every positive rainfall measurement as invalid. Mark the
rate unavailable and retain values; compare Z-score and seasonal populations
without claiming normality or automatically removing extremes.

Correct Spark's population skewness/excess kurtosis to the sample conventions
used by Pandas, and verify the values independently. Use exact interpolated
quartiles for this small data slice. Thresholds remain explicit exploratory
project choices pending comparison with the exact class formula convention.

Run PySpark 3.5.7 with Java 17 in the shared Airflow image, using local[2], a
1 GiB driver and two shuffle partitions. Schedule one active Gold run weekly
without catchup. The schedule rebuilds the full configured historical snapshot;
it is not live ingestion or an automatically changing input list.

## Alternatives and consequences

An unfiltered Silver-folder read would include unreviewed pilot snapshots and
could inflate counts. Selecting every latest version only by revision ID could
ignore a later sighting of an older revision. Deleting every statistical outlier
could remove the weather signal. These alternatives are not adopted.

The course guide's Gold example reads PostgreSQL; the Workshop 3 handout requires
multiple Silver Parquet/PySpark. This design follows the latter technical path
while retaining the guide's stage boundaries and the relational weather system.
The public-opinion/NLP domain discrepancy remains explicit. The later dashboard
source-contract discrepancy is not resolved by adding Gold.

One actual Parquet per small summary supports the handout's output nomenclature.
Both are staged and published together with a lineage manifest. The same batch
identity reuses verified committed output; changed inputs/code/config fail
instead of silently overwriting a batch. Keep bulk files ignored and copy only
selected actual output samples for review.

These summaries prepare descriptive and exploratory diagnostic dashboard views.
They do not implement forecasting, causal inference, CHI, verified county
allocation or official prescriptive safety advice. Wider 2010-2025 coverage,
additional stations and incremental integration remain separate work.
