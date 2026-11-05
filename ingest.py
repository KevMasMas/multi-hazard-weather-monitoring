"""Workshop 1 command-line contract placeholder.

The ingestion modes are implemented in Workshops 2 and 3. This file exists now
because Workshop 1 requires the common CLI entry point to be present as a stub.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence


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
    parser.add_argument("--start", help="Optional inclusive start date (YYYY-MM-DD).")
    parser.add_argument("--end", help="Optional inclusive end date (YYYY-MM-DD).")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse the contract and report that implementation belongs to later workshops."""
    args = build_parser().parse_args(argv)
    print(
        json.dumps(
            {
                "mode": args.mode,
                "start": args.start,
                "end": args.end,
                "status": "not_implemented",
                "milestone": "workshop_1_scaffold",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
