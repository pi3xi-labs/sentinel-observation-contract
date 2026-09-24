#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

MANIFEST = ROOT / "manifest" / "contracts-v1.2.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)


with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

files = manifest.get("files", {})

for rel_path, expected_hash in files.items():

    target = ROOT / rel_path

    if not target.exists():
        fail(f"missing file: {rel_path}")

    actual_hash = sha256_file(target)

    if actual_hash != expected_hash:
        fail(
            f"hash mismatch: {rel_path}\n"
            f"expected={expected_hash}\n"
            f"actual={actual_hash}"
        )

print("[PASS] manifest validation completed")
