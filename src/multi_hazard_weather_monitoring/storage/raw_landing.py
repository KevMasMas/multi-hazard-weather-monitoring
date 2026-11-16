"""Content-addressed landing of immutable source response bytes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


def land_capture(body: bytes, *, source: str, partition: str,
                 root: Path, content_type: str, origin: str) -> dict:
    """Persist unchanged bytes once and return a deterministic capture manifest.

    ``origin`` identifies the existing evidence file or request; it is not a new
    retrieval timestamp. The manifest is a derivative, never the raw response.
    """
    if not re.fullmatch(r"[a-z][a-z0-9_]*", source):
        raise ValueError("invalid_source_name")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", partition):
        raise ValueError("invalid_partition_name")
    digest = hashlib.sha256(body).hexdigest()
    directory = root / source / partition
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{digest}.csv"
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError("existing_capture_hash_mismatch")
    else:
        with tempfile.NamedTemporaryFile(dir=directory, delete=False) as stream:
            temporary = Path(stream.name)
            try:
                stream.write(body)
                stream.flush()
                os.fsync(stream.fileno())
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
        try:
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    manifest = {
        "source": source,
        "partition": partition,
        "content_type": content_type,
        "origin": origin,
        "sha256": digest,
        "byte_count": len(body),
        "raw_path": target.relative_to(root).as_posix(),
        "raw_format": "csv",
    }
    manifest_path = directory / f"{digest}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8")
    return manifest
