# ADR 0003 - Historical Baseline and Current-Condition Windows

- **Status:** Accepted
- **Date:** 2026-11-05
- **Decision owners:** Kevin Rincon and Pablo Garzon
- **Workshop gate:** W1-S01 / W1-D02

## Context

The project needs one reproducible historical interval and an explicit meaning
of “current conditions.” The intervals must support seasonal comparison,
annual historical partitions, NWS operational retention, and a semester-scale
runtime. The current calendar year, 2026, is incomplete and must not be mixed
into a complete-year baseline without a separate partial-period method.

## Decision

### Historical baseline

Use complete calendar years from `2010-01-01` through `2025-12-31`, inclusive.
This produces 16 annual partitions. Source rows outside the interval may be
retained in raw storage but do not enter the primary baseline.

The first seasonal comparison groups historical observations by calendar
month within each county/station. A day-of-year window may be evaluated later
as a sensitivity alternative, but it must not silently replace the accepted
monthly baseline.

### Current conditions

Define current conditions as the rolling 24-hour interval ending at an hourly
UTC calculation boundary:

```text
window_end_utc = current hourly boundary
window_start_utc = window_end_utc - 24 hours
```

Only records whose event/observation/effective intervals overlap that window
may contribute to current component evidence. Retrieval time is retained for
freshness but does not replace source event time.

### Operational context

Maintain a separate rolling seven-day operational context for source audit,
late-arrival recovery, recent trends, and alert/update chains. The seven-day
context is not automatically part of the 24-hour CHI and must be labeled
separately in the dashboard.

## Rationale

- Sixteen complete years provide repeated seasonal observations while keeping
  annual Storm Events and station partitions manageable.
- Starting in 2010 avoids making the project depend on much older and more
  heterogeneous coverage while exceeding the assignment's several-year
  expectation.
- Ending in 2025 prevents incomplete 2026 data from biasing a complete-year
  baseline.
- A rolling 24-hour window is understandable for emergency-management review
  and aligns with daily precipitation/temperature context.
- Hourly calculation is sufficient for the analytical product while source
  polling can remain independently configurable.
- Seven days matches the documented NWS station-observation recovery horizon
  already used in the source contract, without presenting a week as “now.”

## Consequences

- Historical ingestion partitions NOAA Storm Events and GHCN-Daily by year
  and records completeness per source/station/year.
- A station/year that fails the accepted completeness rule remains visible but
  cannot silently influence a baseline percentile.
- Current NWS records may arrive late or be revised; the 24-hour window is
  recomputed from versioned records rather than appended once.
- Historical Storm Events is contextual/outcome evidence and may not be
  available for the current 24 hours; absence of a recent Storm Events row is
  not evidence of no hazard.
- All stored timestamps use UTC where an instant exists. GHCN daily dates stay
  dates and are not converted into fabricated midnight instants.

## Alternatives considered

- **1950-present:** maximizes Storm Events history but has changing event-type
  coverage, unnecessary volume, and weak alignment with station completeness.
- **1996-2025:** includes broader Storm Events type coverage but increases
  runtime and coverage heterogeneity without being required for the semester.
- **Five-year baseline:** manageable but more sensitive to recent anomalies and
  provides fewer seasonal examples.
- **Seven days as current:** useful for context but too broad to describe
  immediate conditions and can dilute short compound episodes.
- **Calendar year 2026 in baseline:** rejected because it is incomplete.

## Review note

Acceptance was communicated in the joint Kevin/Pablo working session on
2026-11-05. Coverage is still measured empirically during historical
ingestion; this decision selects the intended interval, not a fabricated claim
that every station has complete data for all 16 years.
