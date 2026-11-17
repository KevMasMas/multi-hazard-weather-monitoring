"""Initial source-aware canonical checks for historical records."""

from __future__ import annotations

import math


def rejection_reason(record: dict) -> str | None:
    """Return a stable reason code, keeping the original record for quarantine."""
    if "rejection_reason" in record:
        return record["rejection_reason"]
    value = record.get("severity_value")
    if value is not None and (not isinstance(value, (int, float)) or not math.isfinite(value)):
        return "invalid_numeric_value"
    if record.get("source") == "ghcn_daily":
        element = record.get("event_type")
        if element == "PRCP" and value is not None and value < 0:
            return "negative_precipitation"
        if element in {"TMAX", "TMIN"} and value is not None and value < -273.15:
            return "below_absolute_zero"
        if element not in {"PRCP", "TMAX", "TMIN"}:
            return "unsupported_element"
    elif record.get("source") == "noaa_storm_events":
        if value is not None and value < 0:
            return "negative_magnitude"
        if value is not None and not record.get("severity_unit"):
            return "unknown_magnitude_unit"
    else:
        return "unknown_source"
    return None
