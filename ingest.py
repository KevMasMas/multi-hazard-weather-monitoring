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
from multi_hazard_weather_monitoring.storage.migrations import migrate  # noqa: E402
from multi_hazard_weather_monitoring.sources.capture_registry import registered_hashes  # noqa: E402
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
    parser.add_argument("--replay", help="Checksum-locked NWS manifest; performs no network requests")
    parser.add_argument("--source", choices=('nws_alerts','nws_station_observations'), help="Live incremental source; requires NWS_USER_AGENT")
    parser.add_argument("--scope", help="OK for alerts or configured station ID, e.g. KOKC")
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
    migrate(connection)


def _historical(connection, start: str, end: str) -> list[dict]:
    config = json.loads((ROOT / "config/workshop2_saved_captures.json").read_text(encoding="utf-8"))
    selected = select_captures(config, start, end)
    register = registered_hashes(ROOT)
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
    if args.mode == 'incremental' and (bool(args.replay) == bool(args.source)):
        build_parser().error('incremental requires either --replay or --source (live), exclusively')
    if args.mode != 'incremental' and (args.replay or args.source or args.scope):
        build_parser().error('NWS arguments require incremental mode')
    if args.mode == 'incremental' and (args.start or args.end):
        build_parser().error('incremental windows are managed by source state, not historical dates')
    if args.mode == "historical" and (not args.start or not args.end):
        build_parser().error("historical mode requires both --start and --end")
    if args.mode == "status" and (args.start or args.end):
        build_parser().error("status mode does not accept --start or --end")
    try:
        with closing(_connect()) as connection:
            if args.mode == 'incremental':
                from multi_hazard_weather_monitoring.incremental import replay, live
                _migrate(connection)
                result = replay(connection, ROOT, (ROOT / args.replay)) if args.replay else live(connection, ROOT, args.source, args.scope or ('OK' if args.source=='nws_alerts' else 'KOKC'))
            elif args.mode == 'historical':
                result = _historical(connection, args.start, args.end)
            else:
                from multi_hazard_weather_monitoring.incremental import status
                _migrate(connection)
                result = {'historical':_status(connection),'incremental':status(connection)}
        print(json.dumps({"mode": args.mode, "result": result}, default=str))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"mode": args.mode, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
