"""Audit Workshop 1 examples against immutable local evidence; never use network.

Run from the repository with the Workshop 1 Python environment. This verifies
record claims and reproducibility, not student approval or semantic event matches.
"""
import json
from pathlib import Path

import pandas as pd

from compare_daily_sources import build_pairs, sha

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / 'workshop_1/samples'
EXPECTED = {
    'noaa_storm_events/details_sample.csv': '987F5C641B6B85BF89477A823B52757D50D2C5376895FD53056A9AFE9F79403A',
    'region_comparison/ghcn_okc_usw00013967_2025.csv': 'D8EE9E0AFBFE25897C17BABE4A88DC0E12D4FECE8B74C26E8D817D5309FFB5AE',
    'nws_alerts/recent_7d_page_1.geojson': '70AD394CF9E7399ACCB5CEA7B0A3B8E55526F01C314E68136439EA8442E966C3',
    'nws_kden_observations_poll1.geojson': 'ED3B125ABEB90803B649F0E81D0146667517F8F16D6C35AD0448882B09C080B7',
    'nws_kden_observations_poll2.geojson': '83099D933716E406DDE6541FA0AA1A16FA9EAE28DA11797ED4D5D595DE1AA870',
    'region_comparison/nws_kokc_observations_snapshot.geojson': '391C49B75E7E05C225FE0EB63BB7BB822004169FFBB0F8FF6DDA006F236B0E68',
    'region_comparison/nws_kokc_observations_poll_2.geojson': '7857DD85FB4F35E33FA4A0EEFB0F07E6634E457D96F6A0D4C30560B5CDD07D79',
    'candidate_pairs/nws_kokc_observations_page_2.geojson': 'A13720F4E561AC3B20E56DD15F9D43224A1EF1ABE84D37E58DF5BF5FE38BA5CD',
    'region_comparison/ghcn_okc_usw00013967_2026_overlap.csv': '7456D668D4253550881435F5E9BFC95371965B7EBE72F1F8E060872F4A2D8D55',
}


def features(relative):
    return json.loads((SAMPLES / relative).read_text(encoding='utf-8-sig'))['features']


