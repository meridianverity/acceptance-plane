#!/usr/bin/env python3
"""Lint and evaluate one Acceptance Plane scenario card."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from acceptance_plane_eval.evaluator import evaluate_scenario
from acceptance_plane_eval.canonical import digest_json

REQUIRED = {
    "action": ["actor", "operation", "target", "requested_at"],
    "authority": ["subject", "scopes", "expires_at", "revoked", "max_risk"],
    "evidence": ["identity_valid", "runtime_attested", "target_binding", "observed_at", "freshness_window_seconds", "nonce", "policy_digest"],
    "policy": ["policy_id", "version", "trusted_measurements"],
}


def lint(card: dict) -> list[str]:
    findings: list[str] = []
    for section, keys in REQUIRED.items():
        if section not in card or not isinstance(card[section], dict):
            findings.append(f"missing object: {section}")
            continue
        for key in keys:
            if key not in card[section]:
                findings.append(f"missing field: {section}.{key}")
    if "policy" in card and "evidence" in card:
        if card["evidence"].get("policy_digest") != digest_json(card["policy"]):
            findings.append("evidence.policy_digest does not match canonical policy digest")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("card", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    card = json.loads(args.card.read_text(encoding="utf-8"))
    findings = lint(card)
    result = evaluate_scenario(card)
    payload = {"scenario_id": card.get("scenario_id"), "findings": findings, "result": result}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"scenario: {payload['scenario_id']}")
        print(f"lint findings: {len(findings)}")
        for finding in findings:
            print(f"- {finding}")
        print(f"decision: {result['decision']} {result['reason_code']}")
        print(f"receipt_digest: {result['receipt_digest']}")
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())
