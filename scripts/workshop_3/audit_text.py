"""Record exact bounded NOAA narrative findings from saved Silver text Parquet."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]


def main():
    manifest=json.loads((ROOT/'workshop_3/samples/silver_text/noaa_oklahoma_2021_text.manifest.json').read_text())
    path=ROOT/manifest['path']
    if hashlib.sha256(path.read_bytes()).hexdigest().upper()!=manifest['sha256']:
        raise ValueError('text_silver_hash_mismatch')
    frame=pd.read_parquet(path)
    if len(frame)!=manifest['rows'] or frame.source_key.duplicated().any():
        raise ValueError('text_silver_row_identity_mismatch')
    lengths=frame.characters.dropna()
    keywords=Counter(token for tokens in frame.tokens for token in tokens)
    proof={
        'source':'NOAA Storm Events Oklahoma 2021 registered CSV subset',
        'native_capture_sha256':manifest['source_capture_sha256'],
        'text_silver_sha256':manifest['sha256'],
        'source_rows':len(frame),
        'nonempty_selected_narratives':int(frame.raw_text.notna().sum()),
        'event_narrative_rows':int(frame.text_field.eq('EVENT_NARRATIVE').sum()),
        'episode_fallback_rows':int(frame.text_field.eq('EPISODE_NARRATIVE').sum()),
        'characters':{'mean':float(lengths.mean()),'median':float(lengths.median()),
                      'min':int(lengths.min()),'max':int(lengths.max())},
        'lexical_tone_counts':{label:int(frame.sentiment_label.eq(label).sum())
                               for label in ('positive','neutral','negative')},
        'top_tokens':keywords.most_common(10),
        'method':'VADER 3.3.2 raw English narrative; 0.05/-0.05 thresholds; not hazard severity',
        'scope_limit':'2021 Oklahoma sample only; no labelled sentiment validation or full historical text coverage',
        'weather_network':False,
    }
    target=ROOT/'workshop_3/evidence/text_quality.json'
    target.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'rows':proof['source_rows'],'tone':proof['lexical_tone_counts']}))


if __name__=='__main__':main()
