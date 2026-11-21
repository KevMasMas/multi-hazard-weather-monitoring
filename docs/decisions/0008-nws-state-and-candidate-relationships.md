# ADR 0008 - NWS state, revisions and candidate relationships

Date: 2026-11-21. Status: implemented and technically verified; Kevin/Pablo
cross-review pending. No professor clarification or personal approval is inferred.

## Context

The project requires incremental NWS sources as well as weather-adapted Spark
Gold. Saved station captures are partial; treating them as complete seven-day
polls would hide a coverage gap. Source IDs, categorical alerts and daily weather
measurements cannot be treated as independent physical events by default.

## Decision

Use additive SQL 005 with separate replay/test/live namespaces, raw response
hashes, latest records, immutable observed revisions, per-poll sightings/rejects,
transactional query watermarks and per-station overlap/daily reconciliation.
Preserve applied historical migrations and datasets. Exclude replay/test from the
operational integrated view. Do not delete on absence. Enable network/scheduling
explicitly and leave the demonstrated DAG paused.

Use versioned polygon/time associations labelled intra-NWS and unconfirmed;
reuse W1 cross-product candidate context without calling it newly discovered
evidence. Full contract: `workshop_3/INCREMENTAL_CONTRACT.md`.

## Alternatives

Reusing the historical loader unchanged was rejected because its domain writer
assumes NOAA/GHCN. Treating every saved station page as a complete poll was
rejected because pagination evidence disproves completeness. Automatic matching
by county names or point proximity was rejected without a reviewed crosswalk.

## Consequences

Offline replay and bounded live validation are reproducible and distinguishable.
The successful empty active-alert query is valid evidence, not an invented event.
The integrated view serves later current analyses; frozen historical Gold keeps
its established population. County assignments, match evaluation, ongoing
operational activation and the conflicting dashboard input wording remain open.
