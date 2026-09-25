#!/usr/bin/env python3
"""Signature Lock / Sigstore Verification: validate the release certificate.

The certificate-v1 model (introduced in contracts-v1.3) binds the release to
the Integrity Lock manifest via manifest_sha256. contracts-v1.4 keeps that
model and declares the Sigstore provenance policy (issuer + workflow identity)
that the cosign bundle published as a Release asset must satisfy. Cryptographic
bundle verification itself runs in .github/workflows/sign-release.yml.
"""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CERTIFICATE = ROOT / "manifest" / "release-certificate.json"

RELEASE = "contracts-v1.4"
LOCK = "Sigstore Verification"
CANONICAL_REPOSITORY = "pi3xi-labs/sentinel-observation-contract"
MANIFEST_REL = f"manifest/{RELEASE}.json"

REQUIRED_LOCKS = [
    "Structure Lock",
    "Behavior Lock",
    "Integrity Lock",
    "Signature Lock",
    "Sigstore Verification",
]

EXPECTED_ISSUER = "https://token.actions.githubusercontent.com"
EXPECTED_IDENTITY = (
    f"https://github.com/{CANONICAL_REPOSITORY}"
    f"/.github/workflows/sign-release.yml@refs/tags/{RELEASE}"
)
EXPECTED_BUNDLE = f"{RELEASE}.bundle"


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
provenance = require(cert, "provenance")

if release != RELEASE:
    fail(f"release must be {RELEASE}, got: {release}")

if lock != LOCK:
    fail(f"lock must be {LOCK}, got: {lock}")

if canonical_repository != CANONICAL_REPOSITORY:
    fail(
        f"canonical_repository must be {CANONICAL_REPOSITORY}, "
        f"got: {canonical_repository}"
    )

if manifest_rel != MANIFEST_REL:
    fail(f"manifest path must be {MANIFEST_REL}, got: {manifest_rel}")

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
    fail("certificate-v1 signing.status must be 'model'")

sig_path = ROOT / "manifest" / f"{RELEASE}.sig"
if method == "certificate-v1" and not sig_path.exists():
    fail(f"certificate-v1 model attestation missing: {sig_path.relative_to(ROOT)}")

# Sigstore provenance policy (contracts-v1.4).
if not isinstance(provenance, dict):
    fail("provenance must be an object")

expected_provenance = {
    "type": "sigstore-cosign-bundle",
    "issuer": EXPECTED_ISSUER,
    "identity": EXPECTED_IDENTITY,
    "bundle": EXPECTED_BUNDLE,
    "bundle_location": "release-asset",
}
for key, expected in expected_provenance.items():
    actual = provenance.get(key)
    if actual != expected:
        fail(f"provenance.{key} must be {expected!r}, got: {actual!r}")

# The bundle signs the manifest; it must never be committed or hashed.
if (ROOT / "manifest" / EXPECTED_BUNDLE).exists() or (ROOT / EXPECTED_BUNDLE).exists():
    fail(f"{EXPECTED_BUNDLE} must be published as a Release asset, not committed")

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest_files = json.load(f).get("files", {})
if any(p.endswith(".bundle") for p in manifest_files):
    fail("manifest must not hash a Sigstore bundle (circular)")

print("[PASS] signature / release-certificate validation completed")
