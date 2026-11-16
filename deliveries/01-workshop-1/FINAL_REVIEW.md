# Workshop 1 Final Review

Current acceptance is defined by A01-A09 in `IMPLEMENTATION_PLAN.md`. Artifact
existence, verified calculations and student/professor acceptance are separate.
The current PDF exists; it is not a missing deliverable.

## Quality and pair audit - 2026-11-16

The offline submission audit verifies nine captured-input hashes and all six
record claims Q1-Q6. Q1-Q5 are the proposed five integration-quality concerns;
Q6 adds optional-field availability. No claim of six provider defects is made.
It also reproduces eight CSV comparisons: TMAX/TMIN on four days, with required
time/position/value-unit/identifier differences and raw extreme observation IDs.
The NWS daily side is derived, the day boundary assumed and sensor equivalence
unverified. Thus numerical/provenance checks pass, but acceptance as the guide's
five candidate same-real-world-event pairs is still open. No eight independent
weather episodes, confirmed matches or new approvals are asserted.

See `docs/reports/workshop-1-compliance-review.md` and
`workshop_1/samples/candidate_pairs/submission_evidence_audit.json`.

## Current correction review

The revised notebook executes 31/31 code cells with zero errors. Fourteen existing
CSV/GeoJSON hashes match the register. One subsequently authorized GHCN capture
for 2026-10-31 through 2026-11-05 supplies eight daily temperature candidates
with saved KOKC observations on four eligible days. The five old alert/KOKC rows
remain intra-NWS and are excluded from that count. These are candidate records,
not confirmed events or eight independent weather episodes. Daily-boundary and
station equivalence remain review assumptions; no PRCP comparison is claimed.
Report sources include literal excerpts/provenance, unit/time rules and PK/FK
Mermaid diagrams. The thirteen-page PDF has continuous excerpt pagination and
keeps model figures before ingestion contracts. See the latest log/register.

The unsubmitted report's architecture now selects Apache Airflow and explicitly
labels Bronze native raw evidence, Silver canonical PostgreSQL/PostGIS with
traceable Parquet exports, and planned Gold analytics (ADR 0005). This is a design
revision only; no source evidence or notebook output changed.

## Historical verification on 2026-11-11 (29-cell version)

The then-current source-profile notebook was executed with the existing project virtual
environment using:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks\01_source_profiling.ipynb
```

Execution completed successfully. All 29 code cells executed and no notebook error
outputs were stored. This verifies that historical notebook against preserved local
evidence. No live weather request was made. Dependency synchronization against
the lock was not performed because `uv` was unavailable; a fresh-clone environment
reproduction remains a separate check.

## Remaining submission gates

- Final technical review of mapping, quality examples and source contracts.
- Resolve the same-real-world-event interpretation of the derived daily comparisons; the row count alone does not close it.
- Student content review of the generated and visually inspected English PDF.
- Fresh-clone reproduction and final artifact/secret review.
- Student review and submission commit/reference recording.

Assistant verification must not be presented as personal approval by either
student. Candidate pairs remain unconfirmed and historical volume screens remain
estimates.
