# Sentinel Observation Contract

A frozen audit contract for observation, escalation, and delta evaluation.

**Current Stable Release:** `contracts-v1.1`
**Compatibility Level:** Behavior Lock

## Repositories

Canonical public repository:

`pi3xi-labs/sentinel-observation-contract`

Operational repository:

`wizyig/gbox`

## Purpose

Observe → Escalate → Evaluate

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

