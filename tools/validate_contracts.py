#!/usr/bin/env python3
"""Validate frozen Sentinel Observation Contract files for structural integrity."""

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

REQUIRED_FILES = [
    "observation_window.yaml",
    "escalation_rules.yaml",
    "delta_policy.yaml",
]


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def main() -> None:
    for name in REQUIRED_FILES:
        target = CONTRACTS / name
        if not target.exists():
            fail(f"missing contract: {name}")

    observation = load_yaml(CONTRACTS / "observation_window.yaml")
    escalation = load_yaml(CONTRACTS / "escalation_rules.yaml")
    delta = load_yaml(CONTRACTS / "delta_policy.yaml")

    # O01-O07 are dict keys (not list items with id)
    obs = observation.get("observations")
    if not isinstance(obs, dict):
        fail(f"observations must be a mapping, got {type(obs).__name__}")

    expected_obs = [f"O{i:02d}" for i in range(1, 8)]
    actual_obs = list(obs.keys())
    if actual_obs != expected_obs:
        fail(f"O01-O07 sequence mismatch: {actual_obs}")

    window = observation.get("window") or {}
    if window.get("name") != "boundary_integrity_observation":
        fail("window.name mismatch")
    if window.get("duration") != "7d":
        fail("window.duration mismatch")
    if window.get("start") != "2026-09-25T00:00:00+09:00":
        fail("window.start mismatch")

    # E001-E010
    esc_rules = escalation.get("rules")
    if not isinstance(esc_rules, list):
        fail("escalation rules must be a list")
    esc_ids = [x.get("id") for x in esc_rules]
    expected_esc = [f"E{i:03d}" for i in range(1, 11)]
    if esc_ids != expected_esc:
        fail(f"E001-E010 sequence mismatch: {esc_ids}")

    if "gate" not in delta:
        fail("missing gate section")
    gate = delta["gate"]
    for required in ("pass", "review", "fail"):
        if required not in gate:
            fail(f"missing gate.{required}")

    baseline = delta.get("baseline") or {}
    if baseline.get("source") != "sentineltrinity":
        fail("baseline.source mismatch")
    if baseline.get("period") != "previous_90d":
        fail("baseline.period mismatch")

    print("[PASS] contracts validation completed")


if __name__ == "__main__":
    main()
