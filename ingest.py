"""Historical ingestion and database status command for Workshop 2."""

from __future__ import annotations

import argparse
from contextlib import closing
import json
import os
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from multi_hazard_weather_monitoring.sources.historical_samples import (  # noqa: E402
    parse_ghcn_daily, parse_noaa_storm_events,
)
from multi_hazard_weather_monitoring.storage.postgres_historical import load_partition  # noqa: E402
from multi_hazard_weather_monitoring.storage.raw_landing import (  # noqa: E402
    land_capture, require_registered_capture,
)

PARSERS = {"noaa_storm_events": parse_noaa_storm_events, "ghcn_daily": parse_ghcn_daily}


def build_parser() -> argparse.ArgumentParser:
    """Build the shared course-project command-line interface."""
    parser = argparse.ArgumentParser(
        description="Multi-Hazard Weather Impact Monitoring ingestion CLI"
    )
    parser.add_argument(
        "--mode",
        choices=("historical", "incremental", "status"),
        required=True,
        help="Execution mode required by the common course contract.",
    )
    parser.add_argument("--start", help="Inclusive start date (YYYY-MM-DD) for saved capture selection")
    parser.add_argument("--end", help="Inclusive end date (YYYY-MM-DD) for saved capture selection")
    return parser


def select_captures(config: dict, start: str, end: str) -> list[dict]:
    """Select only fully contained saved captures; never truncate a source file."""
    lower, upper = date.fromisoformat(start), date.fromisoformat(end)
    if lower > upper:
        raise ValueError("start_after_end")
    selected = []
    for item in config["captures"]:
        first, last = date.fromisoformat(item["start"]), date.fromisoformat(item["end"])
        if lower <= first and last <= upper:
            selected.append(item)
    if not selected:
        raise ValueError("no_saved_capture_fully_inside_date_range")
    return selected


def _connect():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is required")
    try:
        import psycopg2
    except ImportError as exc:
        raise RuntimeError("Install requirements-workshop2.in before database commands") from exc
    return psycopg2.connect(url)


def _migrate(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute((ROOT / "sql/001_historical_schema.sql").read_text(encoding="utf-8"))
    connection.commit()


def _historical(connection, start: str, end: str) -> list[dict]:
    config = json.loads((ROOT / "config/workshop2_saved_captures.json").read_text(encoding="utf-8"))
    selected = select_captures(config, start, end)
    register = json.loads((ROOT / "workshop_1/samples/candidate_pairs/submission_evidence_audit.json")
                          .read_text(encoding="utf-8"))["input_sha256"]
    # Check all selected inputs before creating schema or writing data.
    bodies = []
    for item in selected:
        body = (ROOT / item["path"]).read_bytes()
        require_registered_capture(body, item["path"], register)
        bodies.append(body)
    _migrate(connection)
    output = []
    for item, body in zip(selected, bodies):
        capture = land_capture(body, source=item["source"], partition=item["partition"],
                               root=ROOT / "data/raw", content_type="text/csv",
                               origin=item["path"])
        counts = load_partition(connection, source=item, capture=capture,
                                records=PARSERS[item["source"]](body))
        output.append({"source": item["source"], "partition": item["partition"], **counts})
    return output


def _status(connection) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT source_id, partition_key, status, rows_read, rows_accepted,
                       rows_rejected, rows_unchanged, started_at_utc, finished_at_utc
                       FROM ingestion_run ORDER BY run_id DESC LIMIT 20""")
        fields = ("source", "partition", "status", "read", "accepted", "rejected",
                  "unchanged", "started_at_utc", "finished_at_utc")
        return [dict(zip(fields, row)) for row in cursor.fetchall()]


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.mode == "incremental":
        print(json.dumps({"mode": args.mode, "status": "planned_for_workshop_3"}))
        return 2
    if args.mode == "historical" and (not args.start or not args.end):
        build_parser().error("historical mode requires both --start and --end")
    if args.mode == "status" and (args.start or args.end):
        build_parser().error("status mode does not accept --start or --end")
    try:
        with closing(_connect()) as connection:
            result = (_historical(connection, args.start, args.end)
                      if args.mode == "historical" else _status(connection))
        print(json.dumps({"mode": args.mode, "result": result}, default=str))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"mode": args.mode, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
