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
```

Each lock level builds upon all previous levels.

A release claiming a higher lock level must satisfy all lower lock levels.
