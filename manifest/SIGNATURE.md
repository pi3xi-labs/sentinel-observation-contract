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

---

# Sigstore Verification (contracts-v1.4)

## Model

contracts-v1.4 **retains** the certificate model introduced in v1.3:

- `manifest/release-certificate.json` (certificate-v1, status `model`) is normative
- certificate → `manifest_sha256` of `manifest/contracts-v1.4.json`
- `manifest/contracts-v1.4.sig` is the human-readable model attestation

The Sigstore bundle **adds cryptographic provenance** on top of it:

- `.github/workflows/sign-release.yml` runs on Release publish
- cosign signs the committed `manifest/contracts-v1.4.json` keyless (GitHub OIDC → Fulcio certificate, Rekor transparency log)
- the result `contracts-v1.4.bundle` is attached to the Release as an asset
- the bundle is **not committed** and **not hashed** into the manifest (circular binding)

The certificate declares the provenance policy in its `provenance` block:

- issuer: `https://token.actions.githubusercontent.com`
- identity: `https://github.com/pi3xi-labs/sentinel-observation-contract/.github/workflows/sign-release.yml@refs/tags/contracts-v1.4`

## Required locks

1. Structure Lock
2. Behavior Lock
3. Integrity Lock
4. Signature Lock
5. Sigstore Verification

## Verify

```bash
cosign verify-blob manifest/contracts-v1.4.json \
  --bundle contracts-v1.4.bundle \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity https://github.com/pi3xi-labs/sentinel-observation-contract/.github/workflows/sign-release.yml@refs/tags/contracts-v1.4
```

The signing workflow also runs negative checks (wrong issuer, wrong identity, tampered manifest, tampered bundle) and fails the release if any of them verifies.

## Phone release checklist (v1.4)

1. Confirm CI `contracts-check` is green (Structure, Behavior, Integrity, Signature, Reproducibility).
2. Open compare/PR from staging branch → org `main` and merge.
3. Create GitHub Release: tag `contracts-v1.4` on the merge commit, title `contracts-v1.4 — Sigstore Verification`, Publish.
4. `sign-release` runs automatically and attaches `contracts-v1.4.json` and `contracts-v1.4.bundle` to the Release.

Compare: https://github.com/pi3xi-labs/sentinel-observation-contract/compare/main...wizyig:sentinel-observation-contract:d1-sigstore-v1.4
