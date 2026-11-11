# Multi-Hazard Weather Impact Monitoring

Semester project for **Data Analysis Programming (2026-II)** at Universidad Distrital Francisco Jose de Caldas.

Team 9 will build an Oklahoma county-level monitoring system that integrates historical and periodically updated weather information and eventually produces a **Compound Hazard Index per region**. Oklahoma/counties, the 2010-2025 complete-year baseline, a rolling 24-hour current window, and a preliminary Workshop 1 indicator proposal are accepted team decisions. The indicator still requires empirical validation in Workshop 4.

## Current status

This repository is closing **Workshop 1**. Evidence and executed profiles exist
for all four assigned sources; Oklahoma/counties, the 2010-2025 complete-year
baseline and the rolling 24-hour current window are accepted team decisions.
Proposed implementation plans for Workshops 2-4 are available under `deliveries/`,
but no later-workshop implementation is claimed. The published Workshop 2-4 PDFs
contain a documented 2026-I public-opinion conflict that requires clarification.

## Start here

Read only these three files to begin:

1. [`WORK_BOARD.md`](WORK_BOARD.md) - current status, exact Kevin/Pablo ownership, next tasks, and working sequence.
2. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) - authoritative academic requirements, constraints, and unresolved decisions.
3. [`deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md`](deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md) - detailed Workshop 1 requirements and acceptance criteria.

Supporting material is indexed under [`docs/`](docs/) and the delivery history under [`deliveries/`](deliveries/). Contributors and coding agents must also follow [`AGENTS.md`](AGENTS.md).

## Repository areas

```text
config/                 Source and application configuration
dashboard/              Plotly Dash application
data/raw/               Raw landing zone (bulk data ignored by Git)
deliveries/              Per-milestone plans, change logs, evidence, and demo guides
docs/                    Plans, reports, decisions, and references
ingest.py                Required CLI contract stub for Workshop 1
notebooks/               Reproducible analysis and profiling notebooks
sql/                     Database schema and analytical views
src/                     Production ingestion package boundaries
tests/fixtures/          Tests and small recorded source fixtures
workshop_1/mapping.md     Preliminary canonical field mapping
workshop_1/samples/      Small immutable evidence samples for Workshop 1
```

The Workshop 1 scaffolds explicitly say when implementation belongs to a later
milestone. Their presence does not mean that Docker, ingestion, database,
orchestration, tests, or the dashboard have already been implemented.

The current CLI placeholder can be inspected without performing ingestion:

```powershell
python ingest.py --mode status
```

It returns `status: not_implemented` until the corresponding workshop work is
completed.

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
- [Workshop 2 specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf)
- [Workshop 3 specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_3.pdf)
- [Workshop 4 specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_4.pdf)

Professor-issued requirements outrank repository notes. When professor-issued
documents conflict across semester/domain, record the discrepancy, prioritize the
current semester/project contract, and request clarification instead of silently
choosing the newest file.
