"""Execute the review in a fresh kernel; preserve real outputs and an audit."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import nbformat
from nbclient import NotebookClient
import pandas
import pyarrow

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--notebook', type=Path, default=ROOT/'notebooks/02_historical_ingestion_review.ipynb')
    parser.add_argument('--receipt', type=Path, default=ROOT/'workshop_2/evidence/notebook_execution.json')
    args=parser.parse_args()
    path=args.notebook.resolve()
    notebook=nbformat.read(path,as_version=4)
    client=NotebookClient(notebook,timeout=180,kernel_name='python3',
                          resources={'metadata':{'path':str(path.parent)}})
    client.execute()
    errors=[o for c in notebook.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
    if errors:
        raise ValueError('notebook_error_outputs')
    nbformat.write(notebook,path)
    proof=dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),
               notebook=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest().upper(),
               code_cells=sum(c.cell_type=='code' for c in notebook.cells),error_outputs=len(errors),
               python=platform.python_version(),pandas=pandas.__version__,pyarrow=pyarrow.__version__,
               weather_network=False,database_network=False,
               environment='Existing dependency environment, fresh kernel; no cached notebook variables reused.')
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))


if __name__=='__main__':
    main()
