"""Audit saved NWS timestamps against request bounds, without network access."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def main():
    evidence=json.loads((ROOT/'workshop_3/evidence/incremental_live.json').read_text(encoding='utf-8'))
    station=next(r for r in evidence['runs'] if r['query']['source']=='nws_station_observations')
    window=station['pages'][0]['window']
    parse=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'))
    lower,upper=parse(window['start_utc']),parse(window['end_utc'])
    values=[];outside=[];hashes={}
    for page in station['pages']:
        path=ROOT/'data/raw'/page['raw_path'];body=path.read_bytes()
        actual=hashlib.sha256(body).hexdigest().upper();assert actual==page['sha256'].upper()
        hashes[path.relative_to(ROOT).as_posix()]=actual
        for f in json.loads(body.decode('utf-8-sig'))['features']:
            stamp=parse(f['properties']['timestamp']);values.append(stamp)
            if stamp<lower or stamp>upper:
                outside.append({'source_key':f['id'],'timestamp':stamp.isoformat(),
                                'position':'before_requested_start' if stamp<lower else 'after_requested_end'})
    proof={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'weather_network':False,
           'requested_window':window,'returned_records':len(values),
           'within_requested_interval':sum(lower<=t<=upper for t in values),
           'before_requested_start':sum(t<lower for t in values),
           'after_requested_end':sum(t>upper for t in values),
           'minimum_observed_at_utc':min(values).isoformat(),'maximum_observed_at_utc':max(values).isoformat(),
           'outside_records':outside,'input_sha256':hashes,
           'handling':'Preserve all returned records and raw evidence; analytics must apply explicit timestamp filters. Complete pagination does not prove all timestamps satisfy request bounds.',
           'interpretation':'Observed response/request-boundary discrepancy; cause not verified.'}
    (ROOT/'workshop_3/evidence/nws_window_review.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:proof[k] for k in ('returned_records','within_requested_interval','before_requested_start','after_requested_end')}))


if __name__=='__main__':main()
