# Change Log - Workshop 4

Append entries; do not silently rewrite historical observations.

## Entries

### [2026-11-10 America/Bogota] - Planning - Initial Workshop 4 plan

- **Objective:** create a Team 9 analytics/CHI/dashboard plan and separate reusable visualization guidance from incompatible sentiment-dashboard requirements.
- **Status:** [x] Plan created; [!] implementation and professor clarification remain pending.
- **Branch or commit:** planning performed on `workflow-1` at base `3304d4b`; Workshop 4 branch will start from the accepted Workshop 3 commit.
- **Requirements addressed:** baseline/current analysis, CHI, data health, dashboard, tests, reproducibility, report, ownership and merge planning.
- **Files created:** `deliveries/04-workshop-4/IMPLEMENTATION_PLAN.md` and this change log.
- **Files modified:** none by this entry outside cross-delivery planning documents.
- **Implementation or documentation completed:** assigned CHI/analytical views to Kevin and geography/dashboard/reporting to Pablo; defined one database-backed compatibility core and conditional two-app/Gold variants.
- **Decisions and rationale:** the 2026-II CHI monitoring objective remains primary. Visual quality and clean-clone standards are adopted; sentiment/keyword charts are rejected as Team 9 requirements.
- **Verification and exact result:** reviewed all seven pages of `Workshop_4.pdf`, rendered title/deliverable/submission pages, and compared them with the 2026-II project contract. No calculation, dashboard, screenshot or end-to-end result is claimed.
- **Evidence location:** `docs/reports/workshops-2-4-specification-review.md` and the implementation plan.
- **Errors found and correction:** the published PDF requires two Gold-Parquet sentiment dashboards, conflicting with the database-backed hazard dashboard. The plan records this as a clarification gate rather than choosing silently.
- **Risks or limitations:** analytical fields depend on Workshops 2-3; professor response may change application count/data-source architecture; dates and a Workshop 4 rubric are not stated.
- **Input received from:** Kevin requested implementation plans for every newly published workshop.
- **Handoff to:** both students for review after Workshop 3 contracts and CHI inputs are supported by implemented evidence.
- **Recovery or rollback:** revise the proposed plan after clarification while preserving this planning history.


### [2026-11-23 America/Bogota] - Input handoff only

- **Objective/status:** record verified W3 runtime inputs for future W4 planning; no W4 code or dashboard/CHI implementation.
- **Branch/commit:** local documentation on `feat/workshop-3-quality-gold`, base `6fa48a9`; no commit/push, approval or W4 branch creation.
- **Files/decision:** added the verified-input paragraph to this delivery plan and this log. Select the actual successful 650/607 Gold batch through `workshop_3/evidence/runtime_20261123/gold_samples.json`; preserve source/time/unit and narrative-coverage boundaries.
- **Verification/evidence:** revised Bronze/Silver/Gold succeeded; 54 Linux tests passed without skips; 20 delivered W3 artifact hashes and accepted historical record/revision hashes are unchanged. Actual receipts, logs and hashes are in the W3 runtime supplement. No new test/implementation execution is attributed to W4 itself.
- **Input/limits/handoff:** Kevin requested closing runtime gaps to continue with W4 and preserving the delivered document. Team review of W4 guide/input/CHI/county scope remains open; no personal approval or professor clarification inferred. Follow the current work board; selecting a new analytical scope must not overwrite submitted W3 artifacts.
