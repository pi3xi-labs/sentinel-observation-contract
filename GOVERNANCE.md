# Governance

## Canonical Repository

After Publication Lock, the canonical public contract is:

`pi3xi-labs/sentinel-observation-contract`

`wizyig/gbox` remains the operational / scaffolding repository.
It must point here as the canonical source of the published contract.

## Version Levels

### v1.0 — Structure Lock

- Contract files present (`observation_window`, `escalation_rules`, `delta_policy`)
- YAML parse integrity
- Observation IDs O01–O07
- Escalation IDs E001–E010
- `gate` section (`pass` / `review` / `fail`)
- CI contracts-check

### v1.1 — Behavior Lock

- Normative examples in `tests/contract_examples.yaml`
- Replay via `tests/evaluate_examples.py` against live `delta_policy` thresholds
- CI fails when published outcomes change without intentional revision

### v2.x — Contract Evolution

Breaking changes to observation semantics, escalation meaning, thresholds that alter normative outcomes, or gate vocabulary.

## Change Rules

- Structure or meaning breaks → Major (`v2.x`)
- Additive documentation, Behavior Lock fixtures, or non-semantic clarification → Minor (`v1.x`)
- Typo / formatting only → Patch (optional)

## Release Tags

Prefer tags of the form `contracts-vX.Y` pinned to a specific commit.

## Future Hardening (optional)

- Contract hash manifest
- Signed releases
