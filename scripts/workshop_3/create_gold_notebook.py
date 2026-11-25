"""Create the offline Pandas preview of actual Spark Gold output samples."""
from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[2]


def main():
    cells=[]
    def md(text):cells.append(nbf.v4.new_markdown_cell(text))
    def code(text):cells.append(nbf.v4.new_code_cell(text))
    md('''# Workshop 3 - Gold outputs

Team 9 - Multi-Hazard Weather Impact Monitoring.

These are verified outputs of the successful revised Airflow/PySpark Gold run. We inspect
the two saved datasets with Pandas. This notebook does not run Spark, query NWS
or access PostgreSQL. The first quality notebook motivates the methods; the
Gold contract documents the fields, estimators and dashboard questions.''')
    code('''from pathlib import Path
import hashlib
import json
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

root = next(p for p in [Path.cwd().resolve(), *Path.cwd().resolve().parents]
            if (p / "workshop_3/evidence/eda_20261124/gold_samples.json").exists())
register = json.loads((root / "workshop_3/evidence/eda_20261124/gold_samples.json").read_text())
manifest_path = root / "workshop_3/samples/eda_20261124/gold_manifest.json"
assert hashlib.sha256(manifest_path.read_bytes()).hexdigest().upper() == register["manifest_sha256"]
manifest = json.loads(manifest_path.read_text())
assert manifest["identity"]["config"]["schema_version"] == "weather-gold-v2-course-eda"
tables = {}
for name, item in register["outputs"].items():
    path = root / item["sample_path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest().upper() == item["sha256"]
    tables[name] = pd.read_parquet(path)
    assert len(tables[name]) == item["rows"]
governance, storytelling = tables["governance"], tables["storytelling"]
print("Verified Airflow batch:", manifest["identity"]["batch_id"])
display(governance.head())
display(storytelling.head())''')
    md('''## 1. Schema and keys

Governance is a long metric table with availability and method fields. Storytelling
is monthly per-source/type/unit and station where applicable. Null station values
for statewide event records are intentional; county allocation is not implemented.''')
    code('''governance.info()
storytelling.info()
assert not governance.duplicated(["source", "station", "population", "period", "variable", "unit", "metric"]).any()
assert not storytelling.duplicated(["source", "station", "period", "event_type", "severity_unit"]).any()
display(storytelling.groupby("source")["record_count"].sum().to_frame("unique_source_records"))''')
    md('''## 2. Governance: quality and snapshot volume

Repeated exports are not additional weather events. Null fractions describe a
specific source/field; some nulls express a different time grain, not missing
observations. Structural compliance is not a certification of all provider QC.''')
    code('''metrics = ["snapshot_rows", "unique_records", "repeated_snapshot_fraction", "schema_compliance_fraction"]
display(governance[governance["metric"].isin(metrics)][["source", "metric", "value", "method"]])
nulls = governance[governance["metric"].eq("null_fraction")]
display(nulls.pivot(index="variable", columns="source", values="value"))
review = governance[governance["population"].isin(["all_days", "positive_reported_precipitation"]) &
                    governance["metric"].isin(["skewness", "excess_kurtosis", "iqr_review_fraction", "zscore_review_fraction"])]
display(review[["station", "variable", "population", "metric", "value", "numerator", "denominator", "status"]])
zero_iqr = review[review["variable"].eq("PRCP") & review["population"].eq("all_days") & review["metric"].eq("iqr_review_fraction")]
assert zero_iqr["value"].isna().all()
assert zero_iqr["status"].eq("unavailable_zero_or_missing_scale").all()''')
    md('''## 3. Storytelling: what was recorded?

Plot reported Storm Events records by month, then station temperature and rain
separately. One station is not statewide measured weather. Monthly means of
daily TMAX/TMIN are not monthly absolute maxima/minima. Rain totals are meaningful;
sums of temperatures and storm magnitudes are deliberately absent.''')
    code('''events = storytelling[storytelling["source"].eq("noaa_storm_events")]
daily = storytelling[storytelling["source"].eq("ghcn_daily")]
assert storytelling.loc[~storytelling["event_type"].eq("PRCP"), "precipitation_total_mm"].isna().all()
event_counts = events.groupby("period")["record_count"].sum()
temperature = daily[daily["event_type"].isin(["TMAX", "TMIN"])].pivot(index="period", columns="event_type", values="mean_value")
rain = daily[daily["event_type"].eq("PRCP")].set_index("period")["precipitation_total_mm"]
fig, axes = plt.subplots(3, 1, figsize=(12, 8))
event_counts.plot(ax=axes[0], title="Oklahoma reported event records per month")
temperature.plot(ax=axes[1], title="USW00013967 monthly mean daily temperatures")
rain.plot(ax=axes[2], title="USW00013967 monthly reported precipitation")
axes[0].set_ylabel("Records")
axes[1].set_ylabel("degrees C")
axes[2].set_ylabel("mm")
plt.tight_layout()
plt.show()
display(daily[["station", "period", "event_type", "record_count", "measured_count", "mean_value", "precipitation_total_mm"]].head(9))''')
    md('''## 4. Narrative storytelling: bounded 2021 scope

These text columns cover registered Oklahoma 2021 NOAA records only. Keywords
are descriptive token frequencies; lexical tone is not hazard severity.
Other years have no portable narrative Silver in this delivery.''')
    code('''text_story = storytelling[storytelling["text_record_count"].gt(0)].copy()
assert text_story["text_record_count"].sum() == 1324
assert (text_story[["positive_count", "neutral_count", "negative_count"]].sum(axis=1)
        == text_story["text_record_count"]).all()
display(text_story[["period", "event_type", "text_record_count", "mean_sentiment_score",
                    "positive_count", "neutral_count", "negative_count", "top_keywords_json"]].head(12))
display(text_story.groupby("period")[["text_record_count", "positive_count", "neutral_count", "negative_count"]].sum())
display(governance[governance["metric"].str.contains("narrative|text_length", na=False)]
        [["period", "metric", "value", "status"]].head(18))''')
    md('''## 5. Reconciliation and dashboard handoff

The separate Pandas reconciliation checks the same Silver input hashes,
deduplication, source totals, sample shape estimators and station/month aggregates.
These descriptive/diagnostic inputs are ready to inform dashboard design;
they do not implement CHI, forecasting, causality or a completed Dash application.''')
    code('''audit = json.loads((root / "workshop_3/evidence/guide_gold_reconciliation.json").read_text())
assert audit["output_hashes_verified"] and audit["unique_gold_keys"]
assert audit["source_record_totals_reconciled"] and audit["zero_iqr_not_fabricated"]
display(pd.Series(audit))
print("Gold previews completed without source or database calls.")''')
    nbf.write(nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{
        'display_name':'Python 3','language':'python','name':'python3'}}),ROOT/'notebooks/04_gold_review.ipynb')


if __name__=='__main__':main()
