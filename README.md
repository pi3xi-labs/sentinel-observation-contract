# Sentinel Observation Contract

A frozen audit contract for observation,
escalation, and delta evaluation.

**Current Stable Release:** `contracts-v1.1`  
**Compatibility Level:** Behavior Lock

Canonical public repository (after org transfer):

`pi3xi-labs/sentinel-observation-contract`

Working / operational skeleton remains:

`wizyig/gbox`

## Purpose

Observe → Escalate → Evaluate

| Layer | File | Role |
| --- | --- | --- |
| Observe | `contracts/observation_window.yaml` | What to observe (O01–O07, 7d window) |
| Escalate | `contracts/escalation_rules.yaml` | How to escalate (E001–E010) |
| Evaluate | `contracts/delta_policy.yaml` | How to judge deltas + `gate` |

## Contract Set

```text
contracts/
├─ observation_window.yaml
├─ escalation_rules.yaml
└─ delta_policy.yaml
```

Details: [`contracts/README.md`](./contracts/README.md)

## Contract Invariants (normative)

```text
promotion_delta=-6.25
→ pass

reobserve_multiplier=1.78
→ review

boundary_violation=1
→ fail
```

A change that alters these outcomes is a contract-breaking change.

## Validation

```bash
pip install pyyaml
python tools/validate_contracts.py
python tests/evaluate_examples.py
```

CI: `.github/workflows/contracts.yml` (Structure Lock + Behavior Lock)

## Version Policy

See [`GOVERNANCE.md`](./GOVERNANCE.md).

| Release | Lock |
| --- | --- |
| `contracts-v1.0` | Structure Lock |
| `contracts-v1.1` | Behavior Lock |
| `v2.x` | Contract Evolution |

## License

CC0 1.0 Universal (see `LICENSE`).
