#!/usr/bin/env python3
"""Generate Integrity Lock hash manifest for contracts-v1.2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "manifest" / "contracts-v1.2.json"

FILES = [
    "README.md",
    "GOVERNANCE.md",
    "LICENSE",
    "contracts/README.md",
    "contracts/observation_window.yaml",
    "contracts/escalation_rules.yaml",
    "contracts/delta_policy.yaml",
    "tools/validate_contracts.py",
    "tools/validate_manifest.py",
    "tools/generate_manifest.py",
    "tests/contract_examples.yaml",
    "tests/evaluate_examples.py",
    ".github/workflows/contracts.yml",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    entries = {}
    for rel in FILES:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"[FAIL] missing file for manifest: {rel}")
        entries[rel] = {"sha256": sha256_file(path)}

    payload = {
        "version": "contracts-v1.2",
        "lock": "Integrity Lock",
        "algorithm": "sha256",
        "files": entries,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"[PASS] wrote {OUTPUT.relative_to(ROOT)} ({len(entries)} files)")


if __name__ == "__main__":
    main()
