# Implementation Plan - Workshop 4

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** TBD - no submission date appears in the reviewed specification
- **Proposed working branch:** `feat/workshop-4-analytics-dashboard`
- **Proposed base:** accepted Workshop 3 delivery commit
- **Status:** proposed; implementation not started
- **Primary specification:** [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf), Semester 2026-II
- **Secondary/conflicting specification:** [Workshop_4.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_4.pdf), labeled Semester 2026-I
- **Conflict review:** `docs/reports/workshops-2-4-specification-review.md`

## 1. Requirement interpretation

The authoritative 2026-II contract assigns Workshop 4 to temporal/geographic
analysis, historical-versus-current comparison, the parameterized Compound Hazard
Index (CHI), and a Plotly Dash monitoring application for the accepted functional
user. The dashboard must read the database or analytical views and expose data
health as well as hazard conditions.

The new Workshop 4 PDF requires two independent dashboards that read Gold Parquet
only and display sentiment/keyword results. Its visualization-quality,
reproducibility and integration standards are reusable. Two apps, Gold-only input
and sentiment-specific charts are conditional because they conflict with Team 9's
database-backed monitoring contract.

## 2. Non-negotiable objective

Provide an evidence-backed Oklahoma county monitoring view that compares the
rolling 24-hour current window with the accepted 2010-2025 seasonal baseline,
computes a transparent CHI with incomplete-data handling, and lets the user trace
every score/chart to database records, parameters, source freshness and known
limitations. It is monitoring, not prediction.

## 3. Minimum demonstrable result

1. Historical analytical views produce county/month baseline distributions for
   the accepted flood, wind, heat, cold and winter components.
2. Current views compute the latest complete rolling 24-hour window at an hourly
   UTC boundary and retain the separate seven-day context.
3. A parameterized CHI returns component scores, interaction term, completeness,
   output score and status/reason for incomplete counties.
4. Tests reproduce known synthetic/fixture calculations and boundary cases; no
   expected score is invented from live evidence.
5. A Plotly Dash app at `localhost:8050` reads only database/approved analytical
   views and shows map, current/history comparison, trends, recent events and data
   health.
6. A fresh pipeline run updates the views/dashboard without code edits.
7. The report documents parameters, sensitivity, limitations, design decisions,
   user-story coverage and reproducibility evidence.

## 4. Non-negotiable principles

- Do not present CHI as a forecast, probability or official warning product.
- Keep raw source measurements/events and derived regional scores distinguishable.
- Version every baseline, component mapping, weight, threshold and formula.
- Never replace missing components with zero; expose completeness and reason.
- Use source units and explicit conversions before normalization.
- Separate county allocation confidence from hazard intensity.
- Dashboards never call live APIs and never compute from raw files directly.
- Prefer a few interpretable, labeled charts over many decorative charts.
- Every chart includes source, units/window and last-updated context.

## 5. Prioritized scope

### P0 - required compatibility core

- [ ] **W4-00 - Clarification gate:** confirm database/views versus Gold-only inputs and one monitoring app versus two apps.
- [ ] **W4-01 - Analytical contracts:** freeze component fields, units, region grain, temporal windows, seasonal comparison, minimum coverage and formula version.
- [ ] **W4-02 - Historical baselines:** implement county/month baseline distributions and completeness metrics from 2010-2025 qualifying data.
- [ ] **W4-03 - Current conditions:** implement rolling 24-hour and seven-day context views using successful incremental state and regional allocations.
- [ ] **W4-04 - CHI components:** implement flood, wind, heat, cold and winter normalization plus the accepted interaction/missingness rules.
- [ ] **W4-05 - CHI output:** persist or expose score, component values, weights, formula version, completeness and explanation per county/window.
- [ ] **W4-06 - Sensitivity/validation:** compare parameter variants and selected known historical periods; document what evidence supports or fails to support the index.
- [ ] **W4-07 - Data-health views:** expose source freshness, watermark age, run status, accepted/rejected counts, coverage and known source limitations.
- [ ] **W4-08 - Dashboard information architecture:** map functional-user stories to pages/sections, cards, map, trends, comparison, recent events and health panel.
- [ ] **W4-09 - Dashboard implementation:** build reusable data-access/layout/chart modules and the database-backed Dash application at `localhost:8050`.
- [ ] **W4-10 - Visualization quality:** apply accessible palette, units/labels, source annotations, responsive 1080p layout, meaningful hover/filter interactions and no horizontal scroll.
- [ ] **W4-11 - Tests:** add calculation, missingness, temporal-boundary, geographic-allocation, query and dashboard smoke tests.
- [ ] **W4-12 - Integration/reproducibility:** run historical then repeated incremental jobs, refresh analytics, launch dashboard and verify traceable updates from a clean clone.
- [ ] **W4-13 - Evidence/report:** produce English PDF, screenshots from real pipeline outputs, limitations, user-story traceability and exact commands/results.

