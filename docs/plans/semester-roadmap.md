# Semester Roadmap

Status: Workshop 1 evidence, profiles, accepted Oklahoma/time decisions and draft
contracts are committed through `3304d4b`. Final cross-review, a fresh locked
notebook rerun, the English PDF and submission commit remain open. Proposed plans
for Workshops 2-4 exist, but implementation has not started.

Specification note: the Workshop 2-4 PDFs published on 2026-11-05 are labeled
2026-I and describe a public-opinion/NLP project. The Team 9 plans prioritize the
2026-II natural-hazard course contract and isolate incompatible PDF items pending
professor clarification. See `docs/reports/workshops-2-4-specification-review.md`.

Each phase below is executed through a numbered folder in `deliveries/`. The roadmap provides semester direction; delivery plans contain the actionable checklist and evidence gate.

## Phase 0 - repository foundation

Goal: establish shared context and working conventions without querying sources or implementing Workshop 1.

- Review authoritative course material.
- Record requirements, constraints, and open decisions.
- Establish branch, review, planning, reporting, and decision-record workflows.
- Reserve the required repository areas and protect raw data and secrets through `.gitignore`.
- Agree on the two-person ownership proposal.

Exit evidence: reviewed foundation diff, agreed ownership, and an integration path for the initially empty repository.

Delivery record: `deliveries/00-project-foundation/`.

## Workshop 1 - definition, validation, and data contract

1. Agree on candidate US regions and explicit selection criteria.
2. Read official documentation and create a source-validation checklist for each assigned source.
3. Perform authorized, rate-conscious calls/downloads; preserve unmodified evidence.
4. Profile at least 200 records per source (or the complete source if smaller) in the required notebook.
5. Document nulls, ranges, duplicate identifiers, timestamps/time zones, coordinates, units, licensing, update behavior, revisions/deletions, and volume estimates.
6. Identify at least five concrete quality problems and investigate at least five candidate cross-source event pairs without forcing false matches.
7. Select and justify region, time window, definition of current conditions, regional unit, canonical mapping, domain tables, duplicate keys, watermarks, polling schedules, and failure recovery.
8. Draft the functional user, at least six prioritized user stories, index proposal, at least five risks, and architecture diagram.
9. Produce and review the report, executed notebook, samples, mapping, ER diagram, configuration draft, and repository setup.

Gate: every factual claim about a source is backed by official documentation or preserved empirical evidence.

Delivery record: `deliveries/01-workshop-1/`.

## Workshop 2 - architecture and historical ingestion

1. Convert approved Workshop 1 contracts into schemas and source adapters.
2. Create Docker Compose services and reproducible local setup.
3. Implement raw landing, historical partitioning/pagination, normalization, validation, missing-value policy, quarantine, audit runs, and idempotent storage.
4. Add unit and integration tests using recorded fixtures, not live services.
5. Demonstrate a clean historical run and a safe rerun.

Gate: two historical sources load reproducibly with traceable counts and no duplicates on rerun.

Proposed plan: `deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md`.

## Workshop 3 - incremental ingestion and integration

1. Implement NWS alerts and station-observation incremental adapters.
2. Implement per-source state, overlap windows, content hashes, retries/backoff, timeouts, and commit-safe watermarks.
3. Schedule incremental jobs and expose `status` information.
4. Implement within-source deduplication and evidence-based event grouping across spatial and temporal representations.
5. Test new, unchanged, revised, late, invalid, empty, and failed responses.

Gate: repeated incremental runs are idempotent and recovery does not skip or duplicate records.

Proposed plan: `deliveries/03-workshop-3/IMPLEMENTATION_PLAN.md`.

## Workshop 4 - analytics and dashboard

1. Create regional and seasonal historical baselines.
2. Implement temporal/geographic comparison and parameterized Compound Hazard Index components.
3. Run sensitivity and limitation analysis; do not claim prediction.
4. Build database-backed views and a Plotly Dash application with map, trends, current/historical comparison, indicator, recent events, and data-health status.
5. Test calculations and review dashboard usability with the functional-user goals.

Gate: every displayed value is traceable to database records and documented transformations.

Proposed plan: `deliveries/04-workshop-4/IMPLEMENTATION_PLAN.md`.

## Final integration

- Reproduce from a fresh clone using only the README.
- Run historical followed by several incremental executions and verify dashboard state.
- Prove idempotency and failure recovery with recorded evidence.
- Complete structured logging, tests, data dictionary, limitations, report, presentation, and live-demo script.
- Cross-train both team members on every subsystem.
- Tag the accepted final commit `v1.0-final`.
