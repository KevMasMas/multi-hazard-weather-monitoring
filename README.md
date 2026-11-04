# Multi-Hazard Weather Impact Monitoring

Semester project for **Data Analysis Programming (2026-II)** at Universidad Distrital Francisco Jose de Caldas.

Team 9 will build a US regional monitoring system that integrates historical and periodically updated weather information and eventually produces a **Compound Hazard Index per region**. The exact US region, time windows, indicator formula, and validation strategy are intentionally undecided until the required source-validation work is completed.

## Current status

This repository is in the **project-foundation stage**. It contains project context, collaboration rules, an academic-material review, and a proposed semester roadmap. It does not yet implement Workshop 1, query weather APIs, or claim any data result.

Start with:

1. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) - authoritative project requirements and open decisions.
2. [`AGENTS.md`](AGENTS.md) - repository working rules for people and coding agents.
3. [`deliveries/README.md`](deliveries/README.md) - delivery workflow and document conventions.
4. [`deliveries/00-project-foundation/`](deliveries/00-project-foundation/) - current foundation delivery and review evidence.
5. [`deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md`](deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md) - planned Workshop 1 work; no source validation has started.
6. [`docs/reports/academic-material-review.md`](docs/reports/academic-material-review.md) - reviewed academic material and its relevance.
7. [`docs/reports/hiles-delivery-workflow-review.md`](docs/reports/hiles-delivery-workflow-review.md) - delivery practices adopted from HiLes and deliberate adjustments.
8. [`docs/plans/semester-roadmap.md`](docs/plans/semester-roadmap.md) - semester-level milestone plan.
9. [`docs/plans/team-work-plan.md`](docs/plans/team-work-plan.md) - initial two-person ownership proposal.

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

## Delivery workflow

The repository follows the useful delivery pattern established in the team's HiLeS project:

1. Each milestone gets one numbered folder under `deliveries/`.
2. Work starts from an implementation plan with scope, priorities, ownership, acceptance criteria, and exclusions.
3. Every material contribution is recorded in the delivery change log with exact tests, evidence, limitations, handoff, and recovery notes.
4. A demo guide is created only when the milestone has a runnable or presentable result.
5. Durable architecture and data-contract decisions are promoted to `docs/`; delivery folders remain the historical record of what was planned and completed.

## Team

- Pablo Garzon - 20232020341
- Kevin Rincon - 20232020356

## Academic source of truth

- [Course materials](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming)
- [Course project specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf)
- [Team assignment](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/TeamsDistribution.pdf)
- [Workshop 1 specification](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_1.pdf)

When repository notes and a newer professor-issued document disagree, the newer professor-issued document wins and the discrepancy must be recorded.
