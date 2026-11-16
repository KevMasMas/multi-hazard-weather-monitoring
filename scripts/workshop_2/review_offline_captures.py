"""Reproduce a bounded Bronze/parser review from Workshop 1 saved captures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from multi_hazard_weather_monitoring.sources.historical_samples import (  # noqa: E402
    parse_ghcn_daily,
    parse_noaa_storm_events,
)
from multi_hazard_weather_monitoring.storage.raw_landing import land_capture  # noqa: E402


CAPTURES = (
    ("noaa_storm_events", "sample_2024",
     "workshop_1/samples/noaa_storm_events/details_sample.csv", parse_noaa_storm_events),
    ("ghcn_daily", "USW00013967_2025",
     "workshop_1/samples/region_comparison/ghcn_okc_usw00013967_2025.csv", parse_ghcn_daily),
    ("ghcn_daily", "USW00013967_2026_overlap",
     "workshop_1/samples/region_comparison/ghcn_okc_usw00013967_2026_overlap.csv", parse_ghcn_daily),
)


def main() -> None:
    summaries = []
    for source, partition, relative, parser in CAPTURES:
        body = (ROOT / relative).read_bytes()
        capture = land_capture(body, source=source, partition=partition,
                               root=ROOT / "data/raw", content_type="text/csv",
                               origin=relative)
        records = list(parser(body))
        accepted = [r for r in records if "rejection_reason" not in r]
        rejected = [r for r in records if "rejection_reason" in r]
        keys = [r["source_key"] for r in accepted]
        if len(keys) != len(set(keys)):
            raise ValueError(f"duplicate_source_key:{source}:{partition}")
        summaries.append({
            "source": source,
            "partition": partition,
            "capture_sha256": capture["sha256"],
            "capture_bytes": capture["byte_count"],
            "origin": relative,
            "parsed_records": len(records),
            "accepted_records": len(accepted),
            "rejected_records": len(rejected),
            "distinct_source_keys": len(keys),
            "sample_keys": keys[:3],
            "output_scope": "offline_parser_review_not_airflow_or_silver",
        })
    output = ROOT / "workshop_2/samples/offline_capture_review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"captures": len(summaries), "summary": str(output),
                      "records": sum(s["parsed_records"] for s in summaries)}))


if __name__ == "__main__":
    main()
