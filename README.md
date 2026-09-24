# Sentinel Observation Contract

A frozen audit contract for observation, escalation, and delta evaluation.

**Current Stable Release:** `contracts-v1.3`  
**Compatibility Level:** Signature Lock

## Repositories

Canonical public repository:

`pi3xi-labs/sentinel-observation-contract`

Operational repository:

`wizyig/gbox`

## Purpose

Observation contracts are separated into three layers:

```text
Observe → Escalate → Evaluate
```

| Layer | File | Role |
| --- | --- | --- |
| Observe | `contracts/observation_window.yaml` | What to observe (O01–O07, 7-day window) |
| Escalate | `contracts/escalation_rules.yaml` | How to escalate (E001–E010) |
| Evaluate | `contracts/delta_policy.yaml` | Delta evaluation and final gate |

## Contract Set

```text
contracts/
├─ observation_window.yaml
├─ escalation_rules.yaml
└─ delta_policy.yaml
```

Details:

- `contracts/README.md`

## Contract Invariants

The following examples are normative and protected by Behavior Lock.

```text
promotion_delta=-6.25
→ pass

reobserve_multiplier=1.78
→ review

boundary_violation=1
→ fail
```

Any change that alters these outcomes is considered a contract-breaking change.

## Validation

Install dependencies:

```bash
pip install pyyaml
```

Run validations:

```bash
python tools/validate_contracts.py
python tests/evaluate_examples.py
python tools/validate_manifest.py
python tools/validate_signature.py
```

## Lock Model

```text
v1.0  Structure Lock
v1.1  Behavior Lock
v1.2  Integrity Lock
v1.3  Signature Lock
v2.x  Contract Evolution
```

## CI Coverage

Current:

- YAML validation
- Contract existence checks
- O01–O07 integrity
- E001–E010 integrity
- Gate existence checks
- Normative behavior verification
- Manifest verification
- Release artifact integrity verification
- Release certificate / Signature Lock verification

## Governance

See:

`GOVERNANCE.md`

## License

CC0 1.0 Universal
