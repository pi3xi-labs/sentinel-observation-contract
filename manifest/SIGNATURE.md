# Signature Lock (contracts-v1.3)

## Model

Phase D ships a **certificate model**, not mandatory Sigstore CI yet.

Normative file:

- `manifest/release-certificate.json`

Integrity binding:

- certificate → `manifest_sha256` of `manifest/contracts-v1.3.json`
- manifest → content hashes of contract/docs/tools (Integrity Lock)

Git commit SHAs are recorded in Release notes / this file for humans.
They are **not** embedded inside hashed certificate fields (avoids circular binding).

## Required locks

1. Structure Lock
2. Behavior Lock
3. Integrity Lock
4. Signature Lock

## Phone release checklist

1. Confirm CI `contracts-check` is green (four lock steps).
2. Open compare/PR from staging fork → org `main`.
3. After merge, create GitHub Release `contracts-v1.3` and pin the merge commit in Release notes.
4. Cosign/Sigstore (Phase D.1) is optional upgrade; do not block v1.3 on it.

## Staging / compare

- Staging: `wizyig/sentinel-observation-contract`
- Canonical: `pi3xi-labs/sentinel-observation-contract`
- Compare: https://github.com/pi3xi-labs/sentinel-observation-contract/compare/main...wizyig:sentinel-observation-contract:main
