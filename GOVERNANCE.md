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

## Compatibility Principle

```text
Structure Lock
    ↓
Behavior Lock
    ↓
Integrity Lock
    ↓
Signature Lock
```

Each lock level builds upon all previous levels.

A release claiming a higher lock level must satisfy all lower lock levels.
