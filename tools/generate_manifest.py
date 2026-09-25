#!/usr/bin/env python3
"""Generate the Integrity Lock manifest for a contracts release.

Usage:
    python tools/generate_manifest.py            # current release (RELEASE)
    python tools/generate_manifest.py --check    # regenerate in memory, fail on drift

Output is deterministic: flat ``path -> sha256`` mapping, sorted keys,
2-space indentation, no trailing newline. Sigstore bundles (``*.bundle``)
are never included: the bundle signs the manifest, so hashing it into the
manifest would be circular.
"""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

# Current release. Released manifests (contracts-v1.2.json, contracts-v1.3.json)
# are frozen artifacts and are never regenerated.
RELEASE = "contracts-v1.4"
LOCK = "Sigstore Verification"

FILES = [
    "contracts/observation_window.yaml",
    "contracts/escalation_rules.yaml",
    "contracts/delta_policy.yaml",
    "contracts/README.md",
    "README.md",
    "GOVERNANCE.md",
    "manifest/SIGNATURE.md",
    "tools/generate_manifest.py",
    "tools/validate_contracts.py",
    "tools/validate_manifest.py",
    "tools/validate_signature.py",
    "tests/contract_examples.yaml",
    "tests/evaluate_examples.py",
    ".github/workflows/contracts.yml",
    ".github/workflows/sign-release.yml",
]

OUTPUT = ROOT / "manifest" / f"{RELEASE}.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()


def build() -> str:
    for rel_path in FILES:
        if rel_path.endswith(".bundle"):
            raise SystemExit(f"[FAIL] bundle must not be hashed into manifest: {rel_path}")

    manifest = {
        "release": RELEASE,
        "lock": LOCK,
        "files": {rel: sha256_file(ROOT / rel) for rel in FILES},
    }

    return json.dumps(manifest, indent=2, sort_keys=True)


def main() -> None:
    content = build()

    if "--check" in sys.argv[1:]:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
        if current != content:
            print(f"[FAIL] {OUTPUT.relative_to(ROOT)} is not reproducible from the tree")
            sys.exit(1)
        print(f"[PASS] {OUTPUT.relative_to(ROOT)} is reproducible")
        return

    OUTPUT.parent.mkdir(exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print(f"[PASS] wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
