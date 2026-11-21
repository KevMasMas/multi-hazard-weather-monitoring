"""Versioned candidate relationships; no ground-truth event assignment."""
import csv
import hashlib
import json
from pathlib import Path
from psycopg2.extras import Json
from .incremental import digest


def build_candidates(connection, namespace='replay'):
    """One closest observation per alert whose polygon contains its station.

    Effective/expires is an alert-validity interval, not proof an impact occurred.
    Missing polygon receives no county-name or nearest-point fallback.
    """
    rule='nws_polygon_validity_v1'
    with connection.cursor() as c:
        c.execute('''SELECT DISTINCT ON (a.record_id) a.source_key,b.source_key,
            a.normalized_fields,b.normalized_fields,a.source_content_sha256,
            b.source_content_sha256,b.observed_at_utc
            FROM incremental_record a JOIN incremental_record b
              ON a.namespace=b.namespace
             AND a.source_id='nws_alerts' AND b.source_id='nws_station_observations'
             AND a.geometry IS NOT NULL AND b.geometry IS NOT NULL
             AND ST_Covers(a.geometry,b.geometry)
             AND b.observed_at_utc BETWEEN (a.normalized_fields->>'effective')::timestamptz
                                         AND (a.normalized_fields->>'expires')::timestamptz
            WHERE a.namespace=%s
            ORDER BY a.record_id,abs(extract(epoch FROM b.observed_at_utc -
                          (a.normalized_fields->>'effective')::timestamptz)),b.source_key''',(namespace,))
        pairs=[]
        for left,right,alert,observation,left_hash,right_hash,stamp in c.fetchall():
            key=digest([rule,namespace,left,right,left_hash.strip(),right_hash.strip()])
            evidence={'relationship':'intra_NWS_temporal_spatial_association',
                      'independence':'same NWS API; not independent source evidence',
                      'geometry_rule':'ST_Covers(alert polygon, station point)',
                      'time_rule':'observation inside effective/expires interval',
                      'observation_timestamp':stamp.isoformat(),
                      'alert_severity':alert.get('severity'),
                      'station_measurements':observation['measurements'],
                      'left_content_sha256':left_hash.strip(),'right_content_sha256':right_hash.strip(),
                      'limitation':'Association does not verify an impact or a shared physical event.'}
            c.execute('''INSERT INTO event_candidate(candidate_key,rule_version,namespace,left_source,left_key,right_source,right_key,evidence)
                         VALUES(%s,%s,%s,'nws_alerts',%s,'nws_station_observations',%s,%s) ON CONFLICT DO NOTHING''',
                      (key,rule,namespace,left,right,Json(evidence)))
            pairs.append({'candidate_key':key,'left_id':left,'right_id':right,'rule_version':rule,'review_status':'candidate_not_confirmed',**evidence})
    connection.commit()
    return pairs


def import_historical_context(connection, root: Path):
    """Index the five W1 reviewed candidate rows without changing their meaning.

    This is traceable context reuse, not five newly discovered W3 matches.
    The original W1 reproduction and checksums remain the evidence authority.
    """
    relative='workshop_1/samples/candidate_pairs/historical_wind_candidate_pairs.csv'
    path=root/relative
    from .sources.capture_registry import registered_hashes
    from .storage.raw_landing import require_registered_capture
    body=path.read_bytes()
    require_registered_capture(body,relative,registered_hashes(root))
    rows=list(csv.DictReader(body.decode('utf-8-sig').splitlines()))
    with connection.cursor() as c:
        for row in rows:
            rule='w1_named_airport_daily_wind_v1'
            evidence={'original_pair':row,'origin':relative,'sha256':hashlib.sha256(body).hexdigest(),
                      'reuse':'previous W1 candidates, not new matches',
                      'limitation':'Daily peak time/boundary unverified; distinct products can share reporting lineage.'}
            key=digest([rule,row['record_a_id'],row['record_b_id'],evidence['sha256']])
            c.execute('''INSERT INTO event_candidate(candidate_key,rule_version,namespace,left_source,left_key,right_source,right_key,evidence)
                         VALUES(%s,%s,'historical_context','noaa_storm_events',%s,'ghcn_daily',%s,%s) ON CONFLICT DO NOTHING''',
                      (key,rule,row['record_a_id'],row['record_b_id'],Json(evidence)))
    connection.commit()
    return len(rows)
