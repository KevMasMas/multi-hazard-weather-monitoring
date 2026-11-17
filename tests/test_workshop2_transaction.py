"""Offline checks for bounded selection and the transaction boundary."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from ingest import select_captures
from multi_hazard_weather_monitoring.storage.postgres_historical import load_partition

ROOT = Path(__file__).resolve().parents[1]


class FakeCursor:
    def __init__(self, fail_on_state: bool = False):
        self.fail_on_state = fail_on_state
        self.statements: list[str] = []
        self.last_statement = ""

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, statement, _params=None):
        self.last_statement = statement
        self.statements.append(statement)
        if self.fail_on_state and "INSERT INTO ingestion_state" in statement:
            raise RuntimeError("injected_state_failure")

    def fetchone(self):
        if "SELECT capture_id" in self.last_statement:
            return (10, "ghcn_daily/partition/hash.csv", "sample.csv")
        if "RETURNING run_id" in self.last_statement:
            return (20,)
        if "SELECT source_content_sha256" in self.last_statement:
            return None
        raise AssertionError(self.last_statement)


class FakeConnection:
    autocommit = False

    def __init__(self, fail_on_state: bool = False):
        self.fake_cursor = FakeCursor(fail_on_state)
        self.commits = 0
        self.rollbacks = 0

    def cursor(self):
        return self.fake_cursor

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


SOURCE = {"source": "ghcn_daily", "partition": "partition",
          "source_url": "https://example.test", "source_format": "csv", "attribution": "test"}
CAPTURE = {"raw_path": "ghcn_daily/partition/hash.csv", "content_type": "text/csv",
           "byte_count": 1, "sha256": "a" * 64, "origin": "sample.csv"}


class HistoricalTransactionTests(unittest.TestCase):
    def test_saved_capture_selection_requires_complete_interval(self):
        # Selection is a date-contract test, independent of the growing real registry.
        config = {'captures': [
            dict(source='noaa_storm_events', partition='sample_2024', start='2024-01-01', end='2024-12-31'),
            dict(source='ghcn_daily', partition='USW00013967_2025', start='2025-01-01', end='2025-12-31'),
            dict(source='ghcn_daily', partition='outside', start='2026-01-01', end='2026-12-31')]}
        selected = select_captures(config, "2024-01-01", "2025-12-31")
        self.assertEqual([(x["source"], x["partition"]) for x in selected],
                         [("noaa_storm_events", "sample_2024"),
                          ("ghcn_daily", "USW00013967_2025")])
        with self.assertRaisesRegex(ValueError, "no_saved_capture"):
            select_captures(config, "2025-07-01", "2025-12-31")

    def test_state_update_and_run_metrics_precede_single_commit(self):
        connection = FakeConnection()
        result = load_partition(connection, source=SOURCE, capture=CAPTURE, records=[])
        self.assertEqual(result, {"read": 0, "accepted": 0, "rejected": 0, "unchanged": 0})
        self.assertEqual((connection.commits, connection.rollbacks), (1, 0))
        statements = connection.fake_cursor.statements
        self.assertIn('pg_advisory_xact_lock', statements[0])
        self.assertLess(next(i for i, s in enumerate(statements) if "UPDATE ingestion_run" in s),
                        next(i for i, s in enumerate(statements) if "INSERT INTO ingestion_state" in s))

    def test_state_failure_rolls_back_without_commit(self):
        connection = FakeConnection(fail_on_state=True)
        with self.assertRaisesRegex(RuntimeError, "injected_state_failure"):
            load_partition(connection, source=SOURCE, capture=CAPTURE, records=[])
        self.assertEqual((connection.commits, connection.rollbacks), (0, 1))

    def test_mismatched_source_rolls_back_before_record_write(self):
        connection = FakeConnection()
        with self.assertRaisesRegex(ValueError, "record_source_mismatch"):
            load_partition(connection, source=SOURCE, capture=CAPTURE,
                           records=[{"source": "noaa_storm_events"}])
        self.assertEqual((connection.commits, connection.rollbacks), (0, 1))


if __name__ == "__main__":
    unittest.main()
