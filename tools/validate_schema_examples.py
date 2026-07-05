#!/usr/bin/env python3
"""Validate scenario examples against the constrained public schema profile."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "scenario_cards"

REQUIRED = {
    "scenario_id": str,
    "action": dict,
    "authority": dict,
    "evidence": dict,
    "policy": dict,
}
SECTION_REQUIRED = {
    "action": ["actor", "operation", "service", "target", "risk", "requested_at"],
    "authority": ["subject", "scopes", "expires_at", "revoked", "max_risk"],
    "evidence": ["identity_valid", "runtime_attested", "attestation_measurement", "target_binding", "observed_at", "freshness_window_seconds", "nonce", "policy_digest"],
    "policy": ["policy_id", "version", "trusted_measurements"],
}


def validate(path: Path) -> list[str]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for key, typ in REQUIRED.items():
        if key not in obj:
            errors.append(f"missing {key}")
        elif not isinstance(obj[key], typ):
            errors.append(f"{key} must be {typ.__name__}")
    for section, keys in SECTION_REQUIRED.items():
        sec = obj.get(section, {})
        if isinstance(sec, dict):
            for key in keys:
                if key not in sec:
                    errors.append(f"missing {section}.{key}")
    return errors


def main() -> int:
    paths = sorted(EXAMPLES.glob("*.json"))
    failures = []
    for path in paths:
        errors = validate(path)
        if errors:
            failures.append((path, errors))
    if failures:
        print("schema example validation: FAIL")
        for path, errors in failures:
            print(path.relative_to(ROOT))
            for error in errors:
                print(f"- {error}")
        return 1
    print(f"schema example validation: PASS ({len(paths)} examples)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
