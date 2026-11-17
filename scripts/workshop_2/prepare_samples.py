"""Copy three actual Airflow outputs and their unchanged CSV inputs for review."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def main():
    proof = json.loads((ROOT/'workshop_2/evidence/historical_airflow_runs.json').read_text())
    config = json.loads((ROOT/'config/workshop2_saved_captures.json').read_text())['captures']
    samples = ROOT/'workshop_2/samples'
    manifest = dict(schema='workshop2-samples-v1', description='Three genuine successful Airflow runs; not copies of one batch.',
                    entries=[], files={})
    for partition in ['OK_2021', 'USW00013967_2021_full', 'USW00013967_2022_full']:
        run = next(r for r in proof['runs'] if r['partition'] == partition)
        if run['bronze']['state'] != 'success' or run['silver']['state'] != 'success':
            raise ValueError('sample_run_not_successful')
        source = next(c for c in config if c['partition'] == partition)
        output = run['output']
        entry = dict(partition=partition, source=source['source'], bronze_run_id=run['bronze_run_id'],
                     silver_run_id=run['silver_run_id'], metrics=output['metrics'],
                     original_input_path=source['path'], native_response_lineage=source.get('acquisition_manifest'))
        for label, path in [('bronze', output['bronze_path']), ('silver', output['silver']['path']),
                            ('native', source['path']), ('lineage', run['output_manifest'])]:
            original = ROOT/path
            target = samples/label/original.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
            relative = target.relative_to(samples).as_posix()
            digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
            manifest['files'][relative] = dict(sha256=digest, bytes=target.stat().st_size)
            entry[label] = relative
            if label == 'bronze' and digest != output['bronze_sha256']:
                raise ValueError('bronze_checksum_mismatch')
            if label == 'silver' and digest != output['silver']['sha256']:
                raise ValueError('silver_checksum_mismatch')
        manifest['entries'].append(entry)
    (samples/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('Prepared 3 actual Bronze JSON, 3 Silver Parquet, 3 CSV inputs and lineage manifests.')


if __name__ == '__main__':
    main()
