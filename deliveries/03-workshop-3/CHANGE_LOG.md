# Change Log - Workshop 3

Append entries; do not silently rewrite historical observations.

## Entries

### [2026-11-10 America/Bogota] - Planning - Initial Workshop 3 plan

- **Objective:** create a Team 9 incremental-ingestion and event-integration plan while isolating the incompatible PySpark/NLP wording in the published Workshop 3 PDF.
- **Status:** [x] Plan created; [!] implementation and professor clarification remain pending.
- **Branch or commit:** planning performed on `workflow-1` at base `3304d4b`; Workshop 3 branch will start from the accepted Workshop 2 commit.
- **Requirements addressed:** state, NWS adapters, scheduling, change detection, deduplication, recovery, event identification, tests, evidence and ownership planning.
- **Files created:** `deliveries/03-workshop-3/IMPLEMENTATION_PLAN.md` and this change log.
- **Files modified:** none by this entry outside cross-delivery planning documents.
- **Implementation or documentation completed:** assigned Alerts/change matching to Kevin and station polling/orchestration to Pablo; defined fixture scenarios and conditional weather-specific Gold/PySpark adaptation.
- **Decisions and rationale:** the 2026-II incremental milestone is the compatibility core. The 2026-I Gold/NLP requirements remain conditional instead of displacing watermarks and integration.
- **Verification and exact result:** reviewed all seven pages of `Workshop_3.pdf`, rendered title/deliverable/submission pages, and compared them with the 2026-II project contract. No DAG, PySpark job, API call or test run is claimed.
- **Evidence location:** `docs/reports/workshops-2-4-specification-review.md` and the implementation plan.
- **Errors found and correction:** sentiment trends, keywords and language KPIs do not apply to Team 9; the plan replaces them only conditionally with weather-specific governance/analytical summaries.
- **Risks or limitations:** exact Gold/PySpark obligations, schedule and evaluation rubric are unresolved. Workshop 3 depends on accepted Workshop 2 storage/transaction contracts.
- **Input received from:** Kevin requested implementation plans for every newly published workshop.
- **Handoff to:** both students for review after Workshop 2 design is accepted; do not start implementation early.
- **Recovery or rollback:** update the proposed plan after professor clarification without rewriting this planning history.
