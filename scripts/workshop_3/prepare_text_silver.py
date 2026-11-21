"""Derive the bounded NOAA 2021 text Silver sample from registered native CSV."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from multi_hazard_weather_monitoring.text_silver import export_narrative_silver  # noqa: E402


def main() -> None:
    native = ROOT / "workshop_2/samples/native/noaa_oklahoma_2021.csv"
    lineage = json.loads((ROOT / "workshop_2/samples/lineage/"
                          "noaa_storm_events_20261117_020238_c0b5c9ad0bca.manifest.json")
                         .read_text(encoding="utf-8"))
    body = native.read_bytes()
    expected = lineage["native_sha256"]
    if hashlib.sha256(body).hexdigest().upper() != expected.upper():
        raise ValueError("registered_noaa_native_mismatch")
    sample = ROOT / "workshop_3/samples/silver_text/noaa_oklahoma_2021_text.parquet"
    result = export_narrative_silver(body, capture_sha256=expected, destination=sample)
    target = ROOT / "datalake_silver/text" / sample.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != sample.read_bytes():
            raise ValueError("text_silver_restore_conflict")
    else:
        shutil.copyfile(sample, target)
    receipt = {**result, "path": sample.relative_to(ROOT).as_posix(),
               "lake_path": target.relative_to(ROOT).as_posix(),
               "native_path": native.relative_to(ROOT).as_posix(),
               "method": "VADER 3.3.2 on original English NOAA narrative; lexical tone only",
               "scope": "2021 Oklahoma sample only; later raw years absent from portable package"}
    manifest = sample.with_suffix(".manifest.json")
    manifest.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    (target.with_suffix(".manifest.json")).write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: receipt[k] for k in ("rows", "nonempty_text", "event_narratives", "sha256")}))


if __name__ == "__main__":
    main()
