# Sentinel Observation Contract v1.1

監査層の観測契約。

v1.0 で Structure Lock（契約存在・YAML・gate・CI）、v1.1 で Behavior Lock（規範例の判定再現）を固定する。

Observe → Escalate → Evaluate の3層を分離する。

## Contract Set

```text
contracts/
├─ observation_window.yaml
├─ escalation_rules.yaml
└─ delta_policy.yaml
```

### observation_window.yaml

7日観測ウィンドウ。

対象:

- O01
- O02
- O03
- O04
- O05
- O06
- O07

開始日時:

`2026-09-25T00:00:00+09:00`

### escalation_rules.yaml

エスカレーション契約。

定義:

E001–E010

### delta_policy.yaml

90日ベースラインとの比較契約。

SentinelTrinity による差分評価を実施し、最終判定を `gate` セクションで実施する。

## Decision Examples

### promotion_delta

入力: `-6.25%`  
判定: `PASS`  
理由: threshold ±20%

### reobserve_multiplier

入力: `1.78`  
判定: `REVIEW`（公開例の WARNING に相当）  
理由: threshold ×1.5

### boundary_violation

入力: `1`  
判定: `FAIL` / `CRITICAL`  
理由: boundary violation > 0

## Contract Invariants

The following examples are normative.

```text
promotion_delta=-6.25
→ pass

reobserve_multiplier=1.78
→ review

boundary_violation=1
→ fail
```

A change that alters these outcomes must be treated as a contract-breaking change.

Normative vectors live in `tests/contract_examples.yaml` and are replayed by `tests/evaluate_examples.py` against live thresholds in `delta_policy.yaml`.

## Validation

```bash
pip install pyyaml
python tools/validate_contracts.py
python tests/evaluate_examples.py
```

CI: `.github/workflows/contracts.yml`（CI-01〜04 + CI-05 Behavior Lock）

## Stability Policy

契約 YAML の構造・閾値意味論を破る変更は Major（v2.x）。

Behavior Lock（例示・判定再現）の追加や説明追加など後方互換な変更は Minor（v1.x）。

v1.0 = Structure Lock  
v1.1 = Behavior Lock
