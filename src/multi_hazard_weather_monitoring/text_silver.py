"""Source-aware Silver narrative processing for real NOAA Storm Events text.

This is a bounded textual view of original NOAA CSV rows. Sentiment describes
lexical tone of the report, never hazard severity or public opinion.
"""

from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import os
import re
import shutil
import tempfile
from pathlib import Path

STOPWORDS = frozenset(
    "a an and are as at be by for from had has have in is it of on or that the their "
    "there this to was were with after before during into over under across near around"
    .split()
)
TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?")
URL = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
TAG = re.compile(r"<[^>]+>")
MENTION = re.compile(r"(?<!\w)@[A-Za-z0-9_]+")


def clean_tokens(value: str) -> list[str]:
    """Decode markup and remove transport noise while retaining useful terms."""
    cleaned = html.unescape(TAG.sub(" ", value))
    cleaned = MENTION.sub(" ", URL.sub(" ", cleaned)).replace("#", "")
    return [token for token in TOKEN.findall(cleaned.lower()) if token not in STOPWORDS]


def classify_sentiment(score: float) -> str:
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def narrative_rows(body: bytes, *, capture_sha256: str) -> list[dict]:
    """Profile each real NOAA event row; preserve missingness explicitly."""
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    if hashlib.sha256(body).hexdigest().lower() != capture_sha256.lower():
        raise ValueError("narrative_capture_hash_mismatch")
    analyzer = SentimentIntensityAnalyzer()
    reader = csv.DictReader(io.StringIO(body.decode("utf-8-sig"), newline=""))
    if not {"EVENT_ID", "EVENT_NARRATIVE", "EPISODE_NARRATIVE"}.issubset(reader.fieldnames or []):
        raise ValueError("noaa_narrative_columns_missing")
    output = []
    seen = set()
    for line, row in enumerate(reader, start=2):
        key = (row.get("EVENT_ID") or "").strip()
        if not key or key in seen:
            raise ValueError("invalid_or_duplicate_narrative_event_id")
        seen.add(key)
        event = (row.get("EVENT_NARRATIVE") or "").strip()
        episode = (row.get("EPISODE_NARRATIVE") or "").strip()
        selected = event or episode
        field = "EVENT_NARRATIVE" if event else "EPISODE_NARRATIVE" if episode else None
        tokens = clean_tokens(selected) if selected else []
        score = analyzer.polarity_scores(selected)["compound"] if selected else None
        output.append({
            "source": "noaa_storm_events", "source_key": key, "source_line": line,
            "text_field": field, "raw_text": selected or None,
            "clean_text": " ".join(tokens) if selected else None,
            "characters": len(selected) if selected else None,
            "tokens": tokens, "token_count": len(tokens) if selected else None,
            "sentiment_score": score,
            "sentiment_label": classify_sentiment(score) if score is not None else None,
            "source_capture_sha256": capture_sha256.upper(),
        })
    return output


def export_narrative_silver(body: bytes, *, capture_sha256: str, destination: Path) -> dict:
    """Publish one checked, immutable Parquet text view and return its lineage."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    rows = narrative_rows(body, capture_sha256=capture_sha256)
    schema = pa.schema([
        ("source", pa.string()), ("source_key", pa.string()), ("source_line", pa.int64()),
        ("text_field", pa.string()), ("raw_text", pa.string()),
        ("clean_text", pa.string()), ("characters", pa.int64()),
        ("tokens", pa.list_(pa.string())), ("token_count", pa.int64()),
        ("sentiment_score", pa.float64()), ("sentiment_label", pa.string()),
        ("source_capture_sha256", pa.string()),
    ], metadata={b"weather_schema": b"silver-narrative-v1",
                 b"sentiment_method": b"VADER 3.3.2 raw English narrative; not hazard severity"})
    table = pa.Table.from_pylist(rows, schema=schema)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        existing = pq.read_table(destination)
        if not existing.equals(table, check_metadata=False) or existing.schema.metadata != table.schema.metadata:
            raise ValueError("existing_narrative_silver_conflict")
    else:
        descriptor, temporary_name = tempfile.mkstemp(dir=destination.parent, suffix=".tmp")
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            pq.write_table(table, temporary, compression="snappy")
            restored = pq.read_table(temporary)
            if not restored.equals(table, check_metadata=False) or restored.schema.metadata != table.schema.metadata:
                raise ValueError("narrative_parquet_roundtrip_mismatch")
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
    return {"path": destination.as_posix(), "rows": len(rows),
            "nonempty_text": sum(row["raw_text"] is not None for row in rows),
            "event_narratives": sum(row["text_field"] == "EVENT_NARRATIVE" for row in rows),
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest().upper(),
            "source_capture_sha256": capture_sha256.upper(), "schema": "silver-narrative-v1"}


def mirror_numeric_silver(source: Path, root: Path) -> dict:
    """Expose a checked historical Silver export in the guide's folder layout."""
    source, root = Path(source).resolve(), Path(root).resolve()
    if not source.is_relative_to(root / "data/curated/silver") or source.suffix != ".parquet":
        raise ValueError("numeric_silver_source_outside_curated")
    destination = root / "datalake_silver" / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(source.read_bytes()).hexdigest().upper()
    if destination.exists():
        if hashlib.sha256(destination.read_bytes()).hexdigest().upper() != digest:
            raise ValueError("numeric_silver_mirror_conflict")
    else:
        shutil.copyfile(source, destination)
    receipt = {"path": destination.relative_to(root).as_posix(),
               "original_path": source.relative_to(root).as_posix(), "sha256": digest,
               "producer": "verified_historical_silver_mirror"}
    sidecar = destination.with_suffix(".manifest.json")
    if sidecar.exists():
        if json.loads(sidecar.read_text(encoding="utf-8")) != receipt:
            raise ValueError("numeric_silver_mirror_manifest_conflict")
    else:
        sidecar.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    return receipt


def publish_narrative_from_bronze(bronze_path: str | Path) -> dict | None:
    """Verify a Bronze/native pair and publish NOAA text as a Silver sidecar."""
    from .historical_pipeline import ROOT, capture_config, checked_bronze_path
    from .sources.capture_registry import registered_hashes
    from .storage.raw_landing import require_registered_capture

    bronze = checked_bronze_path(bronze_path)
    payload = json.loads(bronze.read_text(encoding="utf-8"))
    source = capture_config(payload["source"]["partition"])
    if payload["source"] != source:
        raise ValueError("narrative_bronze_configuration_mismatch")
    if source["source"] != "noaa_storm_events":
        return None
    capture = payload["original_capture"]
    native = (ROOT / "data/raw" / capture["raw_path"]).resolve()
    if not native.is_relative_to((ROOT / "data/raw").resolve()):
        raise ValueError("narrative_native_path_outside_landing")
    body = native.read_bytes()
    require_registered_capture(body, source["path"], registered_hashes(ROOT))
    destination = ROOT / "datalake_silver/text" / (bronze.stem + ".parquet")
    result = export_narrative_silver(body, capture_sha256=capture["sha256"],
                                     destination=destination)
    result["path"] = destination.relative_to(ROOT).as_posix()
    sidecar = destination.with_suffix(".manifest.json")
    if sidecar.exists():
        if json.loads(sidecar.read_text(encoding="utf-8")) != result:
            raise ValueError("narrative_manifest_conflict")
    else:
        sidecar.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result
