#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CERTIFICATE = ROOT / "manifest" / "release-certificate.json"
REQUIRED_LOCKS = [
    "Structure Lock",
    "Behavior Lock",
    "Integrity Lock",
    "Signature Lock",
]


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


def require(obj, key):
    if key not in obj:
        fail(f"missing required field: {key}")
    return obj[key]


if not CERTIFICATE.exists():
    fail(f"missing certificate: {CERTIFICATE.relative_to(ROOT)}")

with open(CERTIFICATE, "r", encoding="utf-8") as f:
    cert = json.load(f)

release = require(cert, "release")
lock = require(cert, "lock")
canonical_repository = require(cert, "canonical_repository")
manifest_rel = require(cert, "manifest")
manifest_sha256 = require(cert, "manifest_sha256")
requires = require(cert, "requires")
approval = require(cert, "approval")
signing = require(cert, "signing")

if release != "contracts-v1.3":
    fail(f"release must be contracts-v1.3, got: {release}")

if lock != "Signature Lock":
    fail(f"lock must be Signature Lock, got: {lock}")

if canonical_repository != "pi3xi-labs/sentinel-observation-contract":
    fail(
        "canonical_repository must be "
        "pi3xi-labs/sentinel-observation-contract, "
        f"got: {canonical_repository}"
    )

if manifest_rel != "manifest/contracts-v1.3.json":
    fail(f"manifest path must be manifest/contracts-v1.3.json, got: {manifest_rel}")

manifest_path = ROOT / manifest_rel
if not manifest_path.exists():
    fail(f"manifest file missing: {manifest_rel}")

actual_sha = sha256_file(manifest_path)
if actual_sha != manifest_sha256:
    fail(
        "manifest_sha256 mismatch\n"
        f"expected={manifest_sha256}\n"
        f"actual={actual_sha}"
    )

if not isinstance(requires, list):
    fail("requires must be a list")

missing = [item for item in REQUIRED_LOCKS if item not in requires]
if missing:
    fail(f"requires missing locks: {missing}")

if not isinstance(approval, str) or not approval.strip():
    fail("approval must be a non-empty string")

if not isinstance(signing, dict):
    fail("signing must be an object")

method = signing.get("method")
status = signing.get("status")

if method not in ("certificate-v1", "sigstore-cosign-blob"):
    fail(f"unsupported signing.method: {method}")

if method == "certificate-v1" and status != "model":
    fail("certificate-v1 signing.status must be 'model' for Phase D")

sig_path = ROOT / "manifest" / "contracts-v1.3.sig"
if (
    method == "sigstore-cosign-blob"
    and sig_path.exists()
    and sig_path.stat().st_size > 0
):
    print(
        "[WARN] signing.method is sigstore-cosign-blob; "
        "cosign verify is not required in contracts-check yet"
    )
elif method == "certificate-v1" and sig_path.exists():
    # Placeholder attestation is fine for the model phase.
    pass

print("[PASS] signature / release-certificate validation completed")
