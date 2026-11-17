"""Check malformed canonical records fail before a database insert."""
import unittest
from multi_hazard_weather_monitoring.sources.historical_samples import parse_ghcn_daily, parse_noaa_storm_events
from multi_hazard_weather_monitoring.normalization.validation import rejection_reason


class CanonicalValidationTests(unittest.TestCase):
    def setUp(self):
        self.record = next(parse_ghcn_daily(b'STATION,DATE,TMAX\nS,2025-01-01,12\n'))

    def test_valid_source_record_and_missing_point_are_retained(self):
        self.assertIsNone(rejection_reason(self.record))

    def test_hail_magnitude_uses_inches_from_official_bulk_format(self):
        body=b'EVENT_ID,EVENT_TYPE,CZ_TIMEZONE,BEGIN_DATE_TIME,MAGNITUDE\n1,Hail,CST-6,01-Jan-24 12:00:00,1.75\n'
        record=next(parse_noaa_storm_events(body))
        self.assertEqual(record['severity_unit'],'in')
        self.assertEqual(record['severity_value'],1.75)
        self.assertIsNone(rejection_reason(record))

    def test_missing_identity_is_a_quarantine_reason(self):
        self.assertEqual(rejection_reason({**self.record, 'source_key': ''}), 'missing_source_key')

    def test_daily_record_must_not_have_two_time_grains(self):
        self.assertEqual(rejection_reason({**self.record, 'observed_at_utc': '2025-01-01T00:00:00Z'}), 'invalid_time_grain')

    def test_daily_measurements_keep_expected_units(self):
        self.assertEqual(rejection_reason({**self.record, 'severity_unit': 'kn'}), 'unexpected_measurement_unit')

    def test_missing_measurement_not_imputed_as_zero(self):
        self.assertEqual(rejection_reason({**self.record, 'severity_value': None}), 'missing_measurement_value')

    def test_coordinate_pair_and_ranges(self):
        self.assertEqual(rejection_reason({**self.record, 'latitude': 35}), 'incomplete_coordinates')
        self.assertEqual(rejection_reason({**self.record, 'latitude': 91, 'longitude': -97}), 'coordinates_out_of_range')

    def test_hash_and_line_are_required_for_provenance(self):
        self.assertEqual(rejection_reason({**self.record, 'source_content_sha256': 'bad'}), 'invalid_content_hash')
        self.assertEqual(rejection_reason({**self.record, 'source_line': 0}), 'invalid_source_line')
