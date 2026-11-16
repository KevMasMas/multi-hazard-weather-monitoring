"""Capture one authorized NCEI response and compare saved daily temperatures.

No network is used unless --fetch is explicitly supplied. Existing captures are
reused with checksum verification. No automatic retries are performed.
"""
import argparse
import hashlib
import json
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT/'workshop_1/samples'
CSV = SAMPLES/'region_comparison/ghcn_okc_usw00013967_2026_overlap.csv'
META = CSV.with_suffix('.metadata.json')
URL = ('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries'
       '&stations=USW00013967&startDate=2026-10-31&endDate=2026-11-05'
       '&format=csv&units=metric&includeAttributes=true&includeStationName=true')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def capture():
    if CSV.exists():
        assert sha(CSV) == json.loads(META.read_text())['sha256']
        print('Using checksum-verified cached response')
        return
    request = Request(URL, headers={'User-Agent': 'multi-hazard-weather-monitoring/0.1 (github.com/KevMasMas/multi-hazard-weather-monitoring)'})
    started = datetime.now(timezone.utc).isoformat()
    with urlopen(request, timeout=90) as response:
        body = response.read()
        status = response.status
        headers = {key: value for key, value in response.headers.items()
                   if key.lower() in {'date','content-type','content-length','etag','last-modified'}}
    CSV.write_bytes(body)
    META.write_text(json.dumps(dict(request_url=URL, request_method='GET',
        requested_at_utc=started, captured_at_utc=datetime.now(timezone.utc).isoformat(),
        http_status=status, response_headers=headers, sha256=sha(CSV), bytes=len(body),
        retries=0), indent=2)+'\n', encoding='utf-8')
    print('Captured once:', status, len(body), sha(CSV))


