#!/usr/bin/env python3
"""Integrity Lock: verify the current release manifest against the tree."""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

RELEASE = "contracts-v1.4"

MANIFEST = ROOT / "manifest" / f"{RELEASE}.json"


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


if not MANIFEST.exists():
    fail(f"missing manifest: {MANIFEST.relative_to(ROOT)}")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

if manifest.get("release") != RELEASE:
    fail(f"manifest release must be {RELEASE}, got: {manifest.get('release')}")

files = manifest.get("files", {})

if not isinstance(files, dict) or not files:
    fail("manifest files must be a non-empty mapping")

for rel_path, expected_hash in files.items():

    if rel_path.endswith(".bundle"):
        fail(f"manifest must not hash a Sigstore bundle (circular): {rel_path}")

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

print(f"[PASS] manifest validation completed ({MANIFEST.relative_to(ROOT)})")