def main():
    for relative, expected in EXPECTED.items():
        assert sha(SAMPLES / relative) == expected, relative
    observations = []

    def record(identifier, source_paths, record_ids, observation, interpretation):
        observations.append(dict(example_id=identifier, source_paths=source_paths,
                                 record_ids=record_ids, observation=observation,
                                 interpretation=interpretation, verification='passed'))

    ghcn_path = 'region_comparison/ghcn_okc_usw00013967_2025.csv'
    row = pd.read_csv(SAMPLES / ghcn_path).set_index('DATE').loc['2025-01-05']
    assert row.PRCP == 0.0 and row.PRCP_ATTRIBUTES == 'T,,W,2400'
    record('Q1', [ghcn_path], ['USW00013967/2025-01-05/PRCP'],
           {'PRCP': 0.0, 'attributes': row.PRCP_ATTRIBUTES},
           'Trace precipitation semantics; flag loss would conflate trace with ordinary zero, not prove invalid provider data.')
    noaa_path = 'noaa_storm_events/details_sample.csv'
    row = pd.read_csv(SAMPLES / noaa_path).set_index('EVENT_ID').loc[1155350]
    assert row.EVENT_TYPE == 'Heavy Snow' and row.CZ_TYPE == 'Z' and row.CZ_NAME == 'CIMARRON'
    assert pd.isna(row.BEGIN_LAT) and pd.isna(row.BEGIN_LON)
    record('Q2', [noaa_path], ['1155350'],
           {'event_type': row.EVENT_TYPE, 'cz_type': row.CZ_TYPE, 'begin_lat': None, 'begin_lon': None},
           'Missing point coordinates for a zone event; preserve zone rather than invent a point.')
    alerts_path = 'nws_alerts/recent_7d_page_1.geojson'
    suffix = '06189d945720161.001.1'
    alert = next(f for f in features(alerts_path) if f['id'].endswith(suffix))
    assert alert['geometry'] is None and alert['properties']['event'] == 'Wind Advisory'
    assert len(alert['properties']['affectedZones']) == 7
    record('Q3', [alerts_path], [alert['id']], {'geometry': None, 'affected_zone_count': 7},
           'Missing polygon with alternative zone geography; not proof of absent location or provider corruption.')
    kden_id = 'https://api.weather.gov/stations/KDEN/observations/2026-11-04T01:53:00+00:00'
    kden_paths = ['nws_kden_observations_poll1.geojson', 'nws_kden_observations_poll2.geojson']
    versions = [next(f for f in features(p) if f['id'] == kden_id) for p in kden_paths]
    before, after = [f['properties']['temperature'] for f in versions]
    assert before['value'] is None and before['qualityControl'] == 'Z'
    assert after['value'] == 4.4 and after['qualityControl'] == 'V' and after['unitCode'] == 'wmoUnit:degC'
    record('Q4', kden_paths, [kden_id], {'before': before, 'after': after},
           'Same-ID revision/value availability; cause unknown, retain payload versions.')
    kokc_path = 'region_comparison/nws_kokc_observations_snapshot.geojson'
    ordered = sorted(features(kokc_path), key=lambda f: pd.Timestamp(f['properties']['timestamp']))
    index = next(i for i, f in enumerate(ordered) if '2026-11-03T21:52:00' in f['id'])
    first, second = ordered[index:index + 2]
    assert '2026-11-03T22:55:00' in second['id']
    gap = (pd.Timestamp(second['properties']['timestamp']) - pd.Timestamp(first['properties']['timestamp'])).total_seconds() / 60
    assert gap == 63
    record('Q5', [kokc_path], [first['id'], second['id']], {'adjacent_gap_minutes': gap},
           'Observed sampling irregularity; no five-minute provider guarantee or missing-record cause established.')
    extrema = {k: first['properties'][k] for k in ['maxTemperatureLast24Hours', 'minTemperatureLast24Hours']}
    assert all(v['value'] is None for v in extrema.values())
    record('Q6', [kokc_path], [first['id']], extrema,
           'Optional 24-hour fields unavailable; preserve null, not zero. Additional availability example.')

    rebuilt, coverage, exclusions = build_pairs()
    saved = pd.read_csv(SAMPLES / 'candidate_pairs/cross_source_candidate_pairs.csv')
    pd.testing.assert_frame_equal(rebuilt, saved, check_dtype=False)
    assert len(saved) == 8 and saved.date.nunique() == 4
    assert not saved.duplicated(['date', 'element']).any()
    assert set(saved.element) == {'TMAX', 'TMIN'}
    assert saved.groupby('date').size().eq(2).all()
    assert saved.source_a.ne(saved.source_b).all()
    assert saved.match_status.eq('candidate_not_confirmed').all()
    required = ['record_a_id', 'record_b_id', 'extreme_observation_id', 'time_difference',
                'position_difference', 'identifier_difference', 'nws_minus_ghcn_degC',
                'ghcn_unit', 'nws_unit', 'day_start_utc', 'day_end_utc_exclusive']
    assert saved[required].notna().all().all()
    kokc = {f['id']: f for p in [kokc_path, 'region_comparison/nws_kokc_observations_poll_2.geojson',
                               'candidate_pairs/nws_kokc_observations_page_2.geojson'] for f in features(p)}
    for pair in saved.itertuples():
        assert pair.extreme_observation_id in kokc
        assert kokc[pair.extreme_observation_id]['properties']['temperature']['value'] == pair.nws_value

    inputs = {str((SAMPLES/p).relative_to(ROOT)).replace('\\', '/'): sha(SAMPLES/p) for p in EXPECTED}
    for p in ['candidate_pairs/cross_source_candidate_pairs.csv', 'region_comparison/source_metadata.yaml']:
        inputs[str((SAMPLES/p).relative_to(ROOT)).replace('\\', '/')] = sha(SAMPLES/p)
    result = dict(input_sha256=inputs, quality_examples=observations,
                  daily_pairs=dict(reproduced_rows=len(saved), distinct_days=saved.date.nunique(),
                                   elements=sorted(saved.element.unique()), exclusions=exclusions,
                                   coverage=coverage.to_dict('records'),
                                   record_b='Derived daily aggregate, not an original NWS event record; raw extreme ID retained.',
                                   rubric_status='Traceability/count verified; same-real-world-event interpretation remains open.',
                                   limitations=['Fixed CST boundary assumed, not independently verified.',
                                                'Station/sensor equivalence not established.',
                                                'Eight element/day comparisons are not eight independent events.',
                                                'No PRCP total or confirmed event match claimed.']),
                  approval_status='No new student or professor approval recorded by this audit.')
    destination = SAMPLES / 'candidate_pairs/submission_evidence_audit.json'
    destination.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Verified: 9 captured-input hashes; Q1-Q6 source claims; 8 reproduced rows over 4 days; no approval inferred.')
    print('Audit SHA-256:', sha(destination))


if __name__ == '__main__':
    main()
