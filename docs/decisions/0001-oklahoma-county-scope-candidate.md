# ADR 0001 - Oklahoma County Scope Candidate

- **Status:** Proposed
- **Date:** 2026-11-04
- **Owners:** Kevin Rincon and Pablo Garzon
- **Decision gate:** W1-S01

## Context

Team 9 needs a US scope that is broad enough to contain several interacting
hazards, small enough for a semester project, and representable across NOAA
Storm Events, GHCN-Daily, NWS Alerts, and NWS station observations.

## Proposal

Evaluate Oklahoma as the state-level study area and counties as the primary
regional unit for the Compound Hazard Index. Keep NWS forecast zones as source
geographies that require an explicit crosswalk or spatial allocation rule.

The initial historical-window candidate is 2010-2025, using complete calendar
years only. A smaller window must still include at least five complete years.

## Rationale to test

- Oklahoma is expected to expose several relevant hazard families rather than
  only a single dominant hazard.
- A single state is more manageable than a multi-state region.
- Counties are understandable dashboard units and align with many Storm Events
  records and alert geocodes.
- The candidate should still provide enough GHCN stations and current NWS
  observations for a defensible historical/current comparison.

These are hypotheses, not validated findings.

## Preliminary Storm Events observation

Evidence `W1-NOAA-SE-001` found 2,317 Oklahoma records in the requested hazard
families for 2024, covering all 14 requested event types and 150 distinct
county/zone identifiers. Of those records, 1,681 use zone geography and have no
begin coordinates, while 636 use county geography. This supports Oklahoma as a
candidate with hazard diversity, but it also proves that a county-only model
needs a documented forecast-zone crosswalk or spatial allocation rule.

This is evidence from one source and one year. It does not establish GHCN or
NWS coverage and is insufficient to accept the proposal.

## Alternatives

- **Kansas:** directly appears in the NOAA tutorial and has strong convective
  hazards, but the tutorial example is not evidence that all four sources or
  the desired compound-hazard mix are adequate.
- **Texas:** likely high record volume and broad hazard diversity, but its size,
  coastline, climate variation, and county count may create unnecessary scope.
- **Colorado:** offers varied elevation-driven hazards, but zone/county and
  station-to-region relationships may be more complex.

## Acceptance evidence

Before changing this ADR to `Accepted`, compare at least Oklahoma, Kansas, and
one of Texas or Colorado using:

1. Storm Events counts by year, event family, and county/zone;
2. active GHCN-Daily station coverage and missingness for required elements;
3. NWS observation-station coverage;
4. observed NWS Alerts geography and volume from the required two polls;
5. ability to map all four sources to the proposed regional unit;
6. estimated historical volume and runtime.

Both members must approve the decision. If the evidence favors another region
or aggregation unit, supersede this proposal rather than rewriting the result.

## Consequences if accepted

- Historical extraction filters the state but retains original geographic
  identifiers and coordinates.
- County-level index values require documented allocation rules for NWS zones
  and alert polygons.
- Stations need a reproducible station-to-county mapping.
- Missing coordinates or ambiguous zone/county mappings must be reported and
  may be quarantined rather than silently assigned.

