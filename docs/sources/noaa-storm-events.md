# NOAA Storm Events - Workshop 1 Source Notes

**Owner:** Kevin Rincon  
**Reviewer:** Pablo Garzon  
**Task IDs:** W1-K01 (documentation), W1-K03 (sample and profile)  
**Status:** documentation prepared; live evidence not captured yet

## Why this source is required

NOAA Storm Events is Team 9's first historical source. It records significant
weather events reported through the National Weather Service and provides
event time, geography, type, impacts, narratives, and hazard-specific severity
fields. It cannot be replaced by NWS Alerts: the former supplies the historical
baseline, while the latter supplies current and recently updated alerts.

## Official references

- [Storm Events Database](https://www.ncei.noaa.gov/access/storm-events-database/)
- [Bulk CSV archive](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/)
- [Bulk CSV README](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/README)
- [Bulk CSV field specification](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Bulk-csv-Format.pdf)
- [Storm Events Database user guide](https://www.ncei.noaa.gov/access/storm-events-database/assets/pdf/Storm_Events_Database_User_Guide.pdf)
- [NWS Directive 10-1605](https://www.weather.gov/directives/sym/pd01016005curr.pdf)

## Access methods and their roles

| Method | Best use in this project | Limitation |
| --- | --- | --- |
| Public Parquet files queried with DuckDB | Workshop 1 exploration, row estimates, deterministic small samples, and candidate-region comparison | It is a query path, not yet the accepted production ingestion contract |
| Yearly compressed CSV files | Workshop 2 historical ingestion and reproducible year partitions | Full archives are too large for Git and may be republished after corrections |
| Interactive website | Manual inspection and learning the fields | Not suitable for a reproducible pipeline |

The NOAA tutorial stored under `notebooks/references/noaa/` demonstrates the
first method. It is reference material, not the required profiling notebook.

## Dataset structure

The bulk archive exposes three related tables:

- `details`: one event record and its descriptive, temporal, geographic, impact,
  narrative, and severity fields;
- `locations`: zero or more location records associated with an event;
- `fatalities`: zero or more direct or indirect fatality records.

`EVENT_ID` links the three tables. Before it is treated as a universal primary
key, the Workshop 1 profile must verify uniqueness within each table and across
the selected years.

Important fields to inspect include `EVENT_ID`, `EPISODE_ID`, `STATE`,
`STATE_FIPS`, `CZ_TYPE`, `CZ_FIPS`, `CZ_NAME`, `EVENT_TYPE`,
`BEGIN_DATE_TIME`, `END_DATE_TIME`, `BEGIN_LAT`, `BEGIN_LON`, `END_LAT`,
`END_LON`, `MAGNITUDE`, `MAGNITUDE_TYPE`, damage and casualty fields, and the
event narratives. This list is a profiling target, not a claim that every field
is complete or consistent.

## Coverage and revision caveats

The database begins in 1950, but the set of recorded event types is limited in
early years. Availability since 1950 does not mean Team 9 should ingest the
entire history. The current project proposal is to evaluate complete years
2010-2025 and then keep at least five complete years if volume or cross-source
coverage requires a smaller range.

Bulk filenames contain both a data year (`dYYYY`) and a creation date
(`cYYYYMMDD`). NOAA can republish historical year files after corrections.
Production ingestion must therefore record the exact filename, retrieval time,
checksum, and content hash instead of assuming that a year is immutable.

The current year is incomplete and should not be used as part of the historical
baseline until the team explicitly defines how partial periods are handled.

## Workshop 1 sample contract

The first evidence sample contains 250 `details` records selected from the
official 2024 compressed CSV without normalizing source values or columns. The
deterministic filter is:

- state: Oklahoma;
- source year: 2024, a complete year used only for the first profile;
- event families relevant to compound hazards: flood/heavy rain, convective
  wind, heat, cold, and winter weather;
- stable ordering by time and `EVENT_ID` before applying the row limit.

The equivalent SQL lives in
`workshop_1/samples/noaa_storm_events/sample_query.sql`, and the executed
PowerShell extraction lives under `scripts/workshop_1/`. The state and proposed
2010-2025 historical window remain open decisions. Capturing this one-year
sample does not approve either decision.

For the evidence to be accepted, Kevin must record:

1. the exact archive URL and extraction filter;
2. retrieval time and extraction-tool version;
3. row and column counts;
4. a SHA-256 checksum of the saved CSV;
5. the untouched archive in ignored raw storage and the derived reviewable CSV
   under `workshop_1/samples/noaa_storm_events/`;
6. a matching entry in `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`;
7. profiling results in `notebooks/01_source_profiling.ipynb`.

## Required profile

The NOAA section of the project notebook must report, from actual evidence:

- schema and inferred data types;
- row count and distinct `EVENT_ID` count;
- exact and identifier duplicates;
- null percentage per field, emphasizing timestamps, geography, severity,
  impacts, and narratives;
- timestamp parsing success, ranges, duration anomalies, and time-zone values;
- latitude/longitude validity and missing-coordinate rates;
- state, county/zone, event-type, source, magnitude-type, and unit frequencies;
- numeric ranges and impossible values;
- examples of real quality problems, if observed.

No quality issue should be listed merely because it seems plausible. Each
reported issue must point to an evidence row or a reproducible aggregate.

## Historical ingestion direction for Workshop 2

Unless Workshop 1 evidence contradicts it, use the official yearly compressed
CSV archives as the production source of record. Land each `.csv.gz` file
unchanged below `data/raw/noaa_storm_events/details/year=YYYY/`, record its
filename and checksum, and parse it into canonical tables later. Keep these
bulk files ignored by Git.

The Parquet tutorial remains valuable for exploration and sample generation;
it does not by itself implement partitioned ingestion, idempotency, validation,
quarantine, or source-revision handling.

## Open questions for review

- Does Oklahoma provide enough records in all proposed event families and all
  four assigned sources?
- Should the final state scope use counties, NWS forecast zones, or both through
  a documented crosswalk?
- Is 2010-2025 manageable for Storm Events and GHCN-Daily while still providing
  a useful seasonal baseline?
- Which severity fields and units are comparable enough to feed the preliminary
  Compound Hazard Index?

