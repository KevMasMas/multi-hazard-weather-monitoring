# Change Log - Workshop 2

Append entries; do not silently rewrite historical observations.

## Entries

### [2026-11-16 America/Bogota] - Handoff - Workshop 1 acceptance audit

- **Objective/status:** inherit the evidence/status corrections without losing Workshop 2 planning; completed, no Workshop 2 implementation.
- **Branch/commit:** focused Workshop 1 audit commit `9b011dd`, fast-forwarded into `workflow-2`; no push or submission.
- **Files/requirements:** inherited acceptance A01-A09, current PDF/compliance review, offline quality/pair audit and evidence hashes; restored existing Workshop 2 plan/log/start-review and combined board updates.
- **Decision/rationale:** same-event interpretation remains open despite eight reproduced daily rows; previous workstream review is not new approval. Workshop 2 planning must not silently mark Workshop 1 accepted.
- **Verification/evidence:** Q1-Q6 assertions, nine captured checksums and eight-row reproduction pass. Thirteen-page PDF and matching ZIP verified. Three stashed planning files were compared byte-for-byte after newline normalization before this handoff annotation; no unmerged paths remain.
- **Errors/correction:** stash restoration conflicted in the board's adjacent status rows. Resolved by retaining the corrected Workshop 1/Pablo status and the existing Workshop 2 planning/next-action rows. The initial subprocess Git lookup was inaccessible; explicit bundled Git verified preservation successfully.
- **Limitations/input/handoff:** Kevin requested a Workshop 1 acceptance audit, not new personal approvals, source downloads or Workshop 2 implementation. A02 interpretation review, A03 same-event semantics, current student review and submission reference remain open.
- **Recovery:** focused commit is reversible; the previous planning content is preserved with its new handoff annotation. Do not discard the uncommitted Workshop 2 planning files.

### [2026-11-16 America/Bogota] - Handoff - Inherit the unsubmitted Workshop 1 architecture correction

- **Objective/status:** preserve Workshop 2 planning while correcting Workshop 1, then resume on `workflow-2`; completed without implementation.
- **Branch/commit:** Workshop 1 correction `009e628`, fast-forwarded into `workflow-2`; no remote push. Pre-existing planning changes restored from the task-specific stash without conflicts.
- **Requirements/files:** inherited ADR 0005, report/diagram and architecture documentation; updated this log, plan architecture reference and current board clarification.
- **Decision/rationale:** use the explicitly selected Airflow/medallion workflow; retain native raw evidence and canonical PostgreSQL storage with Silver Parquet exports. NLP/scraping discrepancy remains separate.
- **Verification/evidence:** focused commit exists on both local branches; revised PDF remains thirteen pages, rendered and inspected; ZIP inputs/assets match byte-for-byte. Samples and executed notebook unchanged. Final branch is `workflow-2` with prior planning files restored; no weather requests.
- **Errors/limitations:** no Git conflict; infrastructure and deployment configuration remain unimplemented and technical details still need review. No final student approval, push or submission is claimed.
- **Input/handoff:** Kevin requested the return to Workshop 1 and subsequent return to Workshop 2; continue W2-01/W2-02 using ADR 0005.
- **Recovery:** the focused architecture commit is reversible. Preserve the restored uncommitted Workshop 2 planning files before any later branch operations.

### [2026-11-16 America/Bogota] - W2-00 - Reverify requirements and start sequence

- **Objective:** explain the complete Workshop 2 path using current professor files and the actual repository state.
- **Status:** review and execution sequence recorded; implementation not started; specification discrepancy remains open.
- **Branch or commit:** `workflow-2`, created by Kevin; uncommitted planning changes only.
- **Requirements addressed:** architecture/historical milestone, source scope, academic precedence, conditional DAG/output requirements and demonstrable completion.
- **Files changed:** implementation plan metadata, `WORK_BOARD.md`, this log and `docs/reports/workshop-2-start-review-2026-11-16.md`.
- **Implementation or documentation completed:** recorded current source hashes, real practice operators/services, ordered offline-first build sequence, multi-year requirement and preflight limits.
- **Decisions and rationale:** reuse the practice's interval/raw/database/orchestration patterns; preserve native captures and quarantine invalid records. Treat TaskFlow/FileSensor/JSON layer wording explicitly rather than claiming the practice and PDF match.
- **Verification and exact result:** current public Workshop 2 and CourseProject hashes match local copies; all seven Workshop 2 pages read and historical milestone checked. Current Compose and all three practice DAGs inspected. Branch is `workflow-2`; tree was clean before documentation edits. `ingest.py` remains a stub. Docker CLI not found on session PATH; no daemon/container validation claimed.
- **Evidence location:** dated start review and prior specification-conflict review.
- **Errors found and correction:** web reader could not retrieve GitHub; direct read-only official GitHub access succeeded after network escalation. No weather endpoint was called.
- **Risks or limitations:** professor clarification, Docker access, architecture acceptance and multi-year coverage remain pending.
- **Input received from:** Kevin confirmed the new branch and requested the professor-aligned sequence to finish Workshop 2.
- **Handoff to:** start W2-01/W2-02 preflight and design; use saved samples for the first end-to-end path before bounded authorized acquisition.
- **Recovery or rollback:** revise the proposed sequence if corrected instructions arrive; retain this dated evidence and preserve Workshop 1 artifacts.

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
