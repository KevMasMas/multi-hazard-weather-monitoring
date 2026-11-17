"""Initial source-aware canonical checks for historical records."""

from __future__ import annotations

import math
import re
from datetime import date, datetime, timedelta


def rejection_reason(record: dict) -> str | None:
    """Return a stable reason code, keeping the original record for quarantine."""
    if "rejection_reason" in record:
        return record["rejection_reason"]
    if not isinstance(record.get('source_key'), str) or not record['source_key'].strip():
        return 'missing_source_key'
    if not isinstance(record.get('event_type'), str) or not record['event_type'].strip():
        return 'missing_event_type'
    if not isinstance(record.get('source_line'), int) or record['source_line'] < 2:
        return 'invalid_source_line'
    if not re.fullmatch(r'[0-9a-f]{64}', record.get('source_content_sha256') or ''):
        return 'invalid_content_hash'
    instant, day = record.get('observed_at_utc'), record.get('observed_date')
    if (instant is None) == (day is None):
        return 'invalid_time_grain'
    try:
        if instant is not None:
            parsed = datetime.fromisoformat(instant)
            if parsed.utcoffset() != timedelta(0):
                return 'timestamp_not_utc'
        else:
            date.fromisoformat(day)
    except (TypeError, ValueError):
        return 'invalid_timestamp_or_date'
    lat, lon = record.get('latitude'), record.get('longitude')
    if (lat is None) != (lon is None):
        return 'incomplete_coordinates'
    if lat is not None:
        if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in [lat, lon]):
            return 'invalid_coordinates'
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return 'coordinates_out_of_range'
    value = record.get("severity_value")
    if value is not None and (not isinstance(value, (int, float)) or not math.isfinite(value)):
        return "invalid_numeric_value"
    if record.get("source") == "ghcn_daily":
        element = record.get("event_type")
        if instant is not None:
            return 'daily_measurement_requires_date'
        if value is None:
            return 'missing_measurement_value'
        expected_units = {'PRCP': 'mm', 'TMAX': 'degC', 'TMIN': 'degC'}
        if element in expected_units and record.get('severity_unit') != expected_units[element]:
            return 'unexpected_measurement_unit'
        if element == "PRCP" and value is not None and value < 0:
            return "negative_precipitation"
        if element in {"TMAX", "TMIN"} and value is not None and value < -273.15:
            return "below_absolute_zero"
        if element not in {"PRCP", "TMAX", "TMIN"}:
            return "unsupported_element"
    elif record.get("source") == "noaa_storm_events":
        if day is not None:
            return 'storm_event_requires_instant'
        if value is not None and value < 0:
            return "negative_magnitude"
        if value is not None and not record.get("severity_unit"):
            return "unknown_magnitude_unit"
    else:
        return "unknown_source"
    return None
