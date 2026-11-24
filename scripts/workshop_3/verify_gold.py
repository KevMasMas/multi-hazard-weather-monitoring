"""Independently reconcile saved Spark Gold with Pandas and reviewed Silver."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]


def reconcile_text_snapshots(frames):
    """Independently reconcile repeated text exports before comparing aggregates.

    Source keys may recur across captures. Conflicting narrative content fails;
    identical exports are evidence of one source record, not additional text.
    """
    snapshots=pd.concat(frames,ignore_index=True)
    if snapshots[['source','source_key','_text_file']].isna().any().any():
        raise ValueError('missing_text_snapshot_identity')
    def signature(row):
        return json.dumps([None if pd.isna(row.raw_text) else row.raw_text,
                           None if pd.isna(row.sentiment_score) else float(row.sentiment_score),
                           list(row.tokens) if row.tokens is not None else None],sort_keys=True)
    snapshots['_signature']=snapshots.apply(signature,axis=1)
    if (snapshots.groupby(['source','source_key'])['_signature'].nunique()>1).any():
        raise ValueError('conflicting_text_snapshot_content')
    selected=(snapshots.sort_values('_text_file').drop_duplicates(['source','source_key'],keep='last')
              .drop(columns=['_signature']))
    return selected,len(snapshots)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--receipt',default='workshop_3/evidence/gold_reconciliation.json')
    args=parser.parse_args()
    path=Path(args.manifest)
    if not path.is_absolute():path=ROOT/path
    receipt=json.loads(path.read_text())
    tables={}
    for name,item in receipt['outputs'].items():
        source=ROOT/item['path']
        assert hashlib.sha256(source.read_bytes()).hexdigest().upper()==item['sha256']
        tables[name]=pd.read_parquet(source)
        assert len(tables[name])==item['rows']
    frames=[]
    for name,digest in receipt['identity']['inputs'].items():
        p=ROOT/name
        assert hashlib.sha256(p.read_bytes()).hexdigest().upper()==digest
        df=pd.read_parquet(p);df['_input_file']=name;frames.append(df)
    raw=pd.concat(frames,ignore_index=True)
    day=pd.to_datetime(raw['observed_date']).fillna(pd.to_datetime(raw['observed_at_utc'],utc=True).dt.tz_localize(None)).dt.normalize()
    config=receipt['identity']['config']
    raw=raw[day.between(pd.Timestamp(config['start']),pd.Timestamp(config['end']))]
    current=raw.sort_values(['run_id','_input_file']).drop_duplicates(['source','source_key'],keep='last').copy()
    assert receipt['counts']['snapshot_rows']==len(raw)
    assert receipt['counts']['unique_business_records']==len(current)
    assert receipt['counts']['source_counts']==current.groupby('source').size().to_dict()
    gov=tables['governance'];story=tables['storytelling']
    assert not gov.duplicated(['source','station','population','period','variable','unit','metric']).any()
    assert not story.duplicated(['source','station','period','event_type','severity_unit']).any()
    assert story.groupby('source')['record_count'].sum().to_dict()==current.groupby('source').size().to_dict()
    assert story.loc[~story['event_type'].eq('PRCP'),'precipitation_total_mm'].isna().all()
    current['_date']=pd.to_datetime(current['observed_date']).fillna(
        pd.to_datetime(current['observed_at_utc'],utc=True).dt.tz_localize(None))
    current['_period']=current['_date'].dt.strftime('%Y-%m')
    monthly_event_groups=0
    for (period,event_type,unit),rows in current[current['source'].eq('noaa_storm_events')].groupby(
            ['_period','event_type','severity_unit'],dropna=False):
        match=story[story['source'].eq('noaa_storm_events')&story['period'].eq(period)&story['event_type'].eq(event_type)]
        match=match[match['severity_unit'].isna() if pd.isna(unit) else match['severity_unit'].eq(unit)]
        assert len(match)==1
        item=match.iloc[0]
        assert item['record_count']==len(rows)
        assert item['measured_count']==rows['severity_value'].notna().sum()
        assert item['missing_point_count']==rows['latitude'].isna().sum()
        for field,expected in [('mean_value',rows['severity_value'].mean()),
                               ('min_value',rows['severity_value'].min()),('max_value',rows['severity_value'].max())]:
            np.testing.assert_allclose(item[field],expected,rtol=1e-9,equal_nan=True)
        monthly_event_groups+=1
    daily=current[current['source'].eq('ghcn_daily')].copy()
    daily['station']=daily['source_key'].str.split('/').str[0]
    shape_checks=0
    for (station,element,unit),rows in daily.groupby(['station','event_type','severity_unit']):
        for population,values in [('all_days',rows['severity_value']),
             *([('positive_reported_precipitation',rows.loc[rows['severity_value'].gt(0),'severity_value'])] if element=='PRCP' else [])]:
            selected=gov[(gov['station'].eq(station))&(gov['variable'].eq(element))&
                         gov['population'].eq(population)&gov['period'].eq('all')]
            actual=selected.set_index('metric')
            q1,q3=values.quantile([.25,.75]);iqr=q3-q1;sd=values.std(ddof=1)
            expected={'measurement_count':len(values),'mean':values.mean(),'median':values.median(),
                      'std_ddof1':sd,'q1':q1,'q3':q3,'iqr':iqr,'zero_fraction':values.eq(0).mean(),
                      'sample_skewness':values.skew(),'sample_excess_kurtosis':values.kurt()}
            for metric,value in expected.items():
                np.testing.assert_allclose(actual.loc[metric,'value'],value,rtol=1e-8,atol=1e-8,equal_nan=True)
                shape_checks+=1
            iq=actual.loc['iqr_review_fraction']
            if iqr==0:
                assert pd.isna(iq['value']) and iq['status']=='unavailable_zero_or_missing_scale'
            else:
                expected_flags=int(((values<q1-config['iqr_multiplier']*iqr)|(values>q3+config['iqr_multiplier']*iqr)).sum())
                assert iq['numerator']==expected_flags
            assert actual.loc['zscore_review_fraction','numerator']==int(((values-values.mean()).abs()>config['zscore_threshold']*sd).sum())
    daily['period']=pd.to_datetime(daily['observed_date']).dt.strftime('%Y-%m')
    count_checks=0
    for (station,period,element,unit),rows in daily.groupby(['station','period','event_type','severity_unit']):
        item=story[story['station'].eq(station)&story['period'].eq(period)&story['event_type'].eq(element)].iloc[0]
        assert item['record_count']==len(rows)
        np.testing.assert_allclose(item['mean_value'],rows['severity_value'].mean(),rtol=1e-9)
        if element=='PRCP':np.testing.assert_allclose(item['precipitation_total_mm'],rows['severity_value'].sum(),rtol=1e-9)
        count_checks+=1
    text_checks={}
    if receipt['identity'].get('text_inputs'):
        text_frames=[]
        for name,expected in receipt['identity']['text_inputs'].items():
            p=ROOT/name
            assert hashlib.sha256(p.read_bytes()).hexdigest().upper()==expected
            frame=pd.read_parquet(p);frame['_text_file']=name
            text_frames.append(frame)
        text,text_snapshot_rows=reconcile_text_snapshots(text_frames)
        assert not text.duplicated(['source','source_key']).any()
        assert set(text['source_key']).issubset(set(current.loc[current.source.eq('noaa_storm_events'),'source_key']))
        selected=story[story.source.eq('noaa_storm_events')]
        for label in ('positive','neutral','negative'):
            assert selected[label+'_count'].sum()==text.sentiment_label.eq(label).sum()
        assert selected.text_record_count.sum()==text.raw_text.notna().sum()
        for _,row in text.iterrows():
            assert row.token_count==len(row.tokens)
        text_checks={'text_rows':len(text),'text_snapshot_rows':text_snapshot_rows,
                     'repeated_text_snapshot_rows':text_snapshot_rows-len(text),
                     'text_records':int(text.raw_text.notna().sum()),
                     'sentiment_distribution':{label:int(text.sentiment_label.eq(label).sum())
                                               for label in ('positive','neutral','negative')},
                     'keyword_json_rows':int(selected.top_keywords_json.notna().sum())}
    output=dict(manifest=path.relative_to(ROOT).as_posix(),manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest().upper(),
        counts=receipt['counts'],gold_rows={k:len(v) for k,v in tables.items()},
        matching_pandas_shape_statistics=shape_checks,matching_station_month_groups=count_checks,
        matching_storm_month_type_unit_groups=monthly_event_groups,
        output_hashes_verified=True,unique_gold_keys=True,source_record_totals_reconciled=True,
        no_temperature_or_event_magnitude_sums=True,zero_iqr_not_fabricated=True,
        text_checks=text_checks,weather_network=False,
        method='Independent Pandas reconciliation of verified Silver folder and text sidecar')
    target=ROOT/args.receipt
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
