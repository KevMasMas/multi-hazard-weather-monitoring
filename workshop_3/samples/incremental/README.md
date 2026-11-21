# Incremental output samples

- `normalized_preview.json`: selected normalized records from checksum-verified
  saved W1 replay; not a complete current-source response.
- `nws_candidates.json`: five saved-data polygon/time associations, all intra-NWS
  and `candidate_not_confirmed`. These are not independent physical events.
- `nws_alerts_live_excerpt.json` / `nws_station_observations_live_excerpt.json`:
  parsed excerpts (up to two original features) from the announced 2026-11-21
  live validation, with source URL/capture time/original response hash. These
  serialized excerpts are not untouched HTTP response bodies.
- `live_nws_candidates.json`: empty because no active Oklahoma alerts were
  returned. An empty source result is not a failed poll or proof no hazards exist.

Original live bytes remain under ignored `data/raw/`, with hashes/paths in
`workshop_3/evidence/incremental_live.json`. Captured live queries yielded zero
active alerts and 903 KOKC observations. Offline reproduction of the saved replay
uses `config/workshop3_nws_replay.json` and original W1 samples; it never substitutes
those old captures for current conditions or a complete station retention window.
Synthetic changed/fault fixtures exist only in `tests/test_incremental.py`.
