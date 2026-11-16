"""Reproduce five source-record wind candidates from saved evidence, offline.

The original NOAA archive is needed only for --extract. Normal reproduction
uses the small derived NOAA subset and the unchanged cached NCEI response.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'workshop_1/samples/candidate_pairs'
ARCHIVE = ROOT / 'data/raw/noaa_storm_events/details/year=2024/StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz'
ARCHIVE_HASH = '2070B83ECCAB041B36360AB73645B9A249C3EEFC5B92B5B3FC0CBBA4D9FCC09C'
IDS = [1170737, 1178563, 1178565, 1178567, 1180427]
GHCN_HASH = 'CD9E68A7FB43343E3E64D3633DF45AF08D21F97E5B6ED9D43B75E4CF82D0CCC2'
SUBSET = DEST / 'noaa_kokc_wind_events_2024.csv'
GHCN = DEST / 'ghcn_kokc_wind_2024.csv'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()


def extract():
    assert sha(ARCHIVE) == ARCHIVE_HASH
    data = pd.read_csv(ARCHIVE, low_memory=False)
    subset = data[data.EVENT_ID.isin(IDS)].sort_values('EVENT_ID')
    assert len(subset) == 5 and subset.EVENT_NARRATIVE.str.contains('KOKC').all()
    subset.to_csv(SUBSET, index=False, lineterminator='\n')
    meta = dict(evidence_type='derived_source_subset', archive_path=str(ARCHIVE.relative_to(ROOT)),
                archive_sha256=ARCHIVE_HASH, source_url='https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz',
                archive_retrieved_at='2026-11-04T13:56:42-05:00',
                selection='Five 2024 Oklahoma measured-wind records explicitly naming KOKC; fixed EVENT_ID list.',
                event_ids=IDS, sha256=sha(SUBSET), rows=5,
                qualification='Parsed subset, not an untouched original HTTP response; archive hash is preserved.')
    SUBSET.with_suffix('.metadata.json').write_text(json.dumps(meta, indent=2)+'\n', encoding='utf-8')


def build_pairs():
    meta = json.loads(SUBSET.with_suffix('.metadata.json').read_text())
    assert sha(SUBSET) == meta['sha256'] and sha(GHCN) == GHCN_HASH
    storm, ghcn = pd.read_csv(SUBSET), pd.read_csv(GHCN)
    result = []
    for number, event_id in enumerate(IDS, 1):
        e = storm.set_index('EVENT_ID').loc[event_id]
        assert e.STATE == 'OKLAHOMA' and e.MAGNITUDE_TYPE == 'MG' and e.SOURCE == 'ASOS'
        assert 'KOKC' in e.EVENT_NARRATIVE and e.CZ_TIMEZONE == 'CST-6'
        local = pd.to_datetime(e.BEGIN_DATE_TIME, format='%d-%b-%y %H:%M:%S')
        day = local.strftime('%Y-%m-%d')
        g = ghcn.set_index('DATE').loc[day]
        assert g.STATION == 'USW00013967' and 'WILL ROGERS' in g.NAME
        assert pd.notna(g.WSF5) and str(g.WSF5_ATTRIBUTES).split(',')[1] == ''
        utc = local.tz_localize('UTC') + pd.Timedelta(hours=6)
        point = pd.notna(e.BEGIN_LAT) and pd.notna(e.BEGIN_LON)
        distance = None
        if point:
            la1, la2 = math.radians(e.BEGIN_LAT), math.radians(g.LATITUDE)
            delta_la, delta_lo = la2-la1, math.radians(g.LONGITUDE-e.BEGIN_LON)
            a = math.sin(delta_la/2)**2 + math.cos(la1)*math.cos(la2)*math.sin(delta_lo/2)**2
            distance = 6371*2*math.asin(min(1, math.sqrt(a)))
        storm_mps = float(e.MAGNITUDE)*0.5144444444444445
        result.append(dict(pair_id=f'WIND-{number:02}', source_a='NOAA Storm Events', record_a_id=str(event_id),
            source_b='GHCN-Daily', record_b_id=f'USW00013967/{day}/WSF5',
            event_type=e.EVENT_TYPE, episode_id=int(e.EPISODE_ID), local_date=day,
            event_local_time=str(local), event_timezone=e.CZ_TIMEZONE, event_time_utc=utc.isoformat(),
            ghcn_date=day, ghcn_peak_time_available=pd.notna(g.PGTM),
            time_difference='Timed gust versus same labelled date daily fastest-5-second wind; exact GHCN peak time unavailable.',
            ghcn_daily_boundary='Same local-date candidate rule; daily wind accumulation boundary not independently verified.',
            position_difference='Zone event has no point; narrative explicitly names KOKC, compare with station point.' if not point else 'Event point versus GHCN airport station point; same airport named in narrative.',
            noaa_latitude=e.BEGIN_LAT if point else None, noaa_longitude=e.BEGIN_LON if point else None,
            ghcn_latitude=float(g.LATITUDE), ghcn_longitude=float(g.LONGITUDE),
            point_distance_km=round(distance,4) if distance is not None else None,
            noaa_magnitude_knots=float(e.MAGNITUDE), noaa_magnitude_type=e.MAGNITUDE_TYPE,
            noaa_magnitude_mps=round(storm_mps,4), ghcn_wsf5_mps=float(g.WSF5),
            ghcn_minus_noaa_mps=round(float(g.WSF5)-storm_mps,4), ghcn_wsf5_attributes=g.WSF5_ATTRIBUTES,
            identifier_difference='Storm EVENT_ID versus station/date/WSF5; no shared event identifier.',
            candidate_basis='Same named airport, labelled local date and compatible wind magnitude; common station reporting lineage possible.',
            match_status='candidate_not_confirmed', independence='Distinct data products; not independent sensors or independent episodes.',
            source_a_path=str(SUBSET.relative_to(ROOT)).replace('\\','/'),
            source_b_path=str(GHCN.relative_to(ROOT)).replace('\\','/')))
    pairs = pd.DataFrame(result)
    assert len(pairs) == 5 and pairs.record_a_id.nunique() == 5
    assert pairs.record_b_id.nunique() == 3
    return pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract', action='store_true')
    if parser.parse_args().extract:
        extract()
    pairs = build_pairs()
    pairs.to_csv(DEST/'historical_wind_candidate_pairs.csv', index=False, lineterminator='\n')
    tex = [r'\subsection{Source-record wind-event candidates}',
           'Five Storm Events records explicitly name the KOKC airport and report measured ASOS wind gusts. They are paired with original GHCN daily WSF5 records for USW00013967, whose returned name and coordinates identify Will Rogers Airport. These are stronger same-weather-episode candidates than generic daily temperature comparisons, not confirmed exact-gust matches or independent sensor validation.',
           r'\begin{longtable}{llL{2.4cm}rrr}',
           r'\toprule Pair & EVENT\_ID & Local date/time & NOAA (kn) & GHCN (m/s) & $\Delta$ (m/s) \\ \midrule\endhead']
    for r in pairs.itertuples():
        tex.append(f'{r.pair_id} & {r.record_a_id} & {r.local_date} {r.event_local_time[11:16]} & {r.noaa_magnitude_knots:.0f} & {r.ghcn_wsf5_mps:.1f} & {r.ghcn_minus_noaa_mps:+.2f} '+r'\\')
    tex += [r'\bottomrule\end{longtable}',
        r'\textbf{Time:} NOAA times are CST-6; UTC adds six hours. GHCN has a daily date and null PGTM, so no exact peak timestamp or exact time delta is invented. The same-labelled-local-date rule is provisional; the daily wind boundary is not independently verified.',
        r'\textbf{Position:} four event points are about 0.02 km from the returned station point. The High Wind record has zone geography and no point; its narrative names KOKC, and no event coordinate or zero distance is fabricated.',
        r'\textbf{Magnitude/identifier:} NOAA measured gusts (MG) in knots convert using 0.5144444444 m/s per knot. GHCN metric WSF5 is fastest 5-second wind, not an identical gust definition. $\Delta$ is GHCN minus converted NOAA. EVENT\_ID differs from station/date/WSF5; all IDs, flags, coordinates, UTC times and file references are in the CSV.',
        'Five pairs use five distinct Storm Events IDs but only three GHCN daily records and three labelled dates. Three May 6 gust reports share one daily summary and may describe one episode. The products can share ASOS reporting lineage. The guide asks for candidate record pairs, not five independent episodes; under that interpretation these are the five proposed overlap examples. Professor acceptance and exact-event equivalence are not asserted.',
        r'Full evidence: \path{workshop_1/samples/candidate_pairs/historical_wind_candidate_pairs.csv}; the NOAA file is a checksum-linked parsed subset of the saved archive, and GHCN CSV is the unchanged newly captured response.']
    (ROOT/'workshop_1/report/historical_pairs.tex').write_text('\n\n'.join(tex)+'\n',encoding='utf-8')
    print(pairs[['pair_id','record_a_id','record_b_id','noaa_magnitude_mps','ghcn_wsf5_mps','ghcn_minus_noaa_mps']].to_string(index=False))


if __name__ == '__main__':
    main()
