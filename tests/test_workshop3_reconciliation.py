"""Independent verification must distinguish text snapshots from source records."""
import unittest
import pandas as pd
from scripts.workshop_3.verify_gold import reconcile_text_snapshots


class TextReconciliationTests(unittest.TestCase):
    def fixture(self,path,text='Synthetic test narrative',score=0.0):
        return pd.DataFrame([{'source':'noaa_storm_events','source_key':'synthetic-test-id',
                              '_text_file':path,'raw_text':text,'sentiment_score':score,
                              'tokens':['synthetic','test','narrative']}])

    def test_identical_exports_are_not_additional_records(self):
        first=self.fixture('first.parquet');second=self.fixture('second.parquet')
        selected,snapshot_rows=reconcile_text_snapshots([first,second])
        self.assertEqual(snapshot_rows,2)
        self.assertEqual(len(selected),1)
        self.assertEqual(selected.iloc[0]['_text_file'],'second.parquet')
        self.assertNotIn('_signature',first.columns)

    def test_conflicting_same_key_text_cannot_be_silently_selected(self):
        with self.assertRaisesRegex(ValueError,'conflicting_text_snapshot'):
            reconcile_text_snapshots([self.fixture('first'),self.fixture('second',text='Different test narrative')])
        with self.assertRaisesRegex(ValueError,'conflicting_text_snapshot'):
            reconcile_text_snapshots([self.fixture('first'),self.fixture('second',score=0.8)])


if __name__=='__main__':unittest.main()
