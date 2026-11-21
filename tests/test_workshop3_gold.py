"""Small synthetic Spark fixtures: duplicates, revisions, undefined flags, units."""
from datetime import date
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from multi_hazard_weather_monitoring.gold import (
    ROOT,create_spark,consolidate,governance,storytelling,verified_inputs,build_gold)


class GoldInputTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        (self.root/'data/curated/silver').mkdir(parents=True)
        self.file=self.root/'data/curated/silver/fixture.parquet'
        # Hash-validation fixture only, never passed to a Spark reader.
        self.file.write_bytes(b'synthetic registry bytes')
        self.register=self.root/'register.json'
        self.config={'input_register':'register.json'}
        self.register.write_text(json.dumps({'input_sha256':{
            'data/curated/silver/fixture.parquet':hashlib.sha256(self.file.read_bytes()).hexdigest()}}))

    def test_registered_hash_is_verified(self):
        self.assertEqual(len(verified_inputs(self.root,self.config)),1)

    def test_changed_file_fails_before_spark(self):
        self.file.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'silver_checksum_mismatch'):
            verified_inputs(self.root,self.config)

    def test_path_outside_silver_is_rejected(self):
        self.register.write_text(json.dumps({'input_sha256':{'register.json':'a'*64}}))
        with self.assertRaisesRegex(ValueError,'silver_path_outside_curated'):
            verified_inputs(self.root,self.config)

    def test_empty_population_is_not_a_successful_zero(self):
        self.register.write_text(json.dumps({'input_sha256':{}}))
        with self.assertRaisesRegex(ValueError,'empty_silver_register'):
            verified_inputs(self.root,self.config)

    def test_committed_batch_identity_is_not_overwritten(self):
        (self.root/'config').mkdir()
        (self.root/'config/workshop3_gold.json').write_text(json.dumps(self.config))
        token=hashlib.sha256(b'fixture').hexdigest()[:12]
        batch=self.root/'data/gold'/('20250101_000000_'+token)
        batch.mkdir(parents=True)
        manifest=batch/'manifest.json'
        manifest.write_text(json.dumps({'signature':'different'}))
        before=manifest.read_bytes()
        with self.assertRaisesRegex(ValueError,'gold_batch_identity_conflict'):
            build_gold(self.root,'fixture','2025-01-01T00:00:00+00:00')
        self.assertEqual(manifest.read_bytes(),before)


class GoldSparkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads((ROOT/'config/workshop3_gold.json').read_text())
        cls.spark=create_spark(cls.config)
        cls.spark.sparkContext.setLogLevel('ERROR')
        # Explicit schema mirrors Silver, with no dependence on live sources.
        cls.schema='''record_id long,source string,source_key string,event_type string,
            observed_at_utc timestamp,observed_date date,latitude double,longitude double,
            severity_value double,severity_unit string,magnitude_type string,quality_attributes string,
            source_content_sha256 string,capture_sha256 string,run_id long,capture_id long,
            source_line long,revision_id long'''

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def rows(self):
        return [dict(record_id=i,source='ghcn_daily',source_key=f'S/2025-01-0{i}/PRCP',event_type='PRCP',
            observed_at_utc=None,observed_date=date(2025,1,i),latitude=35.,longitude=-97.,
            severity_value=0.,severity_unit='mm',magnitude_type=None,quality_attributes=',,S',
            source_content_sha256='a'*64,capture_sha256='b'*64,run_id=1,capture_id=1,
            source_line=i+1,revision_id=i) for i in range(1,5)]

    def save(self,folder,name,rows):
        path=folder/name
        self.spark.createDataFrame(rows,self.schema).coalesce(1).write.parquet(str(path))
        return path

    def test_latest_observed_run_wins_without_double_count(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            first=self.rows()
            repeat=[dict(row,run_id=2,capture_id=2,capture_sha256='c'*64) for row in first]
            repeat[0]=dict(repeat[0],severity_value=7.,revision_id=10,source_content_sha256='d'*64)
            paths=[self.save(folder,'first',first),self.save(folder,'repeat',repeat)]
            raw,current=consolidate(self.spark,paths,'2025-01-01','2025-12-31')
            self.assertEqual(raw.count(),8);self.assertEqual(current.count(),4)
            self.assertEqual(current.filter('record_id=1').first()['severity_value'],7.)
            story=storytelling(current,'fixture')
            self.assertEqual(story.first()['record_count'],4)
            self.assertEqual(story.first()['precipitation_total_mm'],7.)
            raw.unpersist();current.unpersist()

    def test_same_revision_with_conflicting_values_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);rows=self.rows()
            other=[dict(rows[0],run_id=2,severity_value=9.)]
            paths=[self.save(folder,'first',rows),self.save(folder,'conflict',other)]
            with self.assertRaisesRegex(ValueError,'conflicting_silver_snapshot'):
                consolidate(self.spark,paths,'2025-01-01','2025-12-31')

    def test_zero_iqr_and_temperature_sum_are_not_invented(self):
        frame=self.spark.createDataFrame(self.rows(),self.schema).withColumnRenamed('observed_date','_date')
        # Recreate the original date for the nullness metrics.
        from pyspark.sql import functions as F
        frame=frame.withColumn('observed_date',F.col('_date'))
        metrics=governance(frame,frame,self.config,'fixture')
        row=metrics.filter("metric='iqr_review_fraction' AND population='all_days'").first()
        self.assertIsNone(row['value']);self.assertEqual(row['status'],'unavailable_zero_or_missing_scale')
        skew=metrics.filter("metric='sample_skewness' AND population='all_days'").first()
        self.assertIsNone(skew['value'])
        temps=frame.withColumn('event_type',F.lit('TMAX')).withColumn('severity_unit',F.lit('degC'))
        self.assertIsNone(storytelling(temps,'fixture').first()['precipitation_total_mm'])


if __name__=='__main__':unittest.main(verbosity=2)
