# HiLes Delivery Workflow Review

## Review scope

Reviewed on 2026-11-03 from the local HiLes workspace at `D:\usuarios\Monitores\Downloads\HiLes\HiLeS_WEB`, including its root README, general schedule, delivery folders 1-7, implementation plans, change registers, demo guides, durable architecture/MQTT documentation, and recent Git history on `mqtt-pico`.

No HiLes source code or project-specific technical design was copied into this repository. The review focused only on collaboration and delivery-management practices.

## Strong practices adopted

### One folder per delivery

HiLes keeps dated milestone history under `entregas/`, separate from current architecture and operational guides in `docs/`. This project adopts the same boundary as:

- `deliveries/` for historical milestone execution;
- `docs/` for current, reusable knowledge and accepted decisions.

### A plan before implementation

The strongest HiLes plans define:

- a non-negotiable objective;
- requirement interpretation and minimum demonstrable result;
- P0, P1, and explicitly excluded work;
- ownership by person and dependencies among contributors;
- acceptance criteria and a merge gate.

The weather-project templates require these sections for every active milestone.

### Append-only evidence log

HiLes change registers capture more than a conventional changelog. Entries identify the owner, branch/commit, files, decisions, exact test results, physical/visual evidence, limitations, handoff, and recovery. This is especially valuable for preventing software-only tests from being presented as physical validation.

The adapted `CHANGE_LOG.md` template retains this distinction and adds a direct link to addressed requirements and evidence locations.

### Reproducible demo guide

HiLes demo guides separate preparation, ordered actions, expected results, evidence, contingencies, and a final checklist. This project will use a `DEMO_GUIDE.md` only after a milestone produces something runnable or presentable. Creating one prematurely would imply validation that does not exist.

### Honest state and limitations

Recent HiLes records explicitly distinguish automated software verification, broker/network tests, physical hardware validation, and pending work. The weather project adopts the same standard for documentation-only work, recorded fixtures, live-source observations, automated tests, and manual demonstrations.

## Adjustments made for this project

### Consistent naming

HiLes delivery filenames evolved over time. This project uses stable English names:

- `IMPLEMENTATION_PLAN.md`
- `CHANGE_LOG.md`
- `DEMO_GUIDE.md`
- optional milestone-specific evidence registers

English is required by the Data Analysis Programming course.

### Smaller historical documents

Some HiLes plans and change registers became very large because planning, implementation detail, current architecture, and status accumulated together. In this project:

- delivery documents preserve historical execution;
- accepted durable decisions move to `docs/decisions/`;
- current architecture and contracts live under `docs/`;
- the root README remains an operational entry point rather than a full history.

### Two-person review instead of many-person integration

HiLes divides work among several numbered people and an integration owner. Team 9 has two members, so every workstream uses one primary owner and the other member as reviewer. Scope, canonical model, source matching, and index decisions require both approvals.

### Evidence model adapted to data engineering

The weather project needs source-specific provenance beyond code test output. Workshop 1 therefore adds an evidence register for official documentation, request parameters, retrieval time, raw path, checksum, and incremental poll comparison.

## Resulting repository convention

The initial structure now includes:

- `deliveries/00-project-foundation/`: the current plan, change log, and review checklist;
- `deliveries/01-workshop-1/`: an unexecuted plan, empty evidence register, and planning-only change log;
- `deliveries/_templates/`: normalized templates for future workshops and the final project.

This reproduces the useful HiLes workflow without importing its domain, completed-state claims, oversized historical structure, or Spanish documentation convention.
