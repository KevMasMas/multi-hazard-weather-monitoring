# ADR 0002 - Preliminary Compound Hazard Index

- **Status:** Accepted as the Workshop 1 preliminary proposal; empirical validation pending
- **Date:** 2026-11-05
- **Owner:** Kevin Rincon
- **Reviewer:** Pablo Garzon
- **Decision gate:** W1-D02

## Context

The project must produce a parameterized Compound Hazard Index (CHI) per
region and compare current conditions with a historical baseline. Workshop 1
requires a proposal, not an implemented or validated indicator. The accepted
scope is Oklahoma with counties as analytical regions.

The assigned sources have different roles:

- NOAA Storm Events provides historical event occurrence, type, impact, and
  reported severity context;
- GHCN-Daily provides a long daily measurement baseline;
- NWS Alerts provides current/recent authoritative hazard messages and their
  severity, urgency, certainty, and affected geography;
- NWS station observations provide recent measurements and freshness/QC
  information.

The CHI is a monitoring summary. It is not a forecast, an official warning,
or a replacement for its component evidence.

## Proposed output grain

One CHI observation is identified by:

```text
(region_id, window_start_utc, window_end_utc, index_version)
```

The region is a county. The current window is the rolling 24 hours calculated
at an hourly UTC boundary, with a separate seven-day operational context as
specified in ADR 0003.

Every result must include the total score, component scores, input coverage,
source freshness, active limitations, parameter version, and raw-evidence
references.

## Hazard components

The first proposal uses five components, each normalized to `[0, 1]`:

| Code | Hazard family | Historical context | Current evidence |
| --- | --- | --- | --- |
| `flood` | Heavy rain, flash flood, flood | Storm Events frequency/impact; GHCN precipitation distribution | NWS flood/rain alerts and recent precipitation observations where available |
| `wind` | Thunderstorm wind, high wind, strong wind | Storm Events frequency/magnitude | NWS wind/severe-thunderstorm alerts and station wind/gust observations |
| `heat` | Heat and excessive heat | Storm Events frequency/impact; seasonal GHCN maximum-temperature distribution | NWS heat alerts and station temperature observations |
| `cold` | Cold/wind chill and extreme cold/wind chill | Storm Events frequency/impact; seasonal GHCN minimum-temperature distribution | NWS cold alerts and station temperature/wind observations |
| `winter` | Heavy snow, ice storm, winter storm, winter weather | Storm Events frequency/impact; relevant GHCN measurements when available | NWS winter alerts and supported station measurements |

No component may silently infer an unavailable measurement. Final source-field
mappings and units require review before implementation.

## Normalization proposal

Continuous measurements should be compared with an empirical seasonal
baseline for the same station or region. Candidate normalization uses an
empirical percentile `p` from complete historical years:

- upper-tail hazard severity: `s = p`;
- lower-tail cold severity: `s = 1 - p`;
- neutral/non-hazard ranges may be mapped to zero only through a documented
  threshold and sensitivity analysis.

Calendar month or day-of-year windows should be tested to avoid comparing a
summer temperature directly with an annual distribution. Extreme values may
be winsorized only in derived calculations; original values and units remain
unchanged.

Categorical NWS alert severity can provide an additional component signal, but
the mapping from `Minor`, `Moderate`, `Severe`, `Extreme`, and `Unknown` to
numeric values is not accepted yet. `Unknown` must remain missing/unknown, not
zero. Alert urgency and certainty must be shown separately unless review
justifies including them without double counting.

For each hazard family, multiple valid signals may be combined using a
parameterized rule such as a maximum or weighted mean. The rule must be fixed
in an index-version configuration and tested for duplicate-source inflation.

## Preliminary aggregation formula

Let `s_h` be the normalized score for hazard family `h`, and let non-negative
weights `w_h` sum to one. The initial review configuration uses equal weights
of `0.20`; these are neutral starting parameters, not validated importance.

The weighted base is:

```text
B = sum(w_h * s_h)
```

Let `P` be the strongest simultaneous interaction among reviewed hazard pairs:

```text
P = max(min(s_i, s_j)) for each configured pair (i, j)
```

Candidate interaction pairs include flood-wind, cold-wind, winter-wind, and
heat-wind. The pair list requires domain review and is configuration, not
hard-coded logic.

With a candidate interaction coefficient `beta = 0.20`:

```text
CHI = 100 * min(1, B + beta * P)
```

This keeps the result on `[0, 100]`, preserves the component contribution, and
adds a bounded bonus only when at least two configured hazards are elevated.
No Low/Medium/High interpretation bands are proposed until the score
distribution and sensitivity are evaluated.

## Missingness, freshness, and coverage

Missing data is not evidence of zero hazard.

- A component may equal zero only when its required sources completed
  successfully and the accepted mapping establishes an observed non-hazard
  state.
- If a required source failed, is stale, has ambiguous geography, or contains
  an unsupported value/unit, the affected component is `null` with a reason.
- The total CHI is suppressed when any required component cannot be evaluated;
  the dashboard shows the component vector and an `incomplete` status instead.
- A separate coverage/health record reports expected sources, successful and
  fresh sources, station coverage, rejected records, and crosswalk confidence.
- Coverage is never multiplied into the CHI because doing so would make a data
  outage look safer.

This strict Workshop 1 proposal may be relaxed only after the team defines a
defensible partial-score policy and communicates it visibly.

## Historical/current comparison

The dashboard should show the CHI beside:

- each component score and source evidence;
- its percentile relative to the same county and season in the selected
  historical baseline;
- recent score trajectory;
- source freshness and data-health status;
- historical event counts/impacts for context, without implying causation.

The baseline is 2010-2025 complete calendar years. Station/year eligibility
still depends on measured completeness under ADR 0004.

## Validation plan for Workshop 4

1. Freeze an index configuration and retain all parameters with a version.
2. Use complete historical years; separate calibration and held-out periods.
3. Compare component/CHI distributions on documented Storm Events dates with
   seasonally matched non-event dates where the historical measurements allow
   reconstruction.
4. Test sensitivity to weights, `beta`, percentile window, station aggregation,
   geographic crosswalk, and missingness rules.
5. Report rank stability, coverage, false-positive/false-negative examples,
   and limitations; do not select parameters solely to maximize one metric.
6. Review results with the professor/domain stakeholder before assigning
   interpretation bands.

The current NWS endpoints do not provide a long historical alert/observation
archive through the assigned access path. Therefore, a full retrospective
reconstruction of the current-source portion may be impossible; that
limitation must remain explicit.

## Alternatives considered

- **Simple count of active hazards:** easy to explain but ignores severity and
  historical context.
- **Maximum component only:** highlights the most severe condition but is not a
  compound measure.
- **Unbounded sum:** rewards multiple hazards but can exceed a stable scale and
  overcount correlated source signals.
- **Multiply score by data coverage:** rejected because outages would lower the
  apparent hazard level.
- **Machine-learned weights in Workshop 1:** rejected because current evidence
  is insufficient and would create unsupported precision.

## Remaining implementation gate

Both members accepted this design as the Workshop 1 preliminary proposal on
2026-11-05. Before Workshop 4 implementation becomes final, both must approve:

1. regional/time grain and baseline years;
2. component event/field mappings and units;
3. alert categorical mapping;
4. station-to-county and zone/polygon allocation;
5. component combination, weights, interactions, and missingness rules;
6. validation and communication plan.

Implementation belongs to Workshop 4. Workshop 1 only records the proposal.
