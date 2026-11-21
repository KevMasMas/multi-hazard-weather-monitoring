# ADR 0009: Bounded narrative Silver and folder-based Gold

Date: 2026-11-21. Status: proposed for Kevin and Pablo review.

## Context

The team selected the supplied Workshop 3 PDF despite its 2026-I cover. It asks
for text quality, sentiment/keywords and a local Silver-folder-to-Gold PySpark
path. The existing weather pipeline had a frozen numerical input register and
no portable text Silver. The registered NOAA Oklahoma 2021 native CSV contains
actual event/episode narratives; later-year portable captures in this package
do not supply a complete text source.

## Decision

Preserve raw bytes. Select event narrative or episode fallback by source row,
record field provenance, clean transport noise for keywords, and score original
English text with VADER 3.3.2 (MIT). Treat labels as lexical tone only. Publish
a checked text Silver sidecar and mark other years unavailable. Enumerate every
numeric Parquet in `datalake_silver/`, requiring a baseline registry hash or
per-file sidecar. Reconcile revisions and publish governance/storytelling Parquet
in `datalake_gold/` with code/config/input hashes.

## Alternatives

- Reuse the frozen 13-file list: reproducible, but misses new accumulated Silver.
- Infer missing narratives from numeric records: unsupported by source evidence.
- Download later-year text now: outside the current source-call authorization and
  would change the captured source population.
- Treat VADER tone as hazard severity: semantically invalid for provider reports.

## Consequences

The current local Gold run includes text for 1,324 genuine NOAA 2021 rows and
explicitly unavailable later years. New files fail closed without checksum
evidence. The revised Airflow tasks need a fresh integration run; local PySpark
success does not establish DAG execution. Human contract review remains pending.

Source: [official VADER project and MIT license](https://github.com/cjhutto/vaderSentiment).
