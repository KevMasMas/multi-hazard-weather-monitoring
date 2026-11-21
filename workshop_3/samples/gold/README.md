# Actual Gold output samples

These two Parquet files are unchanged copies of the successful Airflow run
`w3_gold_20261121T144317`, computed using PySpark 3.5.7:

- `governance_20261121_144319_caeba6938516.parquet`: 625 metric rows.
- `storytelling_20261121_144319_caeba6938516.parquet`: 607 monthly summary rows.

They summarize 19,039 unique source/key records from the reviewed 2021-2025
Silver population. They are not new weather responses or 1,232 independent
weather events. Governance fractions, unavailable statistics and method fields
are defined in `workshop_3/GOLD_CONTRACT.md`.

`manifest.json` preserves the original committed batch metadata, input/code/config
hashes and schemas. Its `data/gold/...` output paths refer to the original ignored
bulk location. For these portable copies, use
`workshop_3/evidence/gold_samples.json`, which supplies repository paths and the
same exact output hashes. Source acquisition URLs and original native response
lineage remain in the preserved Workshop 2 evidence.

Open `notebooks/04_gold_review.ipynb` from the repository to inspect the samples
offline with Pandas/PyArrow. No Spark, database or weather request is needed to
preview them. Recomputing the full historical batch does require the 13 local
Silver files named in the frozen input register.

One GHCN station is represented. County allocation, CHI, live conditions and
forecasting are not implemented by these summaries. Do not concatenate every
dated Gold snapshot to count weather observations; select one committed batch.
