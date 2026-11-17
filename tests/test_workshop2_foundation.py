"""Tests for the first weather-specific Bronze and validation boundaries."""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multi_hazard_weather_monitoring.normalization.validation import rejection_reason
from multi_hazard_weather_monitoring.sources.historical_samples import (
    parse_ghcn_daily,
    parse_noaa_storm_events,
)
from multi_hazard_weather_monitoring.storage.raw_landing import (
    land_capture,
    require_registered_capture,
)

TEST_TEMP_ROOT = Path(__file__).resolve().parents[1] / "data/raw"


class HistoricalFoundationTests(unittest.TestCase):
    def test_noaa_gust_category_is_not_a_unit(self) -> None:
        body = (b"EVENT_ID,EVENT_TYPE,CZ_TIMEZONE,BEGIN_DATE_TIME,MAGNITUDE,MAGNITUDE_TYPE\n"
                b"1155308,High Wind,CST-6,08-JAN-24 12:00:00,51,MG\n")
        row = next(parse_noaa_storm_events(body))
        self.assertEqual((row["severity_value"], row["severity_unit"], row["magnitude_type"]),
                         (51.0, "kn", "MG"))

    def test_negative_precipitation_is_rejected_after_parsing(self) -> None:
        row = next(parse_ghcn_daily(b"STATION,DATE,PRCP\nS,2025-01-01,-3\n"))
        self.assertEqual(rejection_reason(row), "negative_precipitation")

    def test_registered_hash_is_required_before_landing(self) -> None:
        body = b"recorded source bytes"
        register = {"evidence.csv": hashlib.sha256(body).hexdigest()}
        require_registered_capture(body, "evidence.csv", register)
        with self.assertRaisesRegex(ValueError, "registered_capture_hash_mismatch"):
            require_registered_capture(body + b"changed", "evidence.csv", register)

    def test_landing_is_idempotent_and_keeps_origin(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            root = Path(directory)
            args = dict(source="ghcn_daily", partition="S_2025", root=root,
                        content_type="text/csv", origin="sample.csv")
            first = land_capture(b"a,b\n1,2\n", **args)
            self.assertEqual(first, land_capture(b"a,b\n1,2\n", **args))
            self.assertEqual(len(list(root.rglob("*.csv"))), 1)
            with self.assertRaisesRegex(ValueError, "capture_manifest_conflict"):
                land_capture(b"a,b\n1,2\n", **{**args, "origin": "other.csv"})

    def test_write_failure_removes_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            root = Path(directory)
            with patch("multi_hazard_weather_monitoring.storage.raw_landing.os.fsync",
                       side_effect=OSError("injected fsync failure")):
                with self.assertRaisesRegex(OSError, "injected fsync failure"):
                    land_capture(b"a,b\n1,2\n", source="ghcn_daily", partition="S_2025",
                                 root=root, content_type="text/csv", origin="sample.csv")
            self.assertEqual(list(root.rglob("*.*")), [])

    def test_gzip_keeps_native_format(self) -> None:
        import gzip
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as directory:
            body = gzip.compress(b"a,b\n1,2\n")
            manifest = land_capture(body, source="noaa_storm_events", partition="2024",
                                    root=Path(directory), content_type="application/gzip",
                                    origin="archive.gz")
            self.assertEqual(manifest["raw_format"], "gz")
            self.assertEqual((Path(directory) / manifest["raw_path"]).read_bytes(), body)


if __name__ == "__main__":
    unittest.main()
