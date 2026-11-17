"""Offline batch publication and tamper detection, using synthetic fixtures."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from multi_hazard_weather_monitoring import historical_pipeline as pipeline


class BronzePipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.patch=patch.object(pipeline,'ROOT',self.root)
        self.patch.start();self.addCleanup(self.patch.stop)
        body=b'STATION,DATE,PRCP\nS,2025-01-01,1\n'
        (self.root/'fixture.csv').write_bytes(body)
        (self.root/'config').mkdir()
        source=dict(source='ghcn_daily',partition='fixture',path='fixture.csv',source_url='https://example.test',source_format='csv',attribution='synthetic')
        (self.root/'config/workshop2_saved_captures.json').write_text(json.dumps({'captures':[source]}))
        register=self.root/'workshop_1/samples/candidate_pairs/submission_evidence_audit.json'
        register.parent.mkdir(parents=True)
        register.write_text(json.dumps({'input_sha256':{'fixture.csv':hashlib.sha256(body).hexdigest()}}))

    def publish(self):
        return pipeline.publish_bronze('fixture','test-batch','2026-11-16T20:00:00+00:00')

    def test_retry_publishes_same_bytes_and_original_capture(self):
        first=Path(self.publish()).read_bytes()
        path=self.publish()
        self.assertEqual(Path(path).read_bytes(),first)
        payload=json.loads(first)
        native=self.root/'data/raw'/payload['original_capture']['raw_path']
        self.assertEqual(native.read_bytes(),(self.root/'fixture.csv').read_bytes())

    def test_changed_parsed_view_is_rejected_before_connecting(self):
        path=Path(self.publish());payload=json.loads(path.read_text())
        payload['rows'][0]['PRCP']='9'
        path.write_text(json.dumps(payload))
        with patch('ingest._connect') as connect:
            with self.assertRaisesRegex(ValueError,'bronze_parsed_view_mismatch'):
                pipeline.process_bronze(path)
            connect.assert_not_called()

    def test_exact_bronze_landing_boundary_is_required(self):
        with self.assertRaisesRegex(ValueError,'bronze_path_outside_landing'):
            pipeline.checked_bronze_path(self.root/'untrusted.json')
