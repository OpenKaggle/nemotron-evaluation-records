#!/usr/bin/env python3
"""Build a content-minimized index for a local Nemotron reports tree.

The output keeps file provenance, hashes, schemas, row counts, and numeric
aggregates. It never copies string values or report bodies, so prompt/answer/
completion/trace text and local paths do not enter the release.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

SENSITIVE = re.compile(
    r"(prompt|completion|answer|question|response|trace|token|label|target|"
    r"problem|input|output|id|submission|path|text|content|context)", re.I
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def numeric_stats(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def scalar_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return float(value)


def jsonl_profile(path: Path) -> dict[str, Any]:
    rows = 0
    keys: Counter[str] = Counter()
    nums: dict[str, list[float]] = {}
    with path.open(errors="replace") as f:
        for line in f:
            if not line.strip():
                continue
            rows += 1
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            for key, value in obj.items():
                key = str(key)
                keys[key] += 1
                number = scalar_number(value)
                if number is not None and not SENSITIVE.search(key):
                    nums.setdefault(key, []).append(number)
    return {
        "format": "jsonl",
        "rows": rows,
        "keys": sorted(keys),
        "key_counts": dict(sorted(keys.items())),
        "numeric": {k: numeric_stats(v) for k, v in sorted(nums.items())},
    }


def json_profile(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(errors="replace"))
    except Exception:
        return {"format": "json", "parse": "failed"}
    keys: set[str] = set()
    nums: dict[str, list[float]] = {}

    def walk(node: Any, prefix: str = "") -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                name = f"{prefix}.{key}" if prefix else str(key)
                keys.add(name)
                walk(child, name)
        elif isinstance(node, list):
            for child in node[:256]:
                walk(child, prefix)
        else:
            number = scalar_number(node)
            if number is not None and not SENSITIVE.search(prefix):
                nums.setdefault(prefix, []).append(number)

    walk(value)
    return {
        "format": "json",
        "root_type": type(value).__name__,
        "keys": sorted(keys),
        "numeric": {k: numeric_stats(v) for k, v in sorted(nums.items())},
    }


def csv_profile(path: Path) -> dict[str, Any]:
    with path.open(errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = 0
        numeric: dict[str, list[float]] = {}
        text_lengths: dict[str, list[int]] = {}
        for row in reader:
            rows += 1
            for key in fields:
                value = (row.get(key) or "").strip()
                if SENSITIVE.search(key):
                    continue
                try:
                    number = float(value)
                except ValueError:
                    if value:
                        text_lengths.setdefault(key, []).append(len(value))
                    continue
                if math.isfinite(number):
                    numeric.setdefault(key, []).append(number)
    return {
        "format": "csv",
        "rows": rows,
        "columns": fields,
        "numeric": {k: numeric_stats(v) for k, v in sorted(numeric.items())},
        "text_lengths": {
            k: numeric_stats([float(x) for x in v]) for k, v in sorted(text_lengths.items())
        },
    }


def profile(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return jsonl_profile(path)
    if suffix == ".json":
        return json_profile(path)
    if suffix == ".csv":
        return csv_profile(path)
    try:
        lines = sum(1 for _ in path.open(errors="replace"))
    except Exception:
        lines = None
    return {"format": suffix.lstrip(".") or "binary", "lines": lines}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("reports"))
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    ext_counts: Counter[str] = Counter()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        ext = path.suffix.lower() or "<none>"
        ext_counts[ext] += 1
        raw = path.read_bytes()
        rows.append({
            "path": rel,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "extension": ext,
        })
        sidecar = out / "schemas" / f"{len(rows):04d}.json"
        sidecar.parent.mkdir(parents=True, exist_ok=True)
        sidecar.write_text(json.dumps({"path": rel, "sha256": rows[-1]["sha256"], **profile(path)}, indent=2) + "\n")
    with (out / "report-index.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256", "extension"])
        writer.writeheader()
        writer.writerows(rows)
    (out / "summary.json").write_text(json.dumps({
        "source_group": "kagglenvda/reports",
        "files": len(rows),
        "total_bytes": sum(int(r["bytes"]) for r in rows),
        "extensions": dict(sorted(ext_counts.items())),
        "string_values": "not included",
        "raw_report_bodies": "not included",
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