def build_pairs():
    metadata = json.loads(META.read_text())
    assert sha(CSV) == metadata['sha256']
    ghcn = pd.read_csv(CSV)
    files = [SAMPLES/'candidate_pairs/nws_kokc_observations_page_2.geojson',
             SAMPLES/'region_comparison/nws_kokc_observations_snapshot.geojson',
             SAMPLES/'region_comparison/nws_kokc_observations_poll_2.geojson']
    features = {}
    conflicts = []
    expected_hashes = ['A13720F4E561AC3B20E56DD15F9D43224A1EF1ABE84D37E58DF5BF5FE38BA5CD',
        '391C49B75E7E05C225FE0EB63BB7BB822004169FFBB0F8FF6DDA006F236B0E68',
        '7857DD85FB4F35E33FA4A0EEFB0F07E6634E457D96F6A0D4C30560B5CDD07D79']
    for path, expected in zip(files, expected_hashes):
        assert sha(path) == expected, f'Captured NWS checksum mismatch: {path}'
    for path in files:
        for feature in json.loads(path.read_text(encoding='utf-8-sig'))['features']:
            key = feature['id']
            if key in features and feature != features[key]:
                conflicts.append(key)
            features[key] = feature
    # Conflicting versions are excluded rather than choosing a temperature silently.
    for key in set(conflicts):
        features.pop(key, None)
    observations = []
    exclusions = dict(null_temperature=0, qc_not_selected=0, unsupported_unit=0,
                      conflicting_ids=len(set(conflicts)))
    for key, feature in features.items():
        p = feature['properties']
        t = pd.Timestamp(p['timestamp']).tz_convert('UTC')
        item = p.get('temperature') or {}
        if item.get('value') is None:
            exclusions['null_temperature'] += 1
            continue
        if item.get('qualityControl') != 'V':
            exclusions['qc_not_selected'] += 1
            continue
        if item.get('unitCode') != 'wmoUnit:degC':
            exclusions['unsupported_unit'] += 1
            continue
        observations.append(dict(id=key, utc=t, day=(t-pd.Timedelta(hours=6)).date().isoformat(),
            temperature=float(item['value']), coordinates=feature['geometry']['coordinates']))
    df = pd.DataFrame(observations).sort_values('utc')
    coverage, pairs = [], []
    for day in pd.date_range('2026-10-31','2026-11-05'):
        date = day.date().isoformat()
        start = pd.Timestamp(date, tz='UTC') + pd.Timedelta(hours=6)
        stop = start + pd.Timedelta(days=1)
        group = df[df.day == date].sort_values('utc')
        gaps = [1440.] if group.empty else [
            (group.utc.iloc[0]-start).total_seconds()/60,
            *group.utc.diff().dropna().dt.total_seconds().div(60).tolist(),
            (stop-group.utc.iloc[-1]).total_seconds()/60]
        maximum_gap = max(gaps)
        eligible = len(group) >= 48 and maximum_gap <= 70
        coverage.append(dict(date=date, valid_temperature_observations=len(group),
            max_gap_including_edges_minutes=maximum_gap, eligible=eligible,
            reason='passes proposed sampling coverage threshold' if eligible else 'fewer than 48 valid readings or gap greater than 70 minutes'))
        if not eligible:
            continue
        match = ghcn[ghcn.DATE == date]
        if len(match) != 1:
            continue
        row = match.iloc[0]
        for element, operation in [('TMAX','max'),('TMIN','min')]:
            if element not in row or pd.isna(row[element]):
                continue
            attrs = str(row.get(element+'_ATTRIBUTES','')).split(',')
            if len(attrs)>1 and attrs[1].strip():
                continue
            index = getattr(group.temperature, 'idx'+operation)()
            extreme = group.loc[index]
            lon,lat = extreme.coordinates[:2]
            station_metadata = yaml.safe_load((SAMPLES/'region_comparison/source_metadata.yaml').read_text())['ghcn_daily']
            glat,glon = float(station_metadata['latitude']),float(station_metadata['longitude'])
            a = math.sin(math.radians(lat-glat)/2)**2 + math.cos(math.radians(lat))*math.cos(math.radians(glat))*math.sin(math.radians(lon-glon)/2)**2
            distance = 6371*2*math.asin(min(1,math.sqrt(a)))
            value = float(row[element])
            pairs.append(dict(pair_id=f'CROSS-{len(pairs)+1:02}',date=date,element=element,
                source_a='GHCN-Daily',record_a_id=f'USW00013967/{date}/{element}',
                source_b='NWS KOKC daily aggregate',record_b_id=f'KOKC/{date}/{element}',
                observation_id_first=group.id.iloc[0],observation_id_last=group.id.iloc[-1],
                extreme_observation_id=extreme.id,extreme_timestamp_utc=extreme.utc.isoformat(),
                day_start_utc=start.isoformat(),day_end_utc_exclusive=stop.isoformat(),
                time_difference='same assumed CST day; daily summary versus sampled instantaneous extreme',
                seconds_from_day_start=(extreme.utc-start).total_seconds(),
                ghcn_latitude=glat,ghcn_longitude=glon,nws_latitude=lat,nws_longitude=lon,
                station_distance_km=round(distance,4),position_difference='two source station identifiers; equivalence not established',
                ghcn_value=value,ghcn_unit='degC',nws_value=extreme.temperature,nws_unit='degC',
                nws_minus_ghcn_degC=round(extreme.temperature-value,4),ghcn_attributes=row.get(element+'_ATTRIBUTES',''),
                nws_qc='V',valid_observation_count=len(group),max_gap_minutes=maximum_gap,
                identifier_difference='GHCN station/date/element versus derived NWS day/element and observation ID range',
                match_status='candidate_not_confirmed',daily_boundary_status='assumed_fixed_CST_per_review; provider boundary not independently established'))
    return pd.DataFrame(pairs),pd.DataFrame(coverage),exclusions


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fetch',action='store_true')
    args=parser.parse_args()
    if args.fetch:
        capture()
    if not CSV.exists():
        raise SystemExit('No cached response. Authorized capture command: python scripts/workshop_1/compare_daily_sources.py --fetch')
    pairs,coverage,exclusions=build_pairs()
    destination=SAMPLES/'candidate_pairs'
    pairs.to_csv(destination/'cross_source_candidate_pairs.csv',index=False,lineterminator='\n')
    coverage.to_csv(destination/'daily_coverage.csv',index=False,lineterminator='\n')
    (destination/'daily_comparison_metadata.json').write_text(json.dumps(dict(
        ghcn_sha256=sha(CSV),input_nws_hashes={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in [
        SAMPLES/'candidate_pairs/nws_kokc_observations_page_2.geojson',SAMPLES/'region_comparison/nws_kokc_observations_snapshot.geojson',SAMPLES/'region_comparison/nws_kokc_observations_poll_2.geojson']},
        coverage_rule='at least 48 QC V temperature readings; maximum gap including day edges 70 minutes',
        boundary='fixed CST UTC-6, 06:00Z to next 06:00Z; review assumption',exclusions=exclusions,
        precipitation='not aggregated: null/overlapping accumulation windows and gaps',pairs=len(pairs)),indent=2)+'\n')
    print(coverage.to_string(index=False)); print('Exclusions:',exclusions); print('Pairs:',len(pairs))
    tex = [r'\subsection{Supplementary daily temperature comparisons}',
        'One authorized NCEI capture supplies daily summaries for 2026-10-31 through 2026-11-05. Saved KOKC pages are deduplicated by observation ID; conflicting versions would be excluded. We assume fixed CST days (UTC minus six hours), from 06:00Z to the next 06:00Z, as specified for this review. Provider daily boundaries and station equivalence have not been independently established.',
        'The proposed sampling-coverage rule requires at least 48 valid temperatures and no gap, including day edges, greater than 70 minutes. Only unitCode wmoUnit:degC and QC V are accepted. This is a screening criterion, not proof that every continuous daily extreme was observed. One non-V temperature was excluded; no null temperatures or conflicting IDs were found in the combined saved pages.',
        'October 31, November 1, 3 and 4 qualify; November 2 is excluded for a 75-minute gap and November 5 is partial. Precipitation is not aggregated because overlapping windows and missing observations prevent a reliable total. Official 24-hour max/min fields from NWS are not used.',
        r'\begin{longtable}{llL{2cm}rrrr}',
        r'\toprule Date & Element & UTC window & N & GHCN ($^{\circ}$C) & KOKC ($^{\circ}$C) & $\Delta$ ($^{\circ}$C) \\',
        r'\midrule\endhead']
    for _,row in pairs.iterrows():
        tex.append(f"{row['date']} & {row['element']} & 06:00--06:00 & {row['valid_observation_count']} & {row['ghcn_value']:.1f} & {row['nws_value']:.1f} & {row['nws_minus_ghcn_degC']:+.1f} " + r'\\')
    tex += [r'\bottomrule\end{longtable}',
        r'Each row compares one date/element, not a distinct weather episode. GHCN identifiers use \path{USW00013967/date/element}; NWS identifiers use \path{KOKC/date/element} plus first, last and extreme observation IDs in the submitted CSV. GHCN flags and NWS QC are preserved there. The GHCN coordinates are taken from the saved 2025 station metadata because this new response does not include coordinate columns; that historical position is not a newly verified station location.',
        f"The station-point distance computed from those saved coordinates and the extreme observation point is about {pairs.station_distance_km.iloc[0]:.2f} km. Coordinate proximity does not establish equivalent sensors, exposure or reporting practice. Time differences are daily-summary versus point-sampling granularity; the CSV retains the exact extreme timestamps and seconds from the assumed day boundary.",
        'A sampled KOKC maximum may be lower than a daily GHCN maximum, and a sampled minimum may be higher. Boundary conventions, sampling and station differences can also reverse those differences. These eight rows are candidates, not ground truth. No polygon containment or station equivalence is claimed. Appendix A retains the earlier intra-NWS examples separately.',
        'The NWS side is a derived daily aggregate with a traceable raw extreme observation, not an original daily event record. These eight supplementary comparisons are not counted toward the five primary wind-event candidate examples above and are not eight independent events.',
        r'Full comparison and coverage: \path{workshop_1/samples/candidate_pairs/cross_source_candidate_pairs.csv} and \path{daily_coverage.csv}.']
    (ROOT/'workshop_1/report/daily_pairs.tex').write_text('\n\n'.join(tex)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
