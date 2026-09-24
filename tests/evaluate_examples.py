#!/usr/bin/env python3
"""CI-05: Behavior Lock — replay normative examples against delta_policy thresholds."""

from __future__ import annotations

from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML is required: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
EXAMPLES = ROOT / "tests" / "contract_examples.yaml"

# Public example metric names → delta_policy metrics keys
METRIC_ALIASES = {
    "promotion_delta": "promotion_ratio",
    "reobserve_multiplier": "reobserve_ratio",
    "boundary_violation": "boundary_violation_count",
}


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def evaluate(metric: str, value: float, metrics: dict) -> str:
    """Derive pass/review/fail from live contract thresholds (not hard-coded)."""
    key = METRIC_ALIASES.get(metric, metric)
    spec = metrics.get(key)
    if not isinstance(spec, dict):
        raise ValueError(f"unknown metric in delta_policy: {metric} ({key})")

    compare = spec.get("compare") or {}

    if "max_delta_percent" in compare:
        threshold = float(compare["max_delta_percent"])
        return "pass" if abs(float(value)) <= threshold else "review"

    if "max_multiplier" in compare:
        threshold = float(compare["max_multiplier"])
        return "review" if float(value) > threshold else "pass"

    if "absolute" in compare:
        absolute = float(compare["absolute"])
        return "fail" if float(value) > absolute else "pass"

    raise ValueError(f"unsupported compare for {key}: {compare}")


def main() -> None:
    delta = load_yaml(CONTRACTS / "delta_policy.yaml")
    metrics = delta.get("metrics")
    if not isinstance(metrics, dict):
        fail("delta_policy.metrics missing or not a mapping")

    payload = load_yaml(EXAMPLES)
    examples = payload.get("examples") if isinstance(payload, dict) else None
    if not isinstance(examples, list) or not examples:
        fail("tests/contract_examples.yaml has no examples")

    errors = []
    for case in examples:
        name = case.get("name", "?")
        try:
            actual = evaluate(case["metric"], case["value"], metrics)
        except Exception as exc:  # noqa: BLE001 — surface as CI failure
            fail(f"{name}: {exc}")
        expected = case.get("expected")
        if actual != expected:
            errors.append((name, actual, expected))

    if errors:
        for name, actual, expected in errors:
            print(f"[FAIL] {name}: actual={actual} expected={expected}")
        sys.exit(1)

    print("[PASS] example evaluation")


if __name__ == "__main__":
    main()
