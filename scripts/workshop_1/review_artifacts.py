"""Bounded current-tree/Overleaf secret and artifact scan, offline.

This does not certify absence of every secret or scan remote GitHub history.
Only finding locations/rules are reported; matched credential text is omitted.
"""
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT/'deliveries/01-workshop-1/final_artifact_audit.json'
RULES = {
    'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github_token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'),
    'aws_access_key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'google_api_key': re.compile(r'\bAIza[A-Za-z0-9_-]{35}\b'),
    'slack_token': re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
    'credential_assignment': re.compile(r'''(?im)^\s*["']?(?:api_key|api_token|access_token|client_secret|password)["']?\s*[:=]\s*["']([^"'\s]{12,})["']'''),
    'url_password': re.compile(r'\b(?:postgres(?:ql)?|mysql|https?)://[^\s:/]+:([^\s@/]+)@'),
}


def run(git='git'):
    raw = subprocess.check_output([git,'ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT)
    paths = sorted({p.decode('utf-8') for p in raw.split(b'\0') if p})
    findings, forbidden, placeholders, scanned = [], [], [], []

    def scan(label, body):
        if b'\x00' in body[:2000]:
            return
        try:
            text = body.decode('utf-8-sig')
        except UnicodeDecodeError:
            return
        scanned.append(label)
        for rule, pattern in RULES.items():
            for match in pattern.finditer(text):
                line = text[:match.start()].count('\n')+1
                if rule == 'url_password' and match.group(1) == 'weather' and label == '.env.example':
                    placeholders.append(dict(path=label,line=line,reason='Documented weather/weather local example, not a live credential.'))
                    continue
                findings.append(dict(path=label,line=line,rule=rule))

    for relative in paths:
        path = ROOT/relative
        if not path.is_file() or path == OUTPUT:
            continue
        parts = Path(relative).parts
        if '.venv' in parts or '__pycache__' in parts or path.name == '.env' or (relative.startswith('data/raw/') and path.name != '.gitkeep'):
            forbidden.append(relative)
        if path.suffix == '.zip':
            with zipfile.ZipFile(path) as archive:
                for entry in archive.infolist():
                    if not entry.is_dir():
                        scan(relative+'!'+entry.filename,archive.read(entry))
        elif path.stat().st_size < 8_000_000:
            scan(relative,path.read_bytes())
    ignore_probes = ['.env','.venv/probe','data/raw/probe.csv','__pycache__/probe.pyc']
    ignored = [p for p in ignore_probes if subprocess.run([git,'check-ignore','-q',p],cwd=ROOT).returncode == 0]
    result = dict(scope='Current tracked/unignored working-tree files and text in ZIP deliverables; not full Git history or a guarantee of no secrets.',
                  indexed_paths=len(paths),text_items_scanned=len(scanned),high_confidence_findings=findings,
                  forbidden_delivery_paths=forbidden,documented_placeholders=placeholders,
                  ignored_probes=ignored,expected_ignore_probes=ignore_probes,
                  source_revision=subprocess.check_output([git,'rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    OUTPUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Artifact review:',len(scanned),'text items;',len(findings),'findings;',len(forbidden),'forbidden paths;',len(ignored),'of 4 ignore probes.')
    assert not findings and not forbidden and len(ignored)==4, 'Review finding locations in the audit JSON; no credential text is printed.'
    return result


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--git',default='git')
    run(parser.parse_args().git)
