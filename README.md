# Multi-Hazard Weather Impact Monitoring

Semester project for **Data Analysis Programming (2026-II)** at Universidad Distrital Francisco Jose de Caldas.

Team 9 will build a US regional monitoring system that integrates historical and periodically updated weather information and eventually produces a **Compound Hazard Index per region**. The exact US region, time windows, indicator formula, and validation strategy are intentionally undecided until the required source-validation work is completed.

## Current status

This repository is in **Workshop 1, with source validation and report drafting in progress**. Evidence and initial profiles exist for all four assigned sources. Denver and Oklahoma remain candidate locations, and the team has not chosen a common region. See the active delivery log and evidence register for exact scope and limitations.

## Start here

Read only these three files to begin:

1. [`WORK_BOARD.md`](WORK_BOARD.md) - current status, exact Kevin/Pablo ownership, next tasks, and working sequence.
2. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) - authoritative academic requirements, constraints, and unresolved decisions.
3. [`deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md`](deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md) - detailed Workshop 1 requirements and acceptance criteria.

Supporting material is indexed under [`docs/`](docs/) and the delivery history under [`deliveries/`](deliveries/). Contributors and coding agents must also follow [`AGENTS.md`](AGENTS.md).

## Planned repository areas

```text
config/                 Source and application configuration
dashboard/              Plotly Dash application
data/raw/               Raw landing zone (bulk data ignored by Git)
deliveries/              Per-milestone plans, change logs, evidence, and demo guides
docs/                    Plans, reports, decisions, and references
notebooks/               Reproducible analysis and profiling notebooks
sql/                     Database schema and analytical views
src/                     Production ingestion and processing package
tests/fixtures/          Tests and small recorded source fixtures
workshop_1/samples/      Small immutable evidence samples for Workshop 1
```

These directories are reserved now so later workshop work has a stable destination. Their presence does not mean their deliverables have been implemented.

## Working model

The repository follows the useful delivery pattern established in the team's HiLeS project:

1. `WORK_BOARD.md` answers what happens now and who owns it.
2. Each milestone gets one numbered folder under `deliveries/`.
3. The implementation plan defines required outputs and acceptance criteria.
4. The change log records what actually happened, including exact verification and limitations.
5. Durable architecture and data-contract decisions are promoted to `docs/decisions/`.

## Team

- Pablo Garzon - 20232020341
- Kevin Rincon - 20232020356

## Academic source of truth

- [Course materials](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming)
- [Course project specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf)
- [Team assignment](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/TeamsDistribution.pdf)
- [Workshop 1 specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_1.pdf)

When repository notes and a newer professor-issued document disagree, the newer professor-issued document wins and the discrepancy must be recorded.
