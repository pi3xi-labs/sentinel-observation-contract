#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "contracts/observation_window.yaml",
    "contracts/escalation_rules.yaml",
    "contracts/delta_policy.yaml",
    "README.md",
    "GOVERNANCE.md",
    "tools/validate_contracts.py",
    "tools/validate_manifest.py",
    "tools/validate_signature.py",
    "tests/evaluate_examples.py",
]

RELEASE = "contracts-v1.3"

OUTPUT = ROOT / "manifest" / f"{RELEASE}.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()


manifest = {
    "release": RELEASE,
    "lock": "Signature Lock",
    "files": {}
}

for rel_path in FILES:
    target = ROOT / rel_path

    manifest["files"][rel_path] = sha256_file(target)

OUTPUT.parent.mkdir(exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        manifest,
        f,
        indent=2,
        sort_keys=True
    )

print(f"[PASS] wrote {OUTPUT}")
