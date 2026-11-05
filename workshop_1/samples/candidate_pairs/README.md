# NWS Alerts and KOKC Candidate Event Pairs

This directory contains five deterministic cross-source candidate pairs for
Workshop 1. They are candidates, not confirmed descriptions of the same
physical event.

Eligibility requires:

1. the NWS alert `areaDesc` explicitly names Oklahoma County;
2. the alert is an `Alert` or `Update` with a valid effective/expiry interval;
3. a KOKC observation timestamp falls inside that interval; and
4. each selected observation ID is used only once.

The selection uses the earliest unused KOKC observation at or after each alert
effective time. The method is intentionally deterministic and does not choose
the largest measurement after seeing the data.

`nws_alerts_kokc_candidate_pairs.csv` contains one Dense Fog Advisory pair,
one Special Weather Statement pair, and three Severe Thunderstorm Warning
alert/update pairs. Observed station descriptions include fog, light drizzle,
rain, and thunderstorms. Temporal/geographic overlap supports investigation,
but it does not prove causality or that KOKC represents every part of the alert
polygon.

The source NWS alert page is already registered as
`W1-NWS-ALERTS-PROFILE-001`. The KOKC pagination page and retrieval metadata are
preserved here as `W1-NWS-KOKC-PAGE-002`. Regenerate the derived CSV with
`scripts/workshop_1/build_candidate_event_pairs.py`.
