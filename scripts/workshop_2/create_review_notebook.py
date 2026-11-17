"""Build the short, offline Pandas review notebook from explicit teaching cells."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[2]


def main():
    cells = []
    def md(text): cells.append(nbf.v4.new_markdown_cell(text))
    def code(text): cells.append(nbf.v4.new_code_cell(text))
    md('''# Workshop 2 - Historical pipeline review

**Team 9: Kevin David Rincon Valencia and Pablo Garzon Gomez**

We read three Parquet files produced by successful Airflow runs. The purpose is
to check the saved output with Pandas: records, types, missing values, units and
provenance. This notebook makes no API or database calls.

The samples cover Oklahoma Storm Events in 2021 and one Oklahoma City GHCN
station in 2021/2022. The separate database receipt describes the full executed
2021-2025 slice. Station samples are not statewide weather coverage.''')
    code('''from pathlib import Path
import hashlib
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

here = Path.cwd().resolve()
root = next(p for p in [here, *here.parents]
            if (p / "workshop_2/samples/manifest.json").exists()
            or (p / "samples/manifest.json").exists())
samples = root / "workshop_2/samples" if (root / "workshop_2").exists() else root / "samples"
evidence = root / "workshop_2/evidence" if (root / "workshop_2").exists() else root / "evidence"
manifest = json.loads((samples / "manifest.json").read_text())
print("Python:", sys.version.split()[0], "| Pandas:", pd.__version__)
print("Samples:", len(manifest["entries"]))''')
    md('''## 1. Check the files before reading

The manifest records the SHA-256 and size of each packaged file. A changed file
must fail this check rather than silently produce different results.''')
    code('''for name, expected in manifest["files"].items():
    body = (samples / name).read_bytes()
    assert hashlib.sha256(body).hexdigest().upper() == expected["sha256"], name
    assert len(body) == expected["bytes"], name
print("All packaged hashes and sizes match.")''')
    md('''## 2. Read a Parquet as a DataFrame

Each output contains accepted records for one ingestion run. GHCN has one row
per station, date and element; Storm Events has one row per source event ID.''')
    code('''frames = {}
for entry in manifest["entries"]:
    df = pd.read_parquet(samples / entry["silver"])
    assert len(df) == entry["metrics"]["accepted"] + entry["metrics"]["unchanged"]
    frames[entry["partition"]] = df

storms = frames["OK_2021"]
daily = pd.concat([df for key, df in frames.items() if key.startswith("USW")], ignore_index=True)
display(storms.head())
display(daily[["source_key", "observed_date", "event_type", "severity_value", "severity_unit"]].head())''')
    code('''storms.info()
display(daily.dtypes.to_frame("dtype"))
display(daily.groupby(["event_type", "severity_unit"])["severity_value"].describe())''')
    md('''## 3. Missing fields and time grain

GHCN dates are daily observations, so `observed_at_utc` is intentionally null.
Storm Events keeps the UTC instant and may have no point coordinates. Missing
coordinates are retained with source geography in the database; no point or
midnight timestamp is invented. Missing optional measurements are not imputed.''')
    code('''all_samples = pd.concat(frames.values(), ignore_index=True)
display(all_samples.groupby("source").size().to_frame("records"))
display(all_samples.isna().sum().to_frame("missing"))
assert daily["observed_at_utc"].isna().all()
assert daily["observed_date"].notna().all()
assert storms["observed_at_utc"].notna().all()
assert storms["observed_date"].isna().all()
assert (all_samples["latitude"].isna() == all_samples["longitude"].isna()).all()''')
    md('''## 4. Keys, units and quality attributes

Only like units are compared. Hail magnitude is in inches; wind is in knots;
GHCN temperatures and precipitation were requested in metric units. Original
GHCN attribute strings are preserved. A nonempty quality flag requires review,
and is not automatically treated as a new hazard event.''')
    code('''duplicates = all_samples.duplicated(["source", "source_key"]).sum()
assert duplicates == 0
display(all_samples.groupby(["source", "event_type", "severity_unit"], dropna=False).size().to_frame("records"))
attributes = daily["quality_attributes"].fillna("")
quality_flag = attributes.str.split(",").str[1].fillna("")
display(quality_flag.value_counts(dropna=False).rename_axis("GHCN quality flag").to_frame("records"))
print("Duplicate business keys:", duplicates)''')
    md('''## 5. Distribution review

We use a boxplot and the 1.5-IQR rule separately for each daily variable. These
are review flags, not deletion criteria: extreme rain or temperature may be the
signal this project needs. Values and sample counts remain unchanged.''')
    code('''fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
iqr_review = []
for ax, element in zip(axes, ["PRCP", "TMAX", "TMIN"]):
    values = daily.loc[daily["event_type"].eq(element), "severity_value"].dropna()
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    flagged = ((values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr))
    ax.boxplot(values)
    ax.set_title(element)
    ax.set_ylabel("mm" if element == "PRCP" else "degrees C")
    iqr_review.append({"element": element, "n": len(values), "review_flags": int(flagged.sum()),
                       "lower_fence": q1 - 1.5 * iqr, "upper_fence": q3 + 1.5 * iqr})
plt.tight_layout()
plt.show()
display(pd.DataFrame(iqr_review))''')
    md('''## 6. Follow one record back to Bronze

The Parquet row stores a CSV line number and capture hash. For GHCN, multiple
measurements refer to the same daily CSV row. The Bronze JSON is a parsed view;
the packaged CSV bytes remain separate. NOAA's CSV is an explicitly documented
Oklahoma subset of the preserved nationwide gzip response.''')
    code('''entry = manifest["entries"][0]
bronze = json.loads((samples / entry["bronze"]).read_text())
record = frames[entry["partition"]].iloc[0]
source_row = bronze["rows"][int(record["source_line"]) - 2]
assert str(source_row["EVENT_ID"]) == record["source_key"]
assert record["capture_sha256"].upper() == bronze["original_capture"]["sha256"].upper()
display(pd.Series({"event_id": source_row["EVENT_ID"], "event_type": source_row["EVENT_TYPE"],
                   "source_line": int(record["source_line"]), "run_id": int(record["run_id"]),
                   "capture_sha256": record["capture_sha256"]}))''')
    md('''## 7. Full historical slice and quarantine evidence

This section reads the captured database audit rather than opening a live
connection. The acquisition window is 2021-2025. The semester target remains
2010-2025, and adding stations and reviewed county assignments remains open.
Zero rejected rows in these inputs does not mean the rejection path was untested:
integration fixtures exercise quarantine and transaction rollback separately.''')
    code('''database = json.loads((evidence / "delivery_database.json").read_text())
display(pd.DataFrame(database["sources"]))
display(pd.DataFrame(database["daily_years"]))
display(pd.DataFrame(database["event_years"]))
assert not database["duplicate_business_keys"]
tests = json.loads((evidence / "wsl_test_results.json").read_text())
assert tests["successful"] and not tests["skipped"]
print("Verified tests:", tests["passed"], "| No live calls were made by this notebook.")''')
    md('''## 8. Review result

The packaged samples reconcile with their run metrics and hashes. Units and
daily/instant time grains remain explicit. We preserve weather extremes, missing
point locations and source flags rather than filling them with invented values.
The database evidence and Airflow receipts are technical checks, not personal
approval or confirmation of submission.''')
    notebook = nbf.v4.new_notebook(cells=cells, metadata=dict(kernelspec=dict(display_name='Python 3', language='python', name='python3')))
    nbf.write(notebook, ROOT/'notebooks/02_historical_ingestion_review.ipynb')


if __name__ == '__main__':
    main()
