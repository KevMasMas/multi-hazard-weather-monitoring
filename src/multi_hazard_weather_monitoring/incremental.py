"""NWS snapshots: immutable pages, transactional revisions and conservative state.

Network access occurs only through fetch_pages(), never while reading replay data.
Saved incomplete snapshots can be profiled, but cannot advance a coverage watermark.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from psycopg2.extras import Json

SOURCES = {
    'nws_alerts': 'https://api.weather.gov/alerts',
    'nws_station_observations': 'https://api.weather.gov/stations/KOKC/observations',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def utc(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timestamp_requires_offset')
    return parsed.astimezone(timezone.utc)


def allowed_url(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'api.weather.gov' or parsed.port not in (None, 443) or parsed.username or parsed.password or parsed.fragment:
        raise ValueError('untrusted_nws_url')
    return url


def decode_page(body):
    page = json.loads(body.decode('utf-8-sig'))
    if not isinstance(page, dict) or page.get('type') != 'FeatureCollection' or not isinstance(page.get('features'), list):
        raise ValueError('invalid_feature_collection')
    pagination = page.get('pagination') or {}
    if not isinstance(pagination, dict):
        raise ValueError('invalid_pagination')
    if pagination.get('next'):
        allowed_url(pagination['next'])
    return page


def fetch_pages(url, root: Path, source: str, scope: str, user_agent: str,
                opener=urlopen, sleeper=time.sleep, max_pages=20, on_page=None):
    """Bounded GET with retries; retain every successful body before parsing.

    Retry-After exceeding five minutes is surfaced, rather than retried too early.
    A partial pagination chain never reaches the database success path.
    """
    if not user_agent.strip():
        raise ValueError('NWS_USER_AGENT_required')
    pages, seen = [], set()
    for _ in range(max_pages):
        allowed_url(url)
        if url in seen:
            raise ValueError('pagination_cycle')
        seen.add(url)
        for attempt in range(4):
            try:
                request = Request(url, headers={'User-Agent': user_agent, 'Accept': 'application/geo+json'})
                with opener(request, timeout=30) as response:
                    body = response.read()
                break
            except (HTTPError, URLError, TimeoutError) as exc:
                if isinstance(exc, HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                    raise
                delay = min(60, 5 * 2 ** attempt)
                if isinstance(exc, HTTPError) and exc.headers.get('Retry-After'):
                    from email.utils import parsedate_to_datetime
                    retry = exc.headers['Retry-After']
                    delay = int(retry) if retry.isdigit() else max(0, (parsedate_to_datetime(retry) - datetime.now(timezone.utc)).total_seconds())
                    if delay > 300:
                        raise RuntimeError('retry_after_exceeds_poll_budget') from exc
                if attempt == 3:
                    raise
                sleeper(delay)
        page = save_page(root, source, scope, body, url, datetime.now(timezone.utc).isoformat())
        pages.append(page)
        if on_page:
            on_page(page)
        decoded = decode_page(body)
        url = (decoded.get('pagination') or {}).get('next')
        if not url:
            return pages
    raise ValueError('pagination_page_limit')


def save_page(root, source, scope, body, origin, retrieved_at):
    from .storage.raw_landing import land_capture
    # Origin/timestamp belong to poll receipts, not the content-addressed identity.
    capture = land_capture(body, source=source, partition=scope, root=root / 'data/raw',
                           content_type='application/geo+json', origin='nws_response_bytes')
    return {**capture, 'origin': origin, 'retrieved_at_utc': retrieved_at, 'body': body}


def normalize(feature, source, scope):
    if not isinstance(feature, dict) or feature.get('type') != 'Feature':
        raise ValueError('invalid_feature')
    p = feature.get('properties')
    if not isinstance(p, dict):
        raise ValueError('missing_properties')
    key = feature.get('id') or p.get('@id')
    if not isinstance(key, str) or not key:
        raise ValueError('missing_source_id')
    allowed_url(key)
    geometry = feature.get('geometry')
    if source == 'nws_alerts':
        if not key.startswith('https://api.weather.gov/alerts/') or not p.get('event'):
            raise ValueError('invalid_alert_identity')
        stamp = utc(p['sent'])
        for field in ('effective','onset','expires','ends'):
            if p.get(field):
                utc(p[field])
        if not p.get('effective') or not p.get('expires') or utc(p['effective']) > utc(p['expires']):
            raise ValueError('invalid_alert_interval')
        if geometry is not None and geometry.get('type') not in ('Polygon','MultiPolygon'):
            raise ValueError('invalid_alert_geometry_type')
        normalized = {k: p.get(k) for k in ('sent','effective','onset','expires','ends','event','severity','certainty','urgency','status','messageType','affectedZones','geocode','references')}
        kind = p['event']
    elif source == 'nws_station_observations':
        station = p.get('stationId') or str(p.get('station', '')).rsplit('/',1)[-1]
        if station != scope or not key.startswith(f'https://api.weather.gov/stations/{scope}/observations/'):
            raise ValueError('station_scope_mismatch')
        stamp = utc(p['timestamp'])
        if not geometry or geometry.get('type') != 'Point':
            raise ValueError('missing_station_point')
        lon, lat = geometry['coordinates'][:2]
        if not all(isinstance(v, (int,float)) and math.isfinite(v) for v in (lon,lat)) or not (-180 <= lon <= 180 and -90 <= lat <= 90):
            raise ValueError('invalid_coordinates')
        quantities = {}
        conversions = {'wmoUnit:degC': ('degC',1,0), 'wmoUnit:degF': ('degC',5/9,-32*5/9),
                       'wmoUnit:K': ('degC',1,-273.15), 'wmoUnit:km_h-1': ('m/s',1/3.6,0),
                       'wmoUnit:m_s-1': ('m/s',1,0), 'wmoUnit:kt': ('m/s',1852/3600,0),
                       'wmoUnit:mm': ('mm',1,0), 'wmoUnit:m': ('m',1,0),
                       'wmoUnit:Pa': ('Pa',1,0), 'wmoUnit:percent': ('%',1,0)}
        for name in ('temperature','dewpoint','windSpeed','windGust','precipitationLastHour','precipitationLast3Hours','precipitationLast6Hours','barometricPressure','relativeHumidity'):
            q = p.get(name)
            if not q:
                continue
            value, unit = q.get('value'), q.get('unitCode')
            if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value)):
                raise ValueError('invalid_measurement:'+name)
            entry = {'source_value':value,'source_unit':unit,'quality_control':q.get('qualityControl'), 'value':None,'unit':None,'conversion_status':'unsupported_unit'}
            if unit in conversions:
                outunit, scale, offset = conversions[unit]
                if name.startswith('precipitation') and unit=='wmoUnit:m':
                    outunit,scale,offset='mm',1000,0
                entry.update(value=None if value is None else value*scale+offset, unit=outunit, conversion_status='converted' if value is not None else 'missing')
            if entry['value'] is not None:
                converted=entry['value']
                if ((name in ('windSpeed','windGust') or name.startswith('precipitation')) and converted<0
                    or name=='relativeHumidity' and not 0<=converted<=100
                    or name=='barometricPressure' and converted<=0
                    or name in ('temperature','dewpoint') and entry['unit']=='degC' and converted < -273.15):
                    raise ValueError('physical_invalidity:'+name)
            quantities[name] = entry
        normalized = {'station':station,'timestamp':stamp.isoformat(),'measurements':quantities}
        kind = 'StationObservation'
    else:
        raise ValueError('unsupported_incremental_source')
    return {'source_key':key,'observed_at_utc':stamp,'event_type':kind,
            'geometry':geometry,'fields':normalized,'sha256':digest(feature)}


def register_source(cursor, source):
    cursor.execute('INSERT INTO source_catalog(source_id,source_url,source_format,attribution) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING',
                   (source,SOURCES[source],'GeoJSON','NOAA / National Weather Service'))


def failed_poll(connection, source, scope, namespace, queried_at, pages, error):
    connection.rollback()
    with connection.cursor() as c:
        register_source(c,source)
        c.execute('INSERT INTO incremental_poll(source_id,scope,namespace,queried_at_utc,status,coverage_complete,pages,error_code) VALUES(%s,%s,%s,%s,\'failed\',false,%s,%s)',
                  (source,scope,namespace,queried_at,Json([{k:v for k,v in p.items() if k!='body'} for p in pages]),type(error).__name__+':'+str(error)[:180]))
    connection.commit()


def persist_poll(connection, source, scope, namespace, queried_at, pages, complete):
    """One transaction per poll. Reject invalid features, abort invalid envelopes.

    Observed content is compared with the most recently committed sighting. An
    older query is forbidden from replacing newer state. Absence is not deletion.
    """
    stamp = utc(queried_at) if isinstance(queried_at,str) else queried_at
    if stamp.tzinfo is None or not pages or namespace not in ('replay','live','test'):
        raise ValueError('invalid_poll_contract')
    try:
        decoded = [decode_page(p['body']) for p in pages]
        for p in pages:
            if hashlib.sha256(p['body']).hexdigest() != p['sha256']:
                raise ValueError('page_hash_mismatch')
        if complete:
            for index, page in enumerate(decoded):
                next_url = (page.get('pagination') or {}).get('next')
                expected = pages[index+1]['origin'] if index+1 < len(pages) else None
                if next_url != expected:
                    raise ValueError('incomplete_pagination_chain')
        counts = dict(read=0,new=0,changed=0,unchanged=0,rejected=0)
        with connection.cursor() as c:
            c.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))',(source+':'+namespace+':'+scope,))
            register_source(c,source)
            c.execute("SELECT max(queried_at_utc) FROM incremental_poll WHERE source_id=%s AND namespace=%s AND scope=%s AND status='succeeded'",(source,namespace,scope))
            previous = c.fetchone()[0]
            if previous and stamp < previous:
                raise ValueError('out_of_order_query')
            c.execute("INSERT INTO incremental_poll(source_id,scope,namespace,queried_at_utc,status,coverage_complete,pages) VALUES(%s,%s,%s,%s,'succeeded',%s,%s) RETURNING poll_id",
                      (source,scope,namespace,stamp,complete,Json([{k:v for k,v in p.items() if k!='body'} for p in pages])))
            poll_id = c.fetchone()[0]
            seen = {}
            for page, capture in zip(decoded,pages):
                for index, feature in enumerate(page['features']):
                    counts['read'] += 1
                    try:
                        n = normalize(feature,source,scope)
                        if n['source_key'] in seen:
                            raise ValueError('duplicate_id_in_poll')
                        # PostGIS validates polygon coordinates before storage. Invalid geometry is quarantined.
                        c.execute('SAVEPOINT feature_geometry')
                        try:
                            c.execute('SELECT ST_IsValid(ST_SetSRID(ST_GeomFromGeoJSON(%s),4326)), ST_SRID(ST_GeomFromGeoJSON(%s))',
                                      (json.dumps(n['geometry']),json.dumps(n['geometry']))) if n['geometry'] else None
                            if n['geometry']:
                                valid, srid = c.fetchone()
                                if not valid or srid != 4326:
                                    raise ValueError('invalid_geometry')
                            c.execute('RELEASE SAVEPOINT feature_geometry')
                        except Exception:
                            c.execute('ROLLBACK TO SAVEPOINT feature_geometry')
                            c.execute('RELEASE SAVEPOINT feature_geometry')
                            raise ValueError('invalid_geometry')
                    except (ValueError,KeyError,TypeError,IndexError,AttributeError) as exc:
                        counts['rejected'] += 1
                        c.execute('INSERT INTO incremental_reject VALUES(%s,%s,%s,%s,%s)',(poll_id,capture['sha256'],index,str(exc)[:150],Json(feature)))
                        continue
                    seen[n['source_key']] = n['sha256']
                    c.execute('SELECT record_id,source_content_sha256 FROM incremental_record WHERE source_id=%s AND namespace=%s AND source_key=%s',(source,namespace,n['source_key']))
                    old = c.fetchone()
                    classification = 'new' if old is None else ('unchanged' if old[1].strip()==n['sha256'] else 'changed')
                    counts[classification] += 1
                    if old is None:
                        c.execute('INSERT INTO incremental_record(source_id,namespace,source_key,observed_at_utc,event_type,geometry,normalized_fields,source_content_sha256,last_poll_id) VALUES(%s,%s,%s,%s,%s,ST_SetSRID(ST_GeomFromGeoJSON(%s),4326),%s,%s,%s) RETURNING record_id',
                                  (source,namespace,n['source_key'],n['observed_at_utc'],n['event_type'],json.dumps(n['geometry']) if n['geometry'] else None,Json(n['fields']),n['sha256'],poll_id))
                        record_id=c.fetchone()[0]
                    else:
                        record_id=old[0]
                        c.execute('UPDATE incremental_record SET observed_at_utc=%s,event_type=%s,geometry=ST_SetSRID(ST_GeomFromGeoJSON(%s),4326),normalized_fields=%s,source_content_sha256=%s,last_poll_id=%s WHERE record_id=%s',
                                  (n['observed_at_utc'],n['event_type'],json.dumps(n['geometry']) if n['geometry'] else None,Json(n['fields']),n['sha256'],poll_id,record_id))
                    if classification != 'unchanged':
                        c.execute('INSERT INTO incremental_revision(record_id,poll_id,source_content_sha256,raw_fields,normalized_fields) VALUES(%s,%s,%s,%s,%s)',(record_id,poll_id,n['sha256'],Json(feature),Json(n['fields'])))
                    c.execute('INSERT INTO incremental_sighting VALUES(%s,%s,%s,%s,%s)',(poll_id,record_id,capture['sha256'],index,classification))
            c.execute('UPDATE incremental_poll SET rows_read=%s,rows_new=%s,rows_changed=%s,rows_unchanged=%s,rows_rejected=%s,completed_at_utc=clock_timestamp() WHERE poll_id=%s',
                      (*[counts[k] for k in ('read','new','changed','unchanged','rejected')],poll_id))
            if complete and not counts['rejected']:
                c.execute('INSERT INTO incremental_state VALUES(%s,%s,%s,%s,%s) ON CONFLICT(source_id,namespace,scope) DO UPDATE SET last_successful_query_at_utc=EXCLUDED.last_successful_query_at_utc,last_poll_id=EXCLUDED.last_poll_id',
                          (source,namespace,scope,stamp,poll_id))
        connection.commit()
        return {'poll_id':poll_id,'source':source,'namespace':namespace,'scope':scope,'queried_at_utc':stamp.isoformat(),'coverage_complete':complete,'watermark_advanced':complete and not counts['rejected'],**counts}
    except Exception as exc:
        failed_poll(connection,source,scope,namespace,stamp,pages,exc)
        raise


def replay(connection, root, manifest_path):
    manifest = json.loads(manifest_path.read_text())
    results=[]
    for poll in manifest['polls']:
        pages=[]
        for item in poll['pages']:
            path=(root/item['path']).resolve()
            if not path.is_relative_to(root.resolve()):
                raise ValueError('replay_path_outside_repository')
            body=path.read_bytes()
            if hashlib.sha256(body).hexdigest().upper()!=item['sha256'].upper():
                raise ValueError('replay_hash_mismatch')
            pages.append(save_page(root,poll['source'],poll['scope'],body,item['url'],item['retrieved_at_utc']))
        results.append(persist_poll(connection,poll['source'],poll['scope'],'replay',poll['queried_at_utc'],pages,poll['coverage_complete']))
    return results


def station_window(policy, stamp, state, last_full):
    retention_start=stamp-timedelta(days=policy['station_retention_days'])
    full=not last_full or stamp-last_full>=timedelta(hours=policy['full_reconciliation_hours'])
    start=retention_start if full or not state else max(retention_start,state-timedelta(hours=policy['station_overlap_hours']))
    return {'start_utc':start.isoformat(),'end_utc':stamp.isoformat(),
            'reconciliation':'full' if full else 'overlap',
            'retention_gap_before_utc':retention_start.isoformat() if state and state<retention_start else None}


def live(connection, root, source, scope):
    if source not in SOURCES or (source=='nws_alerts' and scope!='OK') or (source=='nws_station_observations' and not re.fullmatch('[A-Z0-9]{3,8}',scope)):
        raise ValueError('invalid_source_scope')
    policy=json.loads((root/'config/workshop3_incremental.json').read_text())
    if source=='nws_station_observations' and scope not in policy['stations']:
        raise ValueError('station_not_configured')
    stamp=datetime.now(timezone.utc)
    with connection.cursor() as c:
        c.execute("SELECT last_successful_query_at_utc FROM incremental_state WHERE source_id=%s AND namespace='live' AND scope=%s",(source,scope))
        state=c.fetchone()
        c.execute("SELECT max(queried_at_utc) FROM incremental_poll WHERE source_id=%s AND namespace='live' AND scope=%s AND status='succeeded' AND coverage_complete AND pages->0->'window'->>'reconciliation'='full'",(source,scope))
        last_full=c.fetchone()[0]
    connection.rollback()
    if source=='nws_alerts':
        url='https://api.weather.gov/alerts/active?area=OK'
    else:
        window=station_window(policy,stamp,state[0] if state else None,last_full)
        url=f'https://api.weather.gov/stations/{scope}/observations?'+urlencode({'start':window['start_utc'],'end':window['end_utc'],'limit':500})
    pages=[]
    try:
        pages=fetch_pages(url,root,source,scope,os.environ.get('NWS_USER_AGENT',''),on_page=pages.append)
        if source=='nws_station_observations':
            pages[0]['window']=window
    except Exception as exc:
        failed_poll(connection,source,scope,'live',stamp,pages,exc)
        raise
    return persist_poll(connection,source,scope,'live',stamp,pages,True)


def status(connection):
    with connection.cursor() as c:
        c.execute('SELECT source_id,namespace,scope,last_successful_query_at_utc,clock_timestamp()-last_successful_query_at_utc AS state_age FROM incremental_state ORDER BY 1,2,3')
        states=[dict(zip([d.name for d in c.description],r)) for r in c.fetchall()]
        c.execute('SELECT poll_id,source_id,namespace,scope,queried_at_utc,status,coverage_complete,rows_read,rows_new,rows_changed,rows_unchanged,rows_rejected,error_code FROM incremental_poll ORDER BY poll_id DESC LIMIT 20')
        polls=[dict(zip([d.name for d in c.description],r)) for r in c.fetchall()]
        c.execute('SELECT source_id,namespace,count(*) FROM incremental_record GROUP BY 1,2 ORDER BY 1,2')
        records=[{'source':r[0],'namespace':r[1],'records':r[2]} for r in c.fetchall()]
        c.execute('SELECT count(*) FROM incremental_revision')
        revisions=c.fetchone()[0]
    return {'states':states,'recent_polls':polls,'record_counts':records,'revision_count':revisions}
