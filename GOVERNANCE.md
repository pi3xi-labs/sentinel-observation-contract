# Governance

## Purpose

This repository maintains the canonical Sentinel Observation Contract.

The governance model protects the contract through progressive lock levels.

---

## Lock Levels

### Structure Lock (v1.0)

Protects contract structure.

Scope:

- repository layout
- required contract files
- O01–O07 observation identifiers
- E001–E010 escalation identifiers
- gate section existence

Examples:

```text
contracts/
├─ observation_window.yaml
├─ escalation_rules.yaml
└─ delta_policy.yaml
```

Breaking any item above requires a major-version review.

---

### Behavior Lock (v1.1)

Protects contract semantics.

Normative examples:

```text
promotion_delta=-6.25
→ pass

reobserve_multiplier=1.78
→ review

boundary_violation=1
→ fail
```

Any change that alters these outcomes is considered contract-breaking.

---

### Integrity Lock (v1.2)

Protects released artifacts.

Scope:

- hash manifest contents
- manifest consistency
- reproducible release assets
- release integrity validation

Integrity Lock does not define behavior.

Integrity Lock verifies that released artifacts remain unchanged.

---

### Signature Lock (Phase D / v1.3)

Protects release authenticity.

Scope:

- release signatures
- signing identity
- release provenance
- artifact attestation

Signature Lock does not redefine Integrity Lock.

Signature Lock verifies that a release claiming authenticity binds to a verified integrity manifest through a release certificate (certificate-v1 model). Sigstore/cosign blob signing is a later upgrade path (Phase D.1) and does not replace the certificate model.

A valid release must satisfy:

Structure Lock
Behavior Lock
Integrity Lock
Signature Lock

Normative release attestation assets:

```text
manifest/
├─ contracts-v1.3.json
├─ contracts-v1.3.sig
└─ release-certificate.json
```

`release-certificate.json` is normative. It binds to `manifest_sha256` of the Integrity Lock manifest. Git commit SHAs are recorded in human-readable release notes only, not inside hashed certificate fields, to avoid circular binding.

---

### Sigstore Verification (v1.4)

Protects release provenance cryptographically.

Scope:

- Sigstore/cosign bundle over the Integrity Lock manifest
- OIDC issuer verification
- signing workflow identity verification
- public transparency log (Rekor) inclusion

Sigstore Verification does not replace the Signature Lock certificate model. `manifest/release-certificate.json` (certificate-v1) remains normative and binds the release to `manifest_sha256`; the Sigstore bundle adds cryptographic proof that the manifest was signed by the canonical release workflow.

A valid release must satisfy:

Structure Lock
Behavior Lock
Integrity Lock
Signature Lock
Sigstore Verification

Normative release attestation assets:

```text
manifest/
├─ contracts-v1.4.json
├─ contracts-v1.4.sig
└─ release-certificate.json

Release assets (not committed):
├─ contracts-v1.4.json
└─ contracts-v1.4.bundle
```

See `## Sigstore Provenance Requirements`.

---

### Contract Evolution (v2.x)

Major versions may introduce:

- new contract types
- new lock levels
- new evaluation semantics
- new observation models

Breaking changes are allowed only through major-version releases.

---

## Canonical References

Public contract repository:

`pi3xi-labs/sentinel-observation-contract`

Operational repository:

`wizyig/gbox`

---

## Historical Origin

Structure Lock originated in `wizyig/gbox`, release `contracts-v1.0`, commit `823515c81fc234f36e2e372e0a00d140b901714e`.

The canonical repository was created afterward by extracting the contract set into `pi3xi-labs/sentinel-observation-contract`.

The first tag in this repository is `contracts-v1.1`.

---

## Release Naming

Release titles use the format:

```text
<tag> — <milestone>
```

Examples:

```text
contracts-v1.1 — Behavior Lock
contracts-v1.2 — Integrity Lock
contracts-v1.3 — Signature Lock
contracts-v1.4 — Sigstore Verification
```

`contracts-v1.0 — Structure Lock` exists only in `wizyig/gbox`.

Release titles are descriptive only. Release validity is determined by the tag, the tagged commit, the Integrity Lock manifest, and the signature artifacts (release certificate and Sigstore bundle), not by the title.

---

## Sigstore Provenance Requirements

Starting with `contracts-v1.4`, a release MUST satisfy:

1. manifest verification — `manifest/<tag>.json` matches the tagged tree (Integrity Lock) and `release-certificate.json` binds its `manifest_sha256` (Signature Lock)
2. bundle verification — `<tag>.bundle` is a valid Sigstore bundle over `manifest/<tag>.json`
3. issuer verification — the signing certificate was issued for the approved OIDC issuer
4. workflow identity verification — the signing certificate identity is the approved release workflow at the release tag

Approved issuer:

```text
https://token.actions.githubusercontent.com
```

Approved identity:

```text
https://github.com/pi3xi-labs/sentinel-observation-contract/.github/workflows/sign-release.yml@refs/tags/<tag>
```

Verification MUST fail if:

- the issuer differs
- the identity differs (other repository, other workflow, or other ref)
- the manifest contents differ
- the bundle differs

Verification example:

```bash
cosign verify-blob manifest/contracts-v1.4.json \
  --bundle contracts-v1.4.bundle \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity https://github.com/pi3xi-labs/sentinel-observation-contract/.github/workflows/sign-release.yml@refs/tags/contracts-v1.4
```

The bundle is produced by `.github/workflows/sign-release.yml` when the release is published and is attached to the GitHub Release as an asset. It is never committed to the repository: the bundle signs the manifest, so committing it (and hashing it into the manifest) would be circular.

---

## Protected Artifacts

The following paths are protected by the lock levels above. Changes require review and, where hashed, a new manifest in a new release:

```text
contracts/*
manifest/*
tools/*
tests/*
.github/workflows/*
README.md
GOVERNANCE.md
```

Released manifests (`manifest/contracts-v1.2.json`, `manifest/contracts-v1.3.json`) and model attestations (`manifest/contracts-v1.3.sig`) are frozen and are never regenerated.

---

## Compatibility Principle

```text
Structure Lock
    ↓
Behavior Lock
    ↓
Integrity Lock
    ↓
Signature Lock
    ↓
Sigstore Verification
```

Each lock level builds upon all previous levels.

A release claiming a higher lock level must satisfy all lower lock levels.
