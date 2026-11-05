"""Build deterministic NWS Alert/KOKC candidate pairs for Workshop 1 review.

The output contains candidates, not confirmed same-event matches. An alert is
eligible only when its area text names Oklahoma County and a KOKC observation
timestamp falls inside the alert effective/expiry interval. The earliest
unused observation at or after the effective time is selected.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path


OKLAHOMA_COUNTY_PATTERN = re.compile(r"(?:^|;\s*)Oklahoma(?:, OK)?(?:;|$)", re.IGNORECASE)


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def measurement(properties: dict, name: str) -> tuple[object, object]:
    item = properties.get(name)
    if not isinstance(item, dict):
        return None, None
    return item.get("value"), item.get("unitCode")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alerts", type=Path, required=True)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    alerts = json.loads(args.alerts.read_text(encoding="utf-8"))["features"]
    observations = json.loads(args.observations.read_text(encoding="utf-8"))["features"]

    observation_rows = []
    for feature in observations:
        timestamp = parse_timestamp(feature.get("properties", {}).get("timestamp"))
        if timestamp is not None:
            observation_rows.append((timestamp, feature))
    observation_rows.sort(key=lambda item: (item[0], item[1].get("id", "")))

    eligible_alerts = []
    for feature in alerts:
        properties = feature.get("properties", {})
        effective = parse_timestamp(properties.get("effective"))
        expires = parse_timestamp(properties.get("expires"))
        area = properties.get("areaDesc") or ""
        if (
            properties.get("messageType") in {"Alert", "Update"}
            and effective is not None
            and expires is not None
            and effective <= expires
            and OKLAHOMA_COUNTY_PATTERN.search(area)
        ):
            eligible_alerts.append((effective, expires, feature))
    eligible_alerts.sort(key=lambda item: (item[0], item[2].get("id", "")))

    used_observation_ids: set[str] = set()
    pairs: list[dict[str, object]] = []
    for effective, expires, alert in eligible_alerts:
        candidate = next(
            (
                (timestamp, observation)
                for timestamp, observation in observation_rows
                if effective <= timestamp <= expires
                and observation.get("id") not in used_observation_ids
            ),
            None,
        )
        if candidate is None:
            continue

        observation_timestamp, observation = candidate
        used_observation_ids.add(observation["id"])
        alert_properties = alert["properties"]
        observation_properties = observation["properties"]
        temperature, temperature_unit = measurement(observation_properties, "temperature")
        wind_speed, wind_speed_unit = measurement(observation_properties, "windSpeed")
        wind_gust, wind_gust_unit = measurement(observation_properties, "windGust")
        precipitation, precipitation_unit = measurement(
            observation_properties, "precipitationLastHour"
        )
        visibility, visibility_unit = measurement(observation_properties, "visibility")

        pairs.append(
            {
                "candidate_pair_id": f"PAIR-{len(pairs) + 1:02d}",
                "alert_id": alert.get("id"),
                "alert_event": alert_properties.get("event"),
                "alert_message_type": alert_properties.get("messageType"),
                "alert_severity": alert_properties.get("severity"),
                "alert_effective": alert_properties.get("effective"),
                "alert_expires": alert_properties.get("expires"),
                "alert_area_desc": alert_properties.get("areaDesc"),
                "observation_id": observation.get("id"),
                "observation_timestamp": observation_properties.get("timestamp"),
                "seconds_after_alert_effective": int(
                    (observation_timestamp - effective).total_seconds()
                ),
                "station_id": observation_properties.get("stationId"),
                "text_description": observation_properties.get("textDescription"),
                "temperature_value": temperature,
                "temperature_unit": temperature_unit,
                "wind_speed_value": wind_speed,
                "wind_speed_unit": wind_speed_unit,
                "wind_gust_value": wind_gust,
                "wind_gust_unit": wind_gust_unit,
                "precipitation_last_hour_value": precipitation,
                "precipitation_last_hour_unit": precipitation_unit,
                "visibility_value": visibility,
                "visibility_unit": visibility_unit,
                "candidate_basis": "Oklahoma County named in alert area and KOKC timestamp falls inside alert interval",
                "match_status": "candidate_not_confirmed",
            }
        )
        if len(pairs) == args.limit:
            break

    if len(pairs) < args.limit:
        raise RuntimeError(
            f"Only {len(pairs)} defensible candidates found; requested {args.limit}."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)

    print(f"Wrote {len(pairs)} candidate pairs to {args.output}")


if __name__ == "__main__":
    main()
