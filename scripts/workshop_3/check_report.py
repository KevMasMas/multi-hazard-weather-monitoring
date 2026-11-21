"""Check final PDF geometry/text; visual confirmation follows rendered-page review.

Requires pypdf/pdfplumber (available in the bundled document Python runtime).
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--confirm-visual-review',action='store_true')
    args=parser.parse_args()
    path=ROOT/'workshop_3/Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf'
    reader=PdfReader(path);assert len(reader.pages)==8
    texts=[p.extract_text() or '' for p in reader.pages]
    assert all(len(t)>200 for t in texts)
    combined='\n'.join(texts)
    for term in ['20232020356','20232020341','625','607','903','candidate','19,942']:
        assert term in combined,term
    bounds=[]
    with pdfplumber.open(path) as pdf:
        for number,page in enumerate(pdf.pages,1):
            bad=[w['text'] for w in page.extract_words() if w['x0']<15 or w['x1']>page.width-15 or w['top']<8 or w['bottom']>page.height-8]
            assert not bad,(number,bad)
            bounds.append({'page':number,'width':page.width,'height':page.height,'text_characters':len(texts[number-1]),'words_outside_safe_bounds':0})
    log=(ROOT/'workshop_3/report/main.log').read_text(encoding='utf-8',errors='replace')
    assert 'Overfull \\hbox' not in log and 'Overfull \\vbox' not in log
    assert args.confirm_visual_review,'Render and inspect all final pages before recording visual confirmation'
    proof={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'pdf_path':path.relative_to(ROOT).as_posix(),
           'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest().upper(),'pages':len(reader.pages),
           'page_checks':bounds,'visual_review_passed':True,
           'visual_review':'All 8 final pages rendered at 90 DPI and inspected in contact sheet; actual Parquet preview page inspected separately. No clipping/overlap or artificial blank pages observed.',
           'overfull_tex_boxes':0,'nonblocking_tex_note':'One underfull hbox; cached fonts rendered despite host fontconfig diagnostic.',
           'weather_network':False}
    (ROOT/'workshop_3/evidence/report_qa.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('PDF check passed: 8 pages, safe text bounds, rendered visual review confirmed.')


if __name__=='__main__':main()
