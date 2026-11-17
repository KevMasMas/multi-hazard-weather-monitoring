"""Combine immutable Workshop 1 evidence with explicitly acquired W2 captures."""
import json


def registered_hashes(root):
    primary = root / 'workshop_1/samples/candidate_pairs/submission_evidence_audit.json'
    register = json.loads(primary.read_text())['input_sha256'].copy()
    acquired = root / 'workshop_2/evidence/historical_acquisition.json'
    if acquired.exists():
        for path, digest in json.loads(acquired.read_text())['input_sha256'].items():
            if path in register and register[path].upper() != digest.upper():
                raise ValueError('conflicting_capture_register')
            register[path] = digest
    return register
