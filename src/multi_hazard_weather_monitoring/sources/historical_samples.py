"""Offline parsers for the two historical Workshop 1 CSV captures.

These parsers do not fetch data or modify the captured bytes. They expose
source-specific rows for a later transactional storage layer.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from datetime import date, datetime, timedelta, timezone
from typing import Iterator


def _rows(body: bytes) -> Iterator[tuple[int, dict[str, str]]]:
    text = body.decode("utf-8-sig")
    yield from enumerate(csv.DictReader(io.StringIO(text, newline="")), start=2)


def _hash(row: dict[str, str]) -> str:
    encoded = json.dumps(row, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _number(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("nonfinite_number")
    return number


def parse_noaa_storm_events(body: bytes) -> Iterator[dict]:
    """Yield source events, retaining missing point coordinates and raw fields."""
    for line, row in _rows(body):
        try:
            event_id = (row.get("EVENT_ID") or "").strip()
            if not event_id:
                raise ValueError("missing_event_id")
            event_type = (row.get("EVENT_TYPE") or "").strip()
            if not event_type:
                raise ValueError("missing_event_type")
            zone = (row.get("CZ_TIMEZONE") or "").strip()
            if zone != "CST-6":
                raise ValueError("unsupported_source_timezone")
            local = datetime.strptime(row["BEGIN_DATE_TIME"], "%d-%b-%y %H:%M:%S")
            utc = local.replace(tzinfo=timezone(timedelta(hours=-6))).astimezone(timezone.utc)
            lat, lon = _number(row.get("BEGIN_LAT")), _number(row.get("BEGIN_LON"))
            if (lat is None) != (lon is None):
                raise ValueError("incomplete_coordinates")
            if lat is not None and (not -90 <= lat <= 90 or not -180 <= lon <= 180):
                raise ValueError("coordinates_out_of_range")
            magnitude = _number(row.get("MAGNITUDE"))
            magnitude_type = (row.get("MAGNITUDE_TYPE") or "").strip() or None
            wind_types = {"High Wind", "Thunderstorm Wind", "Strong Wind"}
            yield {
                "source": "noaa_storm_events",
                "source_key": event_id,
                "observed_at_utc": utc.isoformat(),
                "observed_date": None,
                "event_type": event_type,
                "latitude": lat,
                "longitude": lon,
                "severity_value": magnitude,
                "severity_unit": "kn" if magnitude is not None and event_type in wind_types else None,
                "magnitude_type": magnitude_type,
                "geography_reference": f"{row.get('CZ_TYPE', '')}/{row.get('CZ_FIPS', '')}/{row.get('CZ_NAME', '')}",
                "source_content_sha256": _hash(row),
                "source_line": line,
                "raw_fields": row,
            }
        except (KeyError, TypeError, ValueError) as exc:
            yield {"source": "noaa_storm_events", "source_line": line,
                   "rejection_reason": str(exc), "raw_fields": row}


def parse_ghcn_daily(body: bytes) -> Iterator[dict]:
    """Yield one measurement per station/date/element without inventing a time."""
    for line, row in _rows(body):
        for element, unit in (("PRCP", "mm"), ("TMAX", "degC"), ("TMIN", "degC")):
            value = row.get(element)
            if value is None or not value.strip():
                continue  # An absent optional element is not a source record.
            try:
                station = (row.get("STATION") or "").strip()
                if not station:
                    raise ValueError("missing_station_id")
                day = date.fromisoformat(row["DATE"])
                number = _number(value)
                lat, lon = _number(row.get("LATITUDE")), _number(row.get("LONGITUDE"))
                if (lat is None) != (lon is None):
                    raise ValueError("incomplete_coordinates")
                if lat is not None and (not -90 <= lat <= 90 or not -180 <= lon <= 180):
                    raise ValueError("coordinates_out_of_range")
                yield {
                    "source": "ghcn_daily",
                    "source_key": f"{station}/{day.isoformat()}/{element}",
                    "observed_at_utc": None,
                    "observed_date": day.isoformat(),
                    "event_type": element,
                    "latitude": lat,
                    "longitude": lon,
                    "severity_value": number,
                    "severity_unit": unit,
                    "quality_attributes": row.get(f"{element}_ATTRIBUTES") or None,
                    "source_content_sha256": _hash(row),
                    "source_line": line,
                    "raw_fields": row,
                }
            except (KeyError, TypeError, ValueError) as exc:
                yield {"source": "ghcn_daily", "source_line": line,
                       "element": element, "rejection_reason": str(exc),
                       "raw_fields": row}
