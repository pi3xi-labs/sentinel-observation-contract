# Sentinel Observation Contract

A frozen audit contract for observation, escalation, and delta evaluation.

**Current Release:** `contracts-v1.4` — Sigstore Verification  
**Compatibility Level:** Sigstore Verification

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
python tools/generate_manifest.py --check
```

## Compatibility Stack

```text
Structure Lock          v1.0
    ↓
Behavior Lock           v1.1
    ↓
Integrity Lock          v1.2
    ↓
Signature Lock          v1.3
    ↓
Sigstore Verification   v1.4
```

A release claiming a lock level satisfies all lower levels.

## Verifying a release

Each release from `contracts-v1.4` onward ships a Sigstore bundle produced by `.github/workflows/sign-release.yml` on the release tag.

1. Download `contracts-v1.4.json` (from `manifest/` at tag `contracts-v1.4`, or from the Release assets).
2. Download `contracts-v1.4.bundle` from the Release assets.
3. Verify with [cosign](https://github.com/sigstore/cosign) v3:

```bash
cosign verify-blob contracts-v1.4.json \
  --bundle contracts-v1.4.bundle \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity https://github.com/pi3xi-labs/sentinel-observation-contract/.github/workflows/sign-release.yml@refs/tags/contracts-v1.4
```

Verification fails if the issuer, the workflow identity, the manifest contents, or the bundle differ. See `GOVERNANCE.md` → Sigstore Provenance Requirements.

## Lock Model

```text
v1.0  Structure Lock
v1.1  Behavior Lock
v1.2  Integrity Lock
v1.3  Signature Lock
v1.4  Sigstore Verification
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
- Manifest reproducibility
- Release tag format (`contracts-vMAJOR.MINOR`, on tags)

Release signing (`sign-release.yml`, on Release publish):

- cosign keyless signing of the manifest (GitHub OIDC)
- positive verification with issuer + workflow identity
- negative verification (wrong issuer, wrong identity, tampered manifest, tampered bundle)

## Governance

See:

`GOVERNANCE.md`

## License

CC0 1.0 Universal
