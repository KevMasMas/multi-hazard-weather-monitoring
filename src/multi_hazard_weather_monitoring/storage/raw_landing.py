"""Content-addressed landing of immutable source response bytes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


def require_registered_capture(body: bytes, relative: str, register: dict[str, str]) -> None:
    """Reject bytes that differ from the saved Workshop 1 evidence register."""
    expected = register.get(relative)
    if expected is None or hashlib.sha256(body).hexdigest().upper() != expected.upper():
        raise ValueError(f"registered_capture_hash_mismatch:{relative}")


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
    formats = {"text/csv": "csv", "application/gzip": "gz"}
    if content_type not in formats:
        raise ValueError("unsupported_content_type")
    native_format = formats[content_type]
    if native_format == "gz" and not body.startswith(b"\x1f\x8b"):
        raise ValueError("invalid_gzip_header")
    digest = hashlib.sha256(body).hexdigest()
    directory = root / source / partition
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{digest}.{native_format}"
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError("existing_capture_hash_mismatch")
    else:
        descriptor, temporary_name = tempfile.mkstemp(dir=directory)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(body)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    manifest = {
        "source": source,
        "partition": partition,
        "content_type": content_type,
        "origin": origin,
        "sha256": digest,
        "byte_count": len(body),
        "raw_path": target.relative_to(root).as_posix(),
        "raw_format": native_format,
    }
    manifest_path = directory / f"{digest}.manifest.json"
    if manifest_path.exists():
        if json.loads(manifest_path.read_text(encoding="utf-8")) != manifest:
            raise ValueError("capture_manifest_conflict")
    else:
        descriptor, temporary_name = tempfile.mkstemp(dir=directory)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
                json.dump(manifest, stream, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, manifest_path)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    return manifest
