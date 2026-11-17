"""Persist source domains, immutable accepted revisions and per-run sightings."""
import json


def persist_details(cursor, *, record_id, run_id, capture_id, record, unchanged):
    raw=record['raw_fields']
    # On an unchanged replay, the revision stays tied to its original accepted
    # run/capture. Only missing legacy parsed payload may be filled in.
    cursor.execute('''INSERT INTO historical_record_revision
        (record_id,run_id,capture_id,source_content_sha256,normalized_fields,raw_fields)
        SELECT record_id,last_run_id,capture_id,source_content_sha256,to_jsonb(h),%s::jsonb
        FROM historical_record h WHERE record_id=%s
        ON CONFLICT (record_id,run_id) DO UPDATE
        SET raw_fields=coalesce(historical_record_revision.raw_fields,EXCLUDED.raw_fields)
        WHERE historical_record_revision.source_content_sha256=EXCLUDED.source_content_sha256
        RETURNING revision_id''',
        (json.dumps(raw),record_id))
    revision=cursor.fetchone()[0]
    cursor.execute('''INSERT INTO record_capture_link
        (record_id,run_id,capture_id,source_line,unchanged,revision_id) VALUES (%s,%s,%s,%s,%s,%s)''',
        (record_id,run_id,capture_id,record['source_line'],unchanged,revision))
    if record['source']=='noaa_storm_events':
        geography=None
        codes=[raw.get(k) for k in ['STATE_FIPS','CZ_TYPE','CZ_FIPS']]
        if all(codes):
            cursor.execute('''INSERT INTO source_geography
                (source_id,state_code,geography_type,geography_code,geography_name)
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (source_id,state_code,geography_type,geography_code)
                DO UPDATE SET geography_name=EXCLUDED.geography_name RETURNING geography_id''',
                (record['source'],*codes,raw.get('CZ_NAME')))
            geography=cursor.fetchone()[0]
        impacts={k:raw.get(k) for k in ['DEATHS_DIRECT','DEATHS_INDIRECT','INJURIES_DIRECT','INJURIES_INDIRECT']}
        cursor.execute('''INSERT INTO storm_event
            (record_id,source_event_id,episode_id,geography_id,magnitude_type,
             damage_property_raw,damage_crops_raw,impact_fields,source_fields)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb)
            ON CONFLICT (record_id) DO UPDATE SET
              episode_id=EXCLUDED.episode_id,geography_id=EXCLUDED.geography_id,
              magnitude_type=EXCLUDED.magnitude_type,damage_property_raw=EXCLUDED.damage_property_raw,
              damage_crops_raw=EXCLUDED.damage_crops_raw,impact_fields=EXCLUDED.impact_fields,
              source_fields=EXCLUDED.source_fields''',
            (record_id,record['source_key'],raw.get('EPISODE_ID'),geography,
             record.get('magnitude_type'),raw.get('DAMAGE_PROPERTY'),raw.get('DAMAGE_CROPS'),
             json.dumps(impacts),json.dumps(raw)))
    else:
        cursor.execute('''INSERT INTO station(source_id,source_station_id,station_name)
            VALUES (%s,%s,%s) ON CONFLICT (source_id,source_station_id)
            DO UPDATE SET station_name=coalesce(EXCLUDED.station_name,station.station_name)
            RETURNING station_id''',(record['source'],raw['STATION'],raw.get('NAME')))
        station=cursor.fetchone()[0]
        cursor.execute('''INSERT INTO station_location_observation
            (station_id,capture_id,latitude,longitude,elevation_raw) VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (station_id,capture_id) DO NOTHING''',
            (station,capture_id,record['latitude'],record['longitude'],raw.get('ELEVATION')))
        cursor.execute('''INSERT INTO daily_station_measurement
            (record_id,station_id,observation_date,element_code,value,unit,attributes,source_fields)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s::jsonb)
            ON CONFLICT (record_id) DO UPDATE SET value=EXCLUDED.value,unit=EXCLUDED.unit,
              attributes=EXCLUDED.attributes,source_fields=EXCLUDED.source_fields''',
            (record_id,station,record['observed_date'],record['event_type'],
             record['severity_value'],record['severity_unit'],record.get('quality_attributes'),json.dumps(raw)))