### Conditional scope from the 2026-I PDF

- [ ] If two applications are confirmed, separate a technical governance/data-health app at `8050` and a functional-user hazard-story app at `8051` using shared modules.
- [ ] If Gold Parquet is confirmed, materialize weather-specific governance/analytical summaries while reconciling them with the relational source of truth.
- [ ] If a workshop tag is required, create `v1.0-workshop4` only after the validated delivery commit is accepted.
- [ ] Optional narrated walkthrough only after both required interfaces and evidence are stable.

### P1 - improvement after P0 is stable

- [ ] Add configurable county/component comparison and downloadable filtered data.
- [ ] Add CHI parameter/version selector for sensitivity explanation, not arbitrary score manipulation.
- [ ] Add cached analytical queries with explicit freshness invalidation.
- [ ] Perform a short usability review with the defined functional-user perspective.

### Out of scope

- Hazard prediction, forecast replacement or emergency instruction generation.
- Direct dashboard connections to NOAA/NWS APIs, raw JSON/CSV or notebook state.
- Sentiment, keywords, language or public-opinion storytelling.
- Hiding incomplete counties or silently imputing unsupported regional measurements.
- Final-project tag `v1.0-final`, which belongs to final integration.

## 6. Work allocation

### Kevin - analytical views and CHI workstream

**Reviewer:** Pablo

- [ ] Lead W4-01 analytical contracts and formula/version configuration.
- [ ] Implement historical/current analytical views and CHI components/output.
- [ ] Implement sensitivity calculations, calculation tests and query performance review.
- [ ] Expose reproducible data-access interfaces for dashboard consumers.
- [ ] Review dashboard values against database queries and report claims.

### Pablo - geography, dashboard and communication workstream

**Reviewer:** Kevin

- [ ] Lead county allocation/coverage presentation and data-health UX.
- [ ] Design W4-08 information architecture from the functional-user stories.
- [ ] Implement Dash layout, map, cards, charts, filters and responsive styling.
- [ ] Lead visual QA at 1080p, accessibility checks and screenshot evidence.
- [ ] Assemble the Workshop 4 report and demonstration narrative.

### Shared decisions and integration

- [ ] Accept W4-01 formula/component/coverage contract and W4-00 dashboard architecture.
- [ ] Select historical validation periods only from documented evidence.
- [ ] Review sensitivity results and limitations before presenting any CHI result.
- [ ] Pair on the clean-clone end-to-end run and final dashboard traceability audit.

## 7. Dependencies and handoffs

1. Workshop 2 provides historical canonical records, station/region model and
   validation/coverage metrics.
2. Workshop 3 provides current versions, source state, event groups and freshness.
3. W4-01 precedes all calculations and dashboard schemas.
4. W4-02/W4-03 precede CHI output; CHI/data-health contracts precede UI coding.
5. Calculation/query tests precede screenshot/report claims.
6. Workshop 4 hands final integration a validated dashboard, analytical contracts,
   reproducibility evidence and unresolved limitation list.

## 8. Acceptance criteria

- [ ] Baselines use only qualifying 2010-2025 records and report coverage/sample size.
- [ ] Current window boundaries are deterministic UTC intervals and seven-day context is separate.
- [ ] Every CHI row exposes components, parameters/version, completeness and source window.
- [ ] Missing components never become implicit zero and incomplete counties are visible.
- [ ] Calculation tests cover normal, threshold, missing, extreme and interaction cases.
- [ ] Historical/current queries reconcile with sampled canonical records.
- [ ] Dashboard reads only the accepted analytical source and makes no live requests.
- [ ] Map, trend, comparison, recent-event and data-health views satisfy user stories.
- [ ] All charts have readable titles, axes/units, legends when needed, sources and timestamps.
- [ ] Dashboard is usable at 1920x1080 without horizontal scrolling.
- [ ] Clean-clone instructions reproduce pipeline, analytics and dashboard launch.
- [ ] Screenshots/report use real validated outputs and state limitations clearly.

## 9. Merge gate

- [ ] The non-owner reviewed the complete diff and can explain formula and dashboard.
- [ ] Calculation, query, smoke and end-to-end tests passed with exact results recorded.
- [ ] Sensitivity/limitations review prevents predictive or unsupported claims.
- [ ] Dashboard data source and application count match professor clarification.
- [ ] Durable analytical/design decisions were promoted to `docs/decisions/`.
- [ ] No placeholder data, secrets, bulk outputs, local databases or unrelated files are tracked.
- [ ] Validated delivery commit/tag and report evidence are recorded.

## 10. Required contributor handoff

Every completed task must add a `CHANGE_LOG.md` entry with task ID, commit,
formula/query/UI verification, evidence path, screenshots only from real outputs,
known limitations and rollback instructions.
