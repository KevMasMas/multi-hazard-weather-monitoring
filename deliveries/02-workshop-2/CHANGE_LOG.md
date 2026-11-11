# Change Log - Workshop 2

Append entries; do not silently rewrite historical observations.

## Entries

### [2026-11-10 America/Bogota] - Planning - Initial Workshop 2 plan

- **Objective:** translate the 2026-II historical-ingestion milestone and the conflicting Workshop 2 PDF into a reviewable, evidence-gated Team 9 plan.
- **Status:** [x] Plan created; [!] implementation has not started and specification clarification is pending.
- **Branch or commit:** planning performed on `workflow-1` at base `3304d4b`; no implementation commit created.
- **Requirements addressed:** planning metadata, requirement interpretation, minimum demonstration, P0/P1/out-of-scope work, ownership, dependencies, acceptance and merge gate.
- **Files created:** `deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md`, this change log, `docs/reports/workshops-2-4-specification-review.md`, and `docs/reports/project-status-2026-11-10.md`.
- **Files modified:** `PROJECT_CONTEXT.md`, `WORK_BOARD.md`, `README.md`, `docs/plans/semester-roadmap.md`, `docs/reports/academic-material-review.md`, `docs/references/academic-materials.md`, and `deliveries/README.md`; Workshop 3-4 plans maintain their own planning entries.
- **Implementation or documentation completed:** assigned NOAA/database/CLI leadership to Kevin and GHCN/orchestration/evidence leadership to Pablo; separated safe historical/database work from conditional Bronze/Silver requirements.
- **Decisions and rationale:** the 2026-II natural-hazard contract takes precedence until the professor resolves the 2026-I public-opinion wording. Airflow is a provisional compatibility choice, not yet an accepted ADR.
- **Verification and exact result:** reviewed all seven pages of `Workshop_2.pdf`, its rendered title/deliverable/submission pages, the 2026-II course contract, Team 9 context and current repository state. Structural validation found 10/10 required plan sections in each plan, 13 Workshop 2, 12 Workshop 3 and 14 Workshop 4 P0 task IDs, zero pre-checked implementation tasks, 15/15 required change-log fields in each new log, and 8/8 required planning files present. `git diff --check` passed with only informational CRLF-to-LF warnings. No code, service or ingestion execution is claimed.
- **Evidence location:** `docs/reports/workshops-2-4-specification-review.md` and the implementation plan.
- **Errors found and correction:** the published PDF refers to API plus scraping, NLP and forced Bronze JSON, which do not describe Team 9. These were moved to incompatible/conditional scope instead of being copied as requirements. The first PowerShell change-log checker used an ambiguous variable interpolation before `:` and failed to parse; the check was corrected with formatted strings and then passed for all three logs.
- **Risks or limitations:** target date and professor clarification are absent; exact infrastructure may change after clarification and architecture review.
- **Input received from:** Kevin requested implementation plans for every newly published workshop.
- **Handoff to:** both students to review the plan and send the clarification questions; Workshop 2 implementation starts only after the Workshop 1 closure gate.
- **Recovery or rollback:** revise the proposed plan and retain this entry if the professor supplies a corrected 2026-II PDF; do not rewrite this historical observation.
