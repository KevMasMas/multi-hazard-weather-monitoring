# ADR 0004 - Oklahoma Geographic and Station Contract

- **Status:** Accepted for Workshop 1 design
- **Date:** 2026-11-05
- **Owner:** Pablo Garzon
- **Reviewer:** Kevin Rincon
- **Implementation milestone:** Workshops 2-4

## Context

The four sources use incompatible geographies: counties and forecast zones,
alert polygons/geocodes, station points, and occasionally missing event
coordinates. The Compound Hazard Index needs one stable regional grain without
discarding source geography or inventing point locations.

## Decision

Use Oklahoma as the study area and Oklahoma counties as the primary analytical
regions. Identify counties with stable state/county FIPS codes. Preserve NWS
forecast zones, alert polygons, source coordinates, and station points as
separate source geographies connected through auditable relations.

### Station selection rule

The final Oklahoma station inventory must be generated, not hand-picked:

1. discover candidate GHCN-Daily stations located in Oklahoma;
2. measure PRCP/TMAX/TMIN availability for every year in 2010-2025;
3. require at least 90% valid daily coverage in a year for that element/year
   to enter its baseline;
4. prefer stations with at least 12 qualifying years out of 16;
5. discover active NWS observation stations for the same area and retain their
   official identifiers/provider metadata;
6. link GHCN and NWS stations only through reviewed identity evidence such as
   official cross-reference, name/airport identity and coordinate proximity;
7. choose a county primary station by highest qualifying-year coverage, then
   lowest recent missingness, then stable station ID as a deterministic tie;
8. retain all qualifying secondary stations for sensitivity and health checks.

`USW00013967` and KOKC are the verified Oklahoma City pilot pair. They do not
establish statewide coverage and are not silently promoted to represent every
county.

### Geographic allocation rules

- **Storm Events county records (`CZ_TYPE=C`):** map state/county FIPS directly
  when valid and retain the original code/name.
- **Storm Events zone records (`CZ_TYPE=Z`):** map through a versioned NWS
  forecast-zone/county relation. If one zone intersects multiple counties,
  retain every candidate allocation and its method/weight.
- **NWS Alerts with geometry:** spatially intersect the original polygon with
  counties and store intersection area/ratio. Do not replace the source
  polygon.
- **NWS Alerts without geometry:** use affected zones/UGC geocodes through a
  versioned crosswalk. Null polygon does not mean null geography.
- **Stations:** assign point geometry to a county through a versioned
  effective-dated relation. Keep the per-observation geometry when supplied.
- **Ambiguous or missing geography:** retain the raw record and reason; do not
  invent coordinates or force a single county. Quarantine only when the
  downstream contract requires a region and no defensible mapping exists.

## Proposed regional entities

```text
region
  region_id, region_type, state_fips, county_fips, name, geometry,
  valid_from, valid_to

source_geography
  source_geography_id, source_id, geography_type, source_code,
  source_name, geometry, valid_from, valid_to, raw_reference

region_source_geography
  region_id, source_geography_id, relation_method, intersection_ratio,
  confidence_status, valid_from, valid_to

station
  station_id, source_id, source_station_code, name, geometry,
  provider, valid_from, valid_to

station_region_assignment
  station_id, region_id, assignment_method, distance_m,
  is_primary, valid_from, valid_to, review_status
```

Measurements/events reference the original station/source geography and the
derived region assignment separately. This keeps source truth distinct from an
analytical join.

## Missing-county behavior

Do not silently interpolate a county score from a distant station. A county
without sufficient station evidence receives an incomplete component and a
coverage reason. Spatial interpolation may be evaluated in Workshop 4 only
with sensitivity analysis, maximum-distance rules, and visible uncertainty.

## Consequences

- County CHI values remain interpretable while NWS zones and polygons are not
  discarded.
- Crosswalk tables require versioning because source boundaries/codes can
  change.
- One alert/event may relate to multiple counties; many-to-many relations are
  expected.
- Station coverage and geographic confidence become first-class data-health
  metrics.
- The dashboard can distinguish source geometry, analytical allocation, and
  incomplete coverage.

## Review note

The team accepted the contract in the joint Kevin/Pablo working session on
2026-11-05. Workshop 1 accepts the rule and pilot evidence; generating the full
16-year station inventory is historical-ingestion work and must not be claimed
complete yet.
