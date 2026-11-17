"""Build literal layer excerpts offline; preserve the original sample/notebook bytes."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def main():
    samples=ROOT/'workshop_2/samples'
    manifest=json.loads((samples/'manifest.json').read_text())
    entry=next(e for e in manifest['entries'] if e['partition']=='OK_2021')
    bronze=samples/entry['bronze']; silver=samples/entry['silver']
    for path,key in [(bronze,entry['bronze']),(silver,entry['silver'])]:
        assert hashlib.sha256(path.read_bytes()).hexdigest().upper()==manifest['files'][key]['sha256']
    rows=json.loads(bronze.read_text())['rows'][:2]
    excerpt=[];omitted=[]
    for number,row in enumerate(rows,1):
        item=row.copy()
        for field in ['EPISODE_NARRATIVE','EVENT_NARRATIVE']:
            if len(item.get(field,''))>72:
                item[field]=item[field][:72]+'...'
                omitted.append(dict(record=number,field=field,retained_prefix_characters=72))
        excerpt.append(item)
    notebook=ROOT/'notebooks/02_historical_ingestion_review.ipynb'
    nb=json.loads(notebook.read_text())
    def content(value):return ''.join(value) if isinstance(value,list) else value
    cell=next(c for c in nb['cells'] if 'display(storms.head())' in content(c['source']))
    head=next(content(o['data']['text/plain']) for o in cell['outputs'] if 'text/plain' in o.get('data',{}))
    cell=next(c for c in nb['cells'] if 'storms.info()' in content(c['source']))
    info=''.join(content(o['text']) for o in cell['outputs'] if o['output_type']=='stream')
    assert head and info and not any(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'])
    folder=ROOT/'workshop_2/report/assets'
    fragments={'bronze_excerpt.json':json.dumps(excerpt,indent=2,ensure_ascii=True)+'\n',
               'silver_head.txt':head+'\n','silver_info.txt':info}
    for name,text in fragments.items():(folder/name).write_text(text,encoding='utf-8',newline='\n')
    def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
    provenance=dict(purpose='Offline report excerpts, not new source responses or pipeline runs.',
        inputs={p.relative_to(ROOT).as_posix():digest(p) for p in [bronze,silver,notebook]},
        fragments={name:digest(folder/name) for name in fragments},
        narrative_omissions=omitted,
        silver_output='Literal text/plain head() and info() outputs copied from the executed notebook; not regenerated.',
        fragment_hash_scope='Fragment hashes identify excerpts; input hashes identify complete unchanged files.')
    (ROOT/'workshop_2/evidence/layer_excerpt_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    lines=[r'\appendix',r'\section{Sample layer content}',
        'The excerpts below come from the submitted files. Input SHA-256 values identify the complete files, not the displayed fragments. No input values have been recomputed.',
        r'\subsection{Bronze JSON: first two records}',
        r'Source: \path{'+bronze.relative_to(ROOT).as_posix()+'}.',
        r'Complete-file SHA-256: \path{'+digest(bronze)+'}.',
        'All fields from the first two entries of the saved JSON rows array are shown. For narrative strings longer than 72 characters, only the unchanged 72-character prefix is displayed followed by "...". The ellipsis denotes omitted content; the saved file remains unchanged.',
        r'{\scriptsize\begin{verbatim}',fragments['bronze_excerpt.json'].rstrip(),r'\end{verbatim}}',
        r'\subsection{Silver Parquet: literal Pandas output}',
        r'Source: \path{'+silver.relative_to(ROOT).as_posix()+'}.',
        r'Complete-file SHA-256: \path{'+digest(silver)+'}.',
        r'Output source: \path{notebooks/02_historical_ingestion_review.ipynb}.',
        r'The recorded cells display \path{storms.head()} and call \path{storms.info()}.',
        r'Notebook SHA-256: \path{'+digest(notebook)+'}.',
        'The following head() and info() text is copied literally from the executed notebook. Pandas column-display ellipses are part of that recorded output; they do not indicate changed data.',
        r'{\scriptsize\begin{verbatim}',head,r'\end{verbatim}}',
        r'{\scriptsize\begin{verbatim}',info.rstrip(),r'\end{verbatim}}']
    (ROOT/'workshop_2/report/layer_appendix.tex').write_text('\n\n'.join(lines)+'\n')
    print('Two literal Bronze records and recorded Silver head/info copied; input hashes verified.')


if __name__=='__main__':main()
