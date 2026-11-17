"""Restore only the three packaged inputs to ignored storage, without network."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def main():
    samples = ROOT/'workshop_2/samples'
    manifest = json.loads((samples/'manifest.json').read_text())
    for entry in manifest['entries']:
        source = samples/entry['native']
        expected = manifest['files'][entry['native']]['sha256']
        if hashlib.sha256(source.read_bytes()).hexdigest().upper() != expected:
            raise ValueError('packaged_input_checksum_mismatch')
        destination = (ROOT/entry['original_input_path']).resolve()
        if not destination.is_relative_to((ROOT/'data/raw/acquired').resolve()):
            raise ValueError('unsafe_restore_path')
        if destination.exists() and destination.read_bytes() != source.read_bytes():
            raise ValueError('existing_input_conflict')
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        print(entry['partition'])


if __name__ == '__main__':
    main()
