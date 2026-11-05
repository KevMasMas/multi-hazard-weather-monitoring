# NOAA Reference Notebook

`noaa_storm_events_duckdb_tutorial.ipynb` is an official NOAA/NCEI tutorial
copied into the repository as learning material.

It shows how DuckDB can query public Storm Events Parquet files in Google Cloud
Storage without downloading the entire dataset. It demonstrates filters,
`details`/`fatalities` joins, conversion to Pandas, plotting, and CSV export.

It is not Team 9's Workshop 1 deliverable because it:

- contains generic examples unrelated to the selected project scope;
- has not been executed in this repository;
- does not profile the four assigned sources;
- does not preserve Team 9 evidence metadata or checksums;
- does not implement the professor's required quality and cross-source checks.

Do not overwrite this reference. Put Team 9's executable work in
`notebooks/01_source_profiling.ipynb` and source evidence under
`workshop_1/samples/`.

Known tutorial cautions found during review:

- the fatality example counts complete duplicate rows rather than explicitly
  grouping fatalities by `EVENT_ID`;
- the `BETWEEN` date example includes both endpoints;
- one Pandas CSV export includes the index unless `index=False` is supplied;
- an empty filtered result can make the selected-list access fail;
- package versions are not pinned and the notebook contains no saved outputs.

