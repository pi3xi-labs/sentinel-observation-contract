#!/usr/bin/env python3
"""Validate Integrity Lock hash manifest for contracts-v1.2."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "contracts-v1.2.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def main() -> None:
    if not MANIFEST.is_file():
        fail(f"missing manifest: {MANIFEST.relative_to(ROOT)}")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("version") != "contracts-v1.2":
        fail(f"unexpected manifest version: {data.get('version')!r}")
    if "commit" in data:
        fail("manifest must not contain a commit field")

    files = data.get("files")
    if not isinstance(files, dict) or not files:
        fail("manifest.files must be a non-empty mapping")

    mismatches = []
    missing = []
    for rel, meta in files.items():
        path = ROOT / rel
        if not path.is_file():
            missing.append(rel)
            continue
        expected = (meta or {}).get("sha256")
        actual = sha256_file(path)
        if expected != actual:
            mismatches.append(rel)

    if missing:
        fail("missing protected files: " + ", ".join(missing))
    if mismatches:
        fail("sha256 mismatch: " + ", ".join(mismatches))

    print(f"[PASS] manifest integrity verified ({len(files)} files)")


if __name__ == "__main__":
    main()
