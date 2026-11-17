"""Transactional PostgreSQL load of one bounded historical capture."""

from __future__ import annotations

import json
from collections.abc import Iterable

from multi_hazard_weather_monitoring.normalization.validation import rejection_reason


def load_partition(connection, *, source: dict, capture: dict,
                   records: Iterable[dict]) -> dict[str, int]:
    """Commit records, rejects, run metrics and partition state together.

    The caller owns the connection. An exception rolls back every database
    change for this partition; the immutable raw file may remain for replay.
    """
    source_id = source["source"]
    partition = source["partition"]
    counts = {"read": 0, "accepted": 0, "rejected": 0, "unchanged": 0}
    seen: set[str] = set()
    if connection.autocommit:
        raise ValueError("transactional_connection_required")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO source_catalog(source_id, source_url, source_format, attribution)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (source_id) DO NOTHING""",
                (source_id, source["source_url"], source["source_format"], source["attribution"]),
            )
            cursor.execute(
                """INSERT INTO raw_capture(source_id, partition_key, raw_path, content_type,
                       byte_count, sha256, origin_reference)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (source_id, partition_key, sha256) DO NOTHING""",
                (source_id, partition, capture["raw_path"], capture["content_type"],
                 capture["byte_count"], capture["sha256"], capture["origin"]),
            )
            cursor.execute(
                """SELECT capture_id, raw_path, origin_reference FROM raw_capture
                   WHERE source_id=%s AND partition_key=%s AND sha256=%s""",
                (source_id, partition, capture["sha256"]),
            )
            capture_id, stored_path, stored_origin = cursor.fetchone()
            if (stored_path, stored_origin) != (capture["raw_path"], capture["origin"]):
                raise ValueError("database_capture_provenance_conflict")
            cursor.execute(
                """INSERT INTO ingestion_run(source_id, partition_key, capture_id, status)
                   VALUES (%s, %s, %s, 'running') RETURNING run_id""",
                (source_id, partition, capture_id),
            )
            run_id = cursor.fetchone()[0]
            for record in records:
                counts["read"] += 1
                if record.get("source") != source_id:
                    raise ValueError("record_source_mismatch")
                reason = rejection_reason(record)
                key = record.get("source_key")
                if reason is None and key in seen:
                    reason = "duplicate_source_key_in_partition"
                if reason is not None:
                    cursor.execute(
                        """INSERT INTO rejected_record(run_id, capture_id, source_line,
                               element_code, reason_code, raw_fields)
                           VALUES (%s, %s, %s, %s, %s, %s::jsonb)
                           ON CONFLICT DO NOTHING""",
                        (run_id, capture_id, record["source_line"],
                         record.get("element") or (record.get("event_type") if source_id == "ghcn_daily" else None),
                         reason, json.dumps(record["raw_fields"])),
                    )
                    counts["rejected"] += 1
                    continue
                seen.add(key)
                cursor.execute(
                    """SELECT source_content_sha256 FROM historical_record
                       WHERE source_id=%s AND source_key=%s FOR UPDATE""",
                    (source_id, key),
                )
                existing = cursor.fetchone()
                if existing and existing[0].strip() == record["source_content_sha256"]:
                    counts["unchanged"] += 1
                    continue
                cursor.execute(
                    """INSERT INTO historical_record(source_id, source_key, event_type,
                           observed_at_utc, observed_date, latitude, longitude,
                           severity_value, severity_unit, magnitude_type,
                           geography_reference, quality_attributes, source_content_sha256,
                           capture_id, source_line, last_run_id)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       ON CONFLICT (source_id, source_key) DO UPDATE SET
                           event_type=EXCLUDED.event_type,
                           observed_at_utc=EXCLUDED.observed_at_utc,
                           observed_date=EXCLUDED.observed_date,
                           latitude=EXCLUDED.latitude,
                           longitude=EXCLUDED.longitude,
                           severity_value=EXCLUDED.severity_value,
                           severity_unit=EXCLUDED.severity_unit,
                           magnitude_type=EXCLUDED.magnitude_type,
                           geography_reference=EXCLUDED.geography_reference,
                           quality_attributes=EXCLUDED.quality_attributes,
                           source_content_sha256=EXCLUDED.source_content_sha256,
                           capture_id=EXCLUDED.capture_id,
                           source_line=EXCLUDED.source_line,
                           last_run_id=EXCLUDED.last_run_id""",
                    (source_id, key, record["event_type"], record["observed_at_utc"],
                     record["observed_date"], record["latitude"], record["longitude"],
                     record["severity_value"], record["severity_unit"],
                     record.get("magnitude_type"), record.get("geography_reference"),
                     record.get("quality_attributes"), record["source_content_sha256"],
                     capture_id, record["source_line"], run_id),
                )
                counts["accepted"] += 1
            cursor.execute(
                """UPDATE ingestion_run SET status='succeeded', finished_at_utc=now(),
                       rows_read=%s, rows_accepted=%s, rows_rejected=%s,
                       rows_unchanged=%s WHERE run_id=%s""",
                (counts["read"], counts["accepted"], counts["rejected"],
                 counts["unchanged"], run_id),
            )
            cursor.execute(
                """INSERT INTO ingestion_state(source_id, partition_key,
                       last_successful_run_id, last_successful_at_utc)
                   VALUES (%s, %s, %s, now())
                   ON CONFLICT (source_id, partition_key) DO UPDATE SET
                       last_successful_run_id=EXCLUDED.last_successful_run_id,
                       last_successful_at_utc=EXCLUDED.last_successful_at_utc""",
                (source_id, partition, run_id),
            )
        connection.commit()
        return counts
    except BaseException:
        connection.rollback()
        raise
