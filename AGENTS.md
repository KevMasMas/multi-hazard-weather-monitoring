# Repository Working Agreement

These instructions apply to contributors and coding agents working anywhere in this repository.

## Before changing files

1. Read `WORK_BOARD.md` for current ownership and next actions.
2. Read `PROJECT_CONTEXT.md` for stable requirements and constraints.
3. Read the active delivery plan and change log under `deliveries/`.
4. Check the current branch and working tree. Never discard another contributor's work.
5. Confirm whether the requested work is foundation work, a specific workshop, or final integration. Do not implement a future milestone implicitly.

## Sources of truth

Professor-issued project and workshop documents outrank repository notes. Record any new or conflicting requirement in `PROJECT_CONTEXT.md` and in a dated report. Do not promote course examples, suggested technologies, or assumptions into requirements without textual support.

## Language and evidence

- Write technical documentation, code, tests, configuration keys, commits, and pull-request descriptions in English.
- Never fabricate data, validation results, API behavior, row counts, performance, quality issues, event matches, or completed tests.
- Distinguish clearly among a requirement, an observed fact, a proposal, and an unresolved decision.
- Cite official source documentation and record license/attribution requirements.

## Data and external services

- Do not call a live weather service unless the current task explicitly authorizes source validation or ingestion.
- When live calls are authorized, use a descriptive User-Agent where required, respect limits and terms, cache responses, and avoid unnecessary repeat downloads.
- Preserve raw evidence unmodified. Put small, reviewable evidence in `workshop_1/samples/` or test fixtures; keep bulk downloads in ignored storage.
- Never commit credentials, tokens, private contact data, `.env`, database volumes, or generated bulk data.

## Architecture boundaries

- Keep notebooks for exploration, evidence, and analysis. Move reusable production logic into `src/` and test it.
- Keep source-specific extraction and normalization separate from canonical validation, storage, and analytics.
- Store configuration outside code. Environment-specific secrets belong in environment variables; document names only in `.env.example`.
- Preserve source provenance, UTC timestamps, WGS84 coordinates, severity units, raw identifiers, and content hashes.
- Design historical and incremental paths for idempotency and failure recovery. Advance a watermark only after a successful commit.
- Quarantine invalid records with reasons; do not silently drop them in production paths.
- The dashboard must ultimately read from the database or analytical views, not directly from live APIs.

## Git workflow

- Never develop directly on `main`.
- Use short-lived branches: `chore/...`, `docs/...`, `feat/...`, `fix/...`, `test/...`.
- Keep commits focused and use Conventional Commit prefixes such as `docs:`, `chore:`, `feat:`, `fix:`, and `test:`.
- Before integration, review the diff, run the checks relevant to the change, and summarize evidence in the pull request.
- Require the other team member to review material schema, contract, indicator, and architecture decisions.
- Do not rewrite shared branch history or force-push without explicit agreement.

## Planning and reporting

- `WORK_BOARD.md` is the only current assignment board. Do not create a second ownership table elsewhere.
- Keep semester-level, cross-delivery plans in `docs/plans/`.
- Give every graded or integration milestone a numbered folder in `deliveries/`.
- Every active delivery must have `IMPLEMENTATION_PLAN.md` and `CHANGE_LOG.md`. Add `DEMO_GUIDE.md` only when a reproducible demonstration exists.
- The implementation plan must define metadata, requirement interpretation, minimum demonstrable result, non-negotiable principles, P0/P1/out-of-scope work, owner/reviewer assignments, dependencies, acceptance criteria, and the merge gate.
- Every material contribution must add a dated change-log entry containing objective, status, branch/commit, files changed, decisions, exact verification results, evidence, errors/corrections, limitations, input received, handoff, and recovery instructions.
- Never check a plan item merely because code or prose exists. Link it to a change-log entry and evidence.
- Place evidence-backed cross-delivery reviews and status reports in `docs/reports/`.
- Place durable design decisions in `docs/decisions/` using a short ADR-style record: context, decision, alternatives, consequences, and status.
- At the end of material work, update the relevant plan/report with completed work, validation performed, known limitations, and next actions.
- A task is not complete merely because code exists; required tests, documentation, and reproducibility evidence must also exist.

## Collaboration standard

Each source and subsystem has a primary owner and a reviewer, but both students must understand and be able to defend every component. Avoid permanent knowledge silos: pair on contracts and schemas, cross-review code, and rotate demonstration responsibility.
