# Implementation Plan - Project Foundation

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Prepared:** 2026-11-03
- **Working branch:** `chore/project-foundation`
- **Base branch/commit:** remote `main` has no commits
- **Status:** under team review; files are staged but uncommitted
- **Official specifications:** `CourseProject.pdf`, `TeamsDistribution.pdf`, and `Workshop_1.pdf`

## 1. Requirement interpretation

Before source validation or pipeline work, the team needs a repository that preserves official requirements, separates semester knowledge from delivery history, assigns two-person ownership, and prevents unverified claims. Because the remote repository is empty, this delivery also defines the initial Git integration path.

## 2. Non-negotiable objective

Leave a reviewable project foundation that both students can use throughout the semester without implementing Workshop 1, calling weather APIs, or deciding evidence-dependent architecture prematurely.

## 3. Minimum demonstrable result

From the repository root, a new contributor can identify:

1. The assigned hazard, team, sources, scope constraints, and common technical contract.
2. Which academic documents are authoritative and which materials are examples.
3. The planned semester phases and two-person ownership.
4. The repository and delivery-document conventions.
5. What remains undecided and what work is explicitly prohibited at this stage.

## 4. Non-negotiable principles

- Preserve existing local academic material outside the repository.
- Keep technical repository documentation in English.
- Do not query weather APIs or create source samples.
- Do not mark Workshop 1 requirements as validated.
- Do not invent region, index formula, results, volumes, quality issues, or event matches.
- Do not develop directly on `main`.
- Do not create a commit with an unconfirmed Git identity.

## 5. Prioritized scope

### P0 - required foundation

- [x] Inspect the local academic files and the professor repository.
- [x] Inspect the team repository before modification and confirm that it is empty.
- [x] Record authoritative requirements, constraints, and open decisions in `PROJECT_CONTEXT.md`.
- [x] Define contributor and coding-agent rules in `AGENTS.md`.
- [x] Review the slides, notebooks, and Airflow practice by workshop relevance.
- [x] Define the semester roadmap and initial two-person work allocation.
- [x] Reserve the professor-required repository areas without adding functional code.
- [x] Protect secrets and bulk raw data through `.gitignore` and `.env.example`.
- [x] Reproduce the HiLes delivery pattern with per-delivery plans, change logs, evidence, and conditional demo guides.
- [x] Prepare an actionable Workshop 1 plan without executing it.

Evidence for these items is recorded in `CHANGE_LOG.md` and `REVIEW_CHECKLIST.md`.

### P1 - after team review

- [ ] Confirm the proposed ownership split with both students.
- [ ] Confirm the Git author identity for the initial commit.
- [ ] Decide how to establish the first `main` commit and review the foundation branch.
- [ ] Push the accepted branch and integrate only after review.

### Out of scope

- Workshop 1 source queries, samples, profiling, mappings, ER model, report, or validation claims.
- Pipeline code, database schema, Docker services, Airflow DAGs, dashboard, or index implementation.
- Selection of the final US region or Compound Hazard Index formula.

## 6. Work allocation

### Kevin - repository foundation owner

**Reviewer:** Pablo

- [ ] Review the staged repository structure and Git workflow.
- [ ] Confirm or correct names, identifiers, and Git author identity.
- [ ] Review `PROJECT_CONTEXT.md` and the delivery workflow.
- [ ] Present the foundation diff to Pablo before integration.

### Pablo - academic traceability reviewer

**Reviewer:** Kevin

- [ ] Verify the academic review against professor-issued documents.
- [ ] Confirm the proposed source ownership and collaboration rhythm.
- [ ] Challenge any item that is a proposal but is written as a requirement.
- [ ] Approve or request changes to the foundation delivery.

### Shared decisions

- [ ] Approve the source ownership split.
- [ ] Approve the delivery-document convention.
- [ ] Approve the initial Git integration procedure.

## 7. Dependencies and handoffs

The foundation must be accepted before Workshop 1 begins. The handoff is the accepted repository structure plus `deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md` with all items still pending.

## 8. Acceptance criteria

- [x] The academic review identifies requirements versus teaching examples.
- [x] All required source and workshop constraints are recorded without validation claims.
- [x] The repository has a clear location for production code, raw data, tests, notebooks, documentation, and workshop evidence.
- [x] The branch is independent from `main` and no commit or push was made automatically.
- [x] `git diff --cached --check` reports no whitespace errors before the HiLes-inspired additions.
- [ ] Both team members review the final staged diff.
- [ ] The correct Git identity is configured.

## 9. Merge gate

- [ ] Kevin and Pablo approve the documentation and ownership split.
- [ ] The final staged diff passes `git diff --cached --check`.
- [ ] No API response, credential, bulk data, or fabricated result is tracked.
- [ ] The first commit uses an approved author identity and an English Conventional Commit message.
- [ ] The initial `main` integration approach is agreed explicitly because the remote has no base commit.

## 10. Required handoff

The reviewer must record approval or requested changes in `CHANGE_LOG.md`. Workshop 1 remains blocked by planning, not by technical failure, until the team deliberately starts it.
