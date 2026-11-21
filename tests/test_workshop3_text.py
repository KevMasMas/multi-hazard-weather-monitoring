"""Focused checks for source-bound narrative Silver and folder inventory."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from multi_hazard_weather_monitoring.gold import verified_inputs
from multi_hazard_weather_monitoring.text_silver import (
    clean_tokens, classify_sentiment, export_narrative_silver, narrative_rows)


class TextSilverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.body = (b'EVENT_ID,EVENT_NARRATIVE,EPISODE_NARRATIVE\n'
                     b'1,"Strong wind damaged homes.",Fallback\n'
                     b'2,,"Thankfully no injuries."\n')
        self.sha = hashlib.sha256(self.body).hexdigest()

    def test_source_field_selection_and_sentiment_are_explicit(self):
        rows = narrative_rows(self.body, capture_sha256=self.sha)
        self.assertEqual([r['text_field'] for r in rows],
                         ['EVENT_NARRATIVE', 'EPISODE_NARRATIVE'])
        self.assertEqual([r['source_key'] for r in rows], ['1', '2'])
        self.assertEqual(classify_sentiment(0.05), 'positive')
        self.assertEqual(classify_sentiment(-0.05), 'negative')
        self.assertEqual(classify_sentiment(0), 'neutral')
        self.assertEqual(clean_tokens('Wind <b>near</b> #Oklahoma https://example.org @user'),
                         ['wind', 'oklahoma'])
        with self.assertRaisesRegex(ValueError, 'narrative_capture_hash_mismatch'):
            narrative_rows(self.body, capture_sha256='0' * 64)

    def test_parquet_replay_preserves_bytes_and_rejects_conflict(self):
        destination = self.root / 'text.parquet'
        first = export_narrative_silver(self.body, capture_sha256=self.sha,
                                        destination=destination)
        second = export_narrative_silver(self.body, capture_sha256=self.sha,
                                         destination=destination)
        self.assertEqual(first, second)
        self.assertEqual(first['rows'], 2)
        changed = self.body.replace(b'damaged', b'destroyed')
        with self.assertRaisesRegex(ValueError, 'existing_narrative_silver_conflict'):
            export_narrative_silver(changed,
                                    capture_sha256=hashlib.sha256(changed).hexdigest(),
                                    destination=destination)

    def test_every_silver_file_requires_hash_evidence(self):
        folder = self.root / 'datalake_silver'
        folder.mkdir()
        first = folder / 'first.parquet'
        first.write_bytes(b'first')
        register = self.root / 'register.json'
        register.write_text(json.dumps({'input_sha256': {
            'data/curated/silver/first.parquet': hashlib.sha256(b'first').hexdigest()}}))
        config = {'input_register': 'register.json', 'silver_folder': 'datalake_silver'}
        self.assertEqual(len(verified_inputs(self.root, config)), 1)
        second = folder / 'second.parquet'
        second.write_bytes(b'second')
        with self.assertRaisesRegex(ValueError, 'unregistered_silver_file'):
            verified_inputs(self.root, config)
        second.with_suffix('.manifest.json').write_text(json.dumps({
            'path': 'datalake_silver/second.parquet',
            'sha256': hashlib.sha256(b'second').hexdigest().upper()}))
        self.assertEqual(len(verified_inputs(self.root, config)), 2)


if __name__ == '__main__':
    unittest.main()
