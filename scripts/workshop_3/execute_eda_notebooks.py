"""Execute revised W3 notebooks with an explicit isolated Python kernel."""
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--notebook',required=True)
    parser.add_argument('--receipt',required=True)
    args=parser.parse_args()
    path=ROOT/args.notebook
    notebook=nbformat.read(path,as_version=4)
    receipt=ROOT/args.receipt
    receipt.parent.mkdir(parents=True,exist_ok=True)
    started=datetime.now(timezone.utc).isoformat()
    error=None
    with tempfile.TemporaryDirectory(prefix='team9-eda-kernel-',ignore_cleanup_errors=True) as directory:
        base=Path(directory)
        spec=base/'kernels/team9-eda';spec.mkdir(parents=True)
        (spec/'kernel.json').write_text(json.dumps({
            'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
            'display_name':'Team 9 isolated EDA','language':'python'}),encoding='utf-8')
        manager=KernelManager(kernel_name='team9-eda',
            kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(base/'kernels')]))
        env=os.environ.copy()
        env.update(IPYTHONDIR=str(base/'ipython'),JUPYTER_RUNTIME_DIR=str(base/'runtime'),
                   MPLCONFIGDIR=str(base/'matplotlib'),NUMBA_CACHE_DIR=str(base/'numba'))
        client=NotebookClient(notebook,km=manager,timeout=600,
                              resources={'metadata':{'path':str(path.parent)}})
        try:
            client.execute(env=env)
        except Exception as exc:
            error=type(exc).__name__+': '+str(exc)
        finally:
            path.write_text(nbformat.writes(notebook),encoding='utf-8',newline='\n')
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
            manager.cleanup_resources()
    cells=[c for c in notebook.cells if c.cell_type=='code']
    errors=[o for c in cells for o in c.outputs if o.output_type=='error']
    proof={'started_at_utc':started,'finished_at_utc':datetime.now(timezone.utc).isoformat(),
           'notebook':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest().upper(),
           'code_cells':len(cells),'executed_cells':sum(c.execution_count is not None for c in cells),
           'error_outputs':len(errors),'successful':error is None and not errors,
           'python_executable':sys.executable,
           'packages':{p:importlib.metadata.version(p) for p in ['pandas','numpy','scipy','matplotlib','pyarrow','ydata-profiling']},
           'weather_network':False,'error':error}
    receipt.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n')
    if error:
        attempt=receipt.with_name(receipt.stem+'_failed_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.json')
        attempt.write_bytes(receipt.read_bytes())
        raise RuntimeError(error)
    print(json.dumps({k:proof[k] for k in ['notebook','code_cells','executed_cells','error_outputs','successful']}))


if __name__=='__main__':main()
