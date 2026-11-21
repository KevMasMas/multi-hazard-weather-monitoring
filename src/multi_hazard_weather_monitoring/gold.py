"""Weather Gold summaries from verified Silver snapshots using Spark SQL only.

The input register freezes the successful exports reviewed in the quality
notebook. It excludes unreviewed files and records every byte hash in output
lineage. No source requests or database writes occur in this module.
"""
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import shutil
import tempfile

LOG=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]
SILVER_TYPES={
    'record_id':'bigint','source':'string','source_key':'string','event_type':'string',
    'observed_at_utc':'timestamp','observed_date':'date','latitude':'double','longitude':'double',
    'severity_value':'double','severity_unit':'string','magnitude_type':'string',
    'quality_attributes':'string','source_content_sha256':'string','capture_sha256':'string',
    'run_id':'bigint','capture_id':'bigint','source_line':'bigint','revision_id':'bigint'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verified_inputs(root, config):
    """Reject path escapes and altered/missing registered Parquet files."""
    register=(root/config['input_register']).resolve()
    if not register.is_relative_to(root.resolve()):
        raise ValueError('input_register_outside_project')
    entries=json.loads(register.read_text())['input_sha256']
    if not entries:
        raise ValueError('empty_silver_register')
    results=[]
    for relative, expected in sorted(entries.items()):
        path=(root/relative).resolve()
        if not path.is_relative_to((root/'data/curated/silver').resolve()) or path.suffix!='.parquet':
            raise ValueError('silver_path_outside_curated')
        if digest(path)!=expected.upper():
            raise ValueError('silver_checksum_mismatch:'+relative)
        results.append((relative,expected.upper()))
    return results


def create_spark(config):
    from pyspark.sql import SparkSession
    return (SparkSession.builder.appName('Team9WeatherGold')
            .master(config['spark_master'])
            .config('spark.driver.memory',config['driver_memory'])
            .config('spark.sql.shuffle.partitions',str(config['shuffle_partitions']))
            .config('spark.sql.session.timeZone','UTC')
            .config('spark.ui.enabled','false')
            .config('spark.driver.bindAddress','127.0.0.1')
            .config('spark.driver.host','127.0.0.1')
            .config('spark.sql.execution.arrow.pyspark.enabled','false')
            .getOrCreate())


def consolidate(spark, paths, start, end):
    from pyspark.sql import functions as F, Window
    # Inspect each schema before a common read: schema merging must not mask drift.
    for path in paths:
        schema=spark.read.parquet(str(path)).schema
        actual={f.name:f.dataType.simpleString() for f in schema}
        if actual!=SILVER_TYPES:
            raise ValueError('silver_schema_mismatch:'+str(path))
    raw=spark.read.parquet(*[str(p) for p in paths]).withColumn('_input_file',F.input_file_name())
    required=['source','source_key','event_type','record_id','run_id','revision_id','source_content_sha256']
    bad=None
    for field in required:
        condition=F.col(field).isNull()
        if field in ['source','source_key','event_type','source_content_sha256']:
            condition=condition | (F.trim(F.col(field))=='')
        bad=condition if bad is None else bad | condition
    if raw.filter(bad).limit(1).count():
        raise ValueError('invalid_silver_identity')
    if raw.filter(~F.col('source').isin('ghcn_daily','noaa_storm_events')).limit(1).count():
        raise ValueError('unsupported_gold_source')
    if raw.filter(F.col('observed_date').isNull()==F.col('observed_at_utc').isNull()).limit(1).count():
        raise ValueError('invalid_silver_time_grain')
    # Hashes cover source rows; check the normalized fields as well before ties.
    signature=F.sha2(F.to_json(F.struct(*[F.col(k) for k in SILVER_TYPES if k not in ['run_id','capture_id','capture_sha256','source_line']])),256)
    for keys in [['source','source_key','revision_id'],['source','source_key','run_id']]:
        conflict=(raw.withColumn('_signature',signature).groupBy(*keys)
                  .agg(F.countDistinct('_signature').alias('variants')).filter('variants > 1'))
        if conflict.limit(1).count():
            raise ValueError('conflicting_silver_snapshot')
    raw=raw.withColumn('_date',F.coalesce(F.col('observed_date'),F.to_date('observed_at_utc')))
    raw=raw.filter(F.col('_date').between(F.lit(start).cast('date'),F.lit(end).cast('date'))).cache()
    if not raw.limit(1).count():
        raise ValueError('empty_silver_scope')
    order=Window.partitionBy('source','source_key').orderBy(F.desc('run_id'),F.desc('_input_file'))
    current=raw.withColumn('_order',F.row_number().over(order)).filter('_order=1').drop('_order').cache()
    return raw,current


def governance(raw,current,config,batch_id):
    """Long-form, typed metrics; null value + status for undefined statistics."""
    from pyspark.sql import functions as F
    result=[]
    base_columns=['source','station','population','period','variable','unit','metric','value',
                  'numerator','denominator','method','status','batch_id']

    def metric(frame,name,value,numerator=None,denominator=None,method='exact_count',status=None):
        def col(value):return value if value is not None else F.lit(None).cast('double')
        defaults={'station':None,'population':'unique_source_records','period':'all',
                  'variable':None,'unit':None}
        for field,default in defaults.items():
            if field not in frame.columns:frame=frame.withColumn(field,F.lit(default).cast('string'))
        status=status if status is not None else F.lit('available')
        result.append(frame.select('source','station','population','period','variable','unit',
            F.lit(name).alias('metric'),col(value).cast('double').alias('value'),
            col(numerator).cast('double').alias('numerator'),col(denominator).cast('double').alias('denominator'),
            F.lit(method).alias('method'),status.alias('status'),F.lit(batch_id).alias('batch_id')))

    volumes=(raw.groupBy('source').agg(F.count('*').alias('snapshot_rows'))
             .join(current.groupBy('source').agg(F.count('*').alias('unique_rows'),
                   F.countDistinct('source_key').alias('distinct_keys')),'source'))
    metric(volumes,'snapshot_rows',F.col('snapshot_rows'),method='includes_replayed_exports')
    metric(volumes,'unique_records',F.col('unique_rows'),method='latest_successful_local_run_per_source_key')
    repeated=F.col('snapshot_rows')-F.col('unique_rows')
    metric(volumes,'repeated_snapshot_fraction',repeated/F.col('snapshot_rows'),repeated,F.col('snapshot_rows'),
           method='repeated_export_rows_not_independent_duplicate_events')
    duplicates=F.col('unique_rows')-F.col('distinct_keys')
    metric(volumes,'canonical_duplicate_key_fraction',duplicates/F.col('unique_rows'),duplicates,F.col('unique_rows'),
           method='source_key_uniqueness_after_deterministic_snapshot_selection')
    # A structural check, not a claim that domain QC flags have all passed.
    metric(volumes,'schema_compliance_fraction',F.lit(1.0),F.col('snapshot_rows'),F.col('snapshot_rows'),
           method='all_18_silver_types_and_required_identity_time_grain_checked_before_aggregation')
    fields=['observed_at_utc','observed_date','latitude','longitude','severity_value','severity_unit','quality_attributes']
    expressions=[F.count('*').alias('n')]+[F.sum(F.when(F.col(c).isNull(),1).otherwise(0)).alias(c) for c in fields]
    nulls=current.groupBy('source').agg(*expressions)
    for field in fields:
        metric(nulls.withColumn('variable',F.lit(field)),'null_fraction',F.col(field)/F.col('n'),F.col(field),F.col('n'),
               method='source_specific_missing_or_not_applicable_not_automatically_invalid')
    monthly=(current.withColumn('period',F.date_format('_date','yyyy-MM')).groupBy('source','period')
             .agg(F.count('*').alias('n')))
    metric(monthly,'monthly_records',F.col('n'))
    daily=(current.filter("source='ghcn_daily'").withColumn('station',F.split('source_key','/')[0])
           .withColumn('variable',F.col('event_type')).withColumn('unit',F.col('severity_unit')))
    if daily.limit(1).count():
        daily=daily.withColumn('_qc',F.coalesce(F.split('quality_attributes',',').getItem(1),F.lit('')))
        qc=daily.groupBy('source','station').agg(F.count('*').alias('n'),
            F.sum(F.when(F.col('_qc')!='',1).otherwise(0)).alias('flagged'))
        metric(qc,'provider_qc_flag_fraction',F.col('flagged')/F.col('n'),F.col('flagged'),F.col('n'),
               method='nonempty_second_attribute_component_retained_for_review')
        all_days=daily.withColumn('population',F.lit('all_days')).withColumn('period',F.lit('all'))
        positive=(daily.filter("event_type='PRCP' AND severity_value>0")
                  .withColumn('population',F.lit('positive_reported_precipitation')).withColumn('period',F.lit('all')))
        seasonal=daily.withColumn('population',F.lit('calendar_month')).withColumn('period',F.date_format('_date','MM'))
        populations=all_days.unionByName(positive).unionByName(seasonal).cache()
        groups=['source','station','population','period','variable','unit']
        values=populations.groupBy(*groups).agg(F.count('severity_value').alias('n'),
            F.avg('severity_value').alias('mean'),F.stddev_samp('severity_value').alias('std'),
            F.expr('percentile(severity_value, array(0.25,0.5,0.75))').alias('quantiles'),
            F.skewness('severity_value').alias('skew_pop'),F.kurtosis('severity_value').alias('kurt_pop'),
            F.sum(F.when(F.col('severity_value')==0,1).otherwise(0)).alias('zeros'))
        values=(values.withColumn('q1',F.col('quantiles')[0]).withColumn('median',F.col('quantiles')[1])
                .withColumn('q3',F.col('quantiles')[2]).withColumn('iqr',F.col('q3')-F.col('q1')))
        joined=populations.join(values,groups,'inner')
        k=config['iqr_multiplier'];z=config['zscore_threshold']
        counts=joined.groupBy(*groups).agg(
            F.sum(F.when((F.col('severity_value')<F.col('q1')-k*F.col('iqr')) |
                        (F.col('severity_value')>F.col('q3')+k*F.col('iqr')),1).otherwise(0)).alias('iqr_flags'),
            F.sum(F.when(F.abs(F.col('severity_value')-F.col('mean'))>z*F.col('std'),1).otherwise(0)).alias('z_flags'))
        values=values.join(counts,groups).cache()
        for name,column in [('measurement_count','n'),('mean','mean'),('median','median'),('std_ddof1','std'),
                            ('q1','q1'),('q3','q3'),('iqr','iqr')]:
            metric(values,name,F.col(column),method='exact_spark_sql_sample_std_linear_percentile')
        metric(values,'zero_fraction',F.col('zeros')/F.col('n'),F.col('zeros'),F.col('n'))
        n=F.col('n').cast('double')
        # Spark returns population moments; transform to Pandas' sample estimators.
        skew=F.sqrt(n*(n-1))/(n-2)*F.col('skew_pop')
        kurt=(n-1)/((n-2)*(n-3))*((n+1)*F.col('kurt_pop')+6)
        for name,expression,minimum in [('sample_skewness',skew,3),('sample_excess_kurtosis',kurt,4)]:
            available=(n>=minimum)&(F.col('std')>0)
            metric(values,name,F.when(available,expression),method='bias_corrected_sample_from_spark_population_moments',
                   status=F.when(available,'available').otherwise('unavailable_insufficient_or_constant'))
        for name,count,available,method in [
            ('iqr_review_fraction','iqr_flags',F.col('iqr')>0,f'linear_quartiles_{k}_iqr_review_only'),
            ('zscore_review_fraction','z_flags',F.col('std')>0,f'absolute_z_gt_{z}_sample_std_comparison_only')]:
            metric(values,name,F.when(available,F.col(count)/n),F.when(available,F.col(count)),n,method,
                   F.when(available,'available').otherwise('unavailable_zero_or_missing_scale'))
    frame=result[0]
    for other in result[1:]:frame=frame.unionByName(other)
    return frame.select(*base_columns)


def storytelling(current,batch_id):
    from pyspark.sql import functions as F
    monthly=(current.withColumn('period',F.date_format('_date','yyyy-MM'))
        .withColumn('station',F.when(F.col('source')=='ghcn_daily',F.split('source_key','/')[0]))
        .withColumn('geographic_scope',F.when(F.col('source')=='ghcn_daily','station_only').otherwise('Oklahoma_state')))
    groups=['source','station','geographic_scope','period','event_type','severity_unit']
    frame=monthly.groupBy(*groups).agg(F.count('*').alias('record_count'),
        F.count('severity_value').alias('measured_count'),F.avg('severity_value').alias('mean_value'),
        F.min('severity_value').alias('min_value'),F.max('severity_value').alias('max_value'),
        F.sum('severity_value').alias('_sum'),F.countDistinct('_date').alias('observed_dates'),
        F.sum(F.when(F.col('latitude').isNull(),1).otherwise(0)).alias('missing_point_count'))
    # A rain total is meaningful; summing temperatures or event magnitudes is not.
    return (frame.withColumn('precipitation_total_mm',F.when((F.col('source')=='ghcn_daily') &
        (F.col('event_type')=='PRCP') & (F.col('severity_unit')=='mm'),F.col('_sum')))
        .drop('_sum').withColumn('batch_id',F.lit(batch_id))
        .withColumn('analysis_type',F.lit('descriptive_not_forecast')))


def build_gold(root,batch_id,logical_time,config_path='config/workshop3_gold.json'):
    """Publish both outputs atomically in a batch folder; retries verify hashes."""
    root=Path(root).resolve()
    config_file=(root/config_path).resolve()
    if not config_file.is_relative_to((root/'config').resolve()):
        raise ValueError('gold_config_outside_project')
    config=json.loads(config_file.read_text())
    inputs=verified_inputs(root,config)
    moment=datetime.fromisoformat(logical_time)
    if moment.utcoffset() is None:raise ValueError('gold_logical_time_requires_timezone')
    stamp=moment.astimezone(timezone.utc).strftime('%Y%m%d_%H%M%S')
    token=hashlib.sha256(batch_id.encode()).hexdigest()[:12]
    identity=dict(batch_id=batch_id,logical_time=logical_time,config=config,
                  config_path=config_file.relative_to(root).as_posix(),config_sha256=digest(config_file),
                  input_register_sha256=digest(root/config['input_register']),
                  inputs=dict(inputs),implementation_sha256=digest(Path(__file__)))
    signature=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest().upper()
    output_root=root/'data/gold';output_root.mkdir(parents=True,exist_ok=True)
    target=output_root/f'{stamp}_{token}'
    if target.exists():
        receipt=json.loads((target/'manifest.json').read_text())
        if receipt['signature']!=signature:raise ValueError('gold_batch_identity_conflict')
        for item in receipt['outputs'].values():
            if digest(root/item['path'])!=item['sha256']:raise ValueError('gold_existing_output_corrupt')
        LOG.info('Reused committed Gold batch %s',batch_id)
        return str(target/'manifest.json')
    staging=Path(tempfile.mkdtemp(prefix='.gold_pending_',dir=output_root))
    spark=None
    try:
        spark=create_spark(config);spark.sparkContext.setLogLevel('WARN')
        raw,current=consolidate(spark,[root/p for p,_ in inputs],config['start'],config['end'])
        counts=dict(snapshot_rows=raw.count(),unique_business_records=current.count(),
                    source_counts={row['source']:row['count'] for row in current.groupBy('source').count().collect()})
        counts['repeated_snapshot_rows']=counts['snapshot_rows']-counts['unique_business_records']
        outputs={}
        for name,frame in [('governance',governance(raw,current,config,batch_id)),
                           ('storytelling',storytelling(current,batch_id))]:
            frame=frame.cache()
            rows=frame.count()
            if not rows:raise ValueError('empty_gold_'+name)
            filename=f'{name}_{stamp}_{token}.parquet'
            output=staging/filename
            # Hadoop chmod is unsupported on some Windows bind mounts. Compute
            # parts on Linux /tmp, then copy only the finished file to staging.
            with tempfile.TemporaryDirectory(prefix='weather_spark_') as temporary:
                directory=Path(temporary)/'parts'
                frame.orderBy(*[column for column in frame.columns if column not in ['value']][:6]).coalesce(1).write.mode('error').parquet(str(directory))
                parts=list(directory.glob('part-*.parquet'))
                if len(parts)!=1:raise ValueError('single_summary_part_required')
                shutil.copyfile(parts[0],output)
            restored=spark.read.parquet(str(output))
            if restored.count()!=rows or restored.columns!=frame.columns:
                raise ValueError('gold_parquet_roundtrip_mismatch')
            outputs[name]=dict(path=(target/filename).relative_to(root).as_posix(),rows=rows,
                               sha256=digest(output),bytes=output.stat().st_size,schema=frame.schema.jsonValue())
            frame.unpersist()
        receipt=dict(signature=signature,identity=identity,outputs=outputs,counts=counts,
            generated_at_utc=datetime.now(timezone.utc).isoformat(),spark_version=spark.version,
            spark_configuration={key:(spark.conf.get(key) if key.startswith('spark.sql.')
                else spark.sparkContext.getConf().get(key)) for key in ['spark.master','spark.driver.memory',
                'spark.sql.shuffle.partitions','spark.sql.session.timeZone']},
            limitations=['One GHCN station; no county assignments or forecasting.',
                'Reviewed registered historical snapshot; not an automatically expanding input folder.',
                'Review flags preserve extremes; missing-inapplicable columns remain explicit.'])
        (staging/'manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
        # Check inputs again before publishing so a concurrent mutation is not ignored.
        if verified_inputs(root,config)!=inputs:raise ValueError('gold_inputs_changed_during_run')
        os.replace(staging,target)
        LOG.info('Published Gold %s: %s',batch_id,counts)
        return str(target/'manifest.json')
    finally:
        try:
            if spark is not None:spark.stop()
        finally:
            if staging.exists():shutil.rmtree(staging)
