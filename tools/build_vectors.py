#!/usr/bin/env python3
"""Generate deterministic public-evaluation vectors for Acceptance Plane."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from acceptance_plane_eval.canonical import digest_json, canonical_json
from acceptance_plane_eval.evaluator import evaluate_scenario

VECTOR_PATH = ROOT / "vectors" / "public_eval_vectors.jsonl"
EXAMPLE_DIR = ROOT / "examples" / "scenario_cards"

POLICY = {
    "policy_id": "ap-policy-public-eval",
    "version": "2026-06-11.v1",
    "trusted_measurements": [
        "sha256:runtime-accepted-001",
        "sha256:runtime-accepted-002",
    ],
    "require_target_binding": True,
    "require_nonce": True,
    "require_policy_digest_binding": True,
    "decision_profile": "accept-hold-refuse-v1",
}
POLICY_DIGEST = digest_json(POLICY)

BASE = {
    "schema": "AP-SCENARIO-CARD-v1",
    "scenario_id": "APV-000-ACCEPT-BASELINE",
    "title": "accepted production deploy with current verifier-ready evidence",
    "action": {
        "actor": "agent:deploy-bot",
        "operation": "deploy",
        "service": "orders-api",
        "target": "prod/orders-api",
        "risk": "medium",
        "requested_at": "2026-06-11T12:00:00Z",
        "parameters": {
            "artifact_digest": "sha256:artifact-orders-api-20260611",
            "change_ticket": "CHG-2026-0611-001",
        },
    },
    "authority": {
        "subject": "agent:deploy-bot",
        "delegation_id": "deleg-20260611-prod-orders",
        "scopes": ["deploy:orders-api", "rollback:orders-api"],
        "expires_at": "2026-06-11T12:10:00Z",
        "revoked": False,
        "max_risk": "medium",
    },
    "evidence": {
        "acceptance_boundary": "gateway:prod-deploy",
        "identity_valid": True,
        "runtime_attested": True,
        "attestation_measurement": "sha256:runtime-accepted-001",
        "target_binding": "prod/orders-api",
        "observed_at": "2026-06-11T11:59:30Z",
        "freshness_window_seconds": 300,
        "nonce": "nonce-APV-000",
        "approval_required": False,
        "approval_present": False,
        "transparency_required": True,
        "transparency_proof_present": True,
        "policy_digest": POLICY_DIGEST,
    },
    "policy": POLICY,
}


def variant(vector_id: str, title: str, mutator, expected_decision: str, expected_reason: str) -> dict:
    scenario = copy.deepcopy(BASE)
    scenario["scenario_id"] = vector_id
    scenario["title"] = title
    scenario["evidence"]["nonce"] = f"nonce-{vector_id}"
    mutator(scenario)
    return {
        "vector_id": vector_id,
        "scenario": scenario,
        "expected": {
            "decision": expected_decision,
            "reason_code": expected_reason,
        },
    }


def no_change(_):
    return None


VECTORS = [
    variant("APV-000-ACCEPT-BASELINE", "accepted production deploy with current verifier-ready evidence", no_change, "ACCEPT", "AP-000_ACCEPTED"),
    variant("APV-001-REFUSE-SUBJECT-MISMATCH", "actor does not match delegated subject", lambda s: s["authority"].update(subject="agent:other-bot"), "REFUSE", "AP-110_SUBJECT_MISMATCH"),
    variant("APV-002-REFUSE-IDENTITY-INVALID", "identity evidence fails", lambda s: s["evidence"].update(identity_valid=False), "REFUSE", "AP-111_IDENTITY_INVALID"),
    variant("APV-003-REFUSE-AUTHORITY-EXPIRED", "delegation expired before requested action", lambda s: s["authority"].update(expires_at="2026-06-11T11:00:00Z"), "REFUSE", "AP-120_AUTHORITY_EXPIRED"),
    variant("APV-004-REFUSE-AUTHORITY-REVOKED", "delegation revoked before impact", lambda s: s["authority"].update(revoked=True), "REFUSE", "AP-121_AUTHORITY_REVOKED"),
    variant("APV-005-REFUSE-SCOPE-MISMATCH", "operation outside delegated scope", lambda s: s["authority"].update(scopes=["read:orders-api"]), "REFUSE", "AP-122_SCOPE_MISMATCH"),
    variant("APV-006-REFUSE-TARGET-MISMATCH", "evidence bound to wrong target", lambda s: s["evidence"].update(target_binding="prod/payments-api"), "REFUSE", "AP-130_TARGET_MISMATCH"),
    variant("APV-007-HOLD-ATTESTATION-MISSING", "attestation not present", lambda s: s["evidence"].update(runtime_attested=False), "HOLD", "AP-140_ATTESTATION_MISSING"),
    variant("APV-008-REFUSE-ATTESTATION-UNTRUSTED", "runtime measurement not trusted", lambda s: s["evidence"].update(attestation_measurement="sha256:runtime-unknown"), "REFUSE", "AP-141_ATTESTATION_MEASUREMENT_UNTRUSTED"),
    variant("APV-009-REFUSE-POLICY-DIGEST-MISMATCH", "evidence is bound to stale policy digest", lambda s: s["evidence"].update(policy_digest="0" * 64), "REFUSE", "AP-150_POLICY_DIGEST_MISMATCH"),
    variant("APV-010-HOLD-EVIDENCE-STALE", "evidence observed outside freshness window", lambda s: s["evidence"].update(observed_at="2026-06-11T11:00:00Z"), "HOLD", "AP-160_EVIDENCE_STALE"),
    variant("APV-011-HOLD-APPROVAL-REQUIRED", "step-up approval missing", lambda s: s["evidence"].update(approval_required=True, approval_present=False), "HOLD", "AP-180_APPROVAL_REQUIRED"),
    variant("APV-012-HOLD-RISK-EXCEEDS-AUTHORITY", "risk exceeds delegated ceiling", lambda s: s["action"].update(risk="critical"), "HOLD", "AP-190_RISK_EXCEEDS_AUTHORITY"),
    variant("APV-013-HOLD-TRANSPARENCY-MISSING", "transparency proof required but absent", lambda s: s["evidence"].update(transparency_required=True, transparency_proof_present=False), "HOLD", "AP-200_TRANSPARENCY_PROOF_MISSING"),
    variant("APV-014-ACCEPT-WILDCARD-SCOPE", "wildcard scope accepts bounded service deploy", lambda s: s["authority"].update(scopes=["deploy:*"]), "ACCEPT", "AP-000_ACCEPTED"),
    variant("APV-015-ACCEPT-APPROVAL-PRESENT", "approval required and present", lambda s: s["evidence"].update(approval_required=True, approval_present=True), "ACCEPT", "AP-000_ACCEPTED"),
]

# Replay vector must intentionally reuse the previous vector's nonce and target.
replay = copy.deepcopy(BASE)
replay["scenario_id"] = "APV-016-REFUSE-REPLAY-DETECTED"
replay["title"] = "nonce replay at the same acceptance boundary"
replay["evidence"]["nonce"] = VECTORS[0]["scenario"]["evidence"]["nonce"]
VECTORS.append({"vector_id": replay["scenario_id"], "scenario": replay, "expected": {"decision": "REFUSE", "reason_code": "AP-170_REPLAY_DETECTED"}})

# Add broader matrix coverage.  These keep the primary failure dominant by
# starting from a fresh valid card and mutating one property.
for i in range(17, 64):
    selector = i % 12
    vid = f"APV-{i:03d}-MATRIX-{selector:02d}"
    if selector == 0:
        VECTORS.append(variant(vid, "matrix accept low-risk read action", lambda s, i=i: (s["action"].update(operation="read", risk="low"), s["authority"].update(scopes=["read:orders-api"], max_risk="low")), "ACCEPT", "AP-000_ACCEPTED"))
    elif selector == 1:
        VECTORS.append(variant(vid, "matrix revoked authority", lambda s: s["authority"].update(revoked=True), "REFUSE", "AP-121_AUTHORITY_REVOKED"))
    elif selector == 2:
        VECTORS.append(variant(vid, "matrix stale evidence", lambda s: s["evidence"].update(observed_at="2026-06-11T11:40:00Z", freshness_window_seconds=60), "HOLD", "AP-160_EVIDENCE_STALE"))
    elif selector == 3:
        VECTORS.append(variant(vid, "matrix target mismatch", lambda s: s["evidence"].update(target_binding="prod/other-api"), "REFUSE", "AP-130_TARGET_MISMATCH"))
    elif selector == 4:
        VECTORS.append(variant(vid, "matrix risk hold", lambda s: (s["action"].update(risk="high"), s["authority"].update(max_risk="medium")), "HOLD", "AP-190_RISK_EXCEEDS_AUTHORITY"))
    elif selector == 5:
        VECTORS.append(variant(vid, "matrix missing approval", lambda s: s["evidence"].update(approval_required=True, approval_present=False), "HOLD", "AP-180_APPROVAL_REQUIRED"))
    elif selector == 6:
        VECTORS.append(variant(vid, "matrix untrusted attestation", lambda s: s["evidence"].update(attestation_measurement="sha256:untrusted"), "REFUSE", "AP-141_ATTESTATION_MEASUREMENT_UNTRUSTED"))
    elif selector == 7:
        VECTORS.append(variant(vid, "matrix policy digest mismatch", lambda s: s["evidence"].update(policy_digest="f" * 64), "REFUSE", "AP-150_POLICY_DIGEST_MISMATCH"))
    elif selector == 8:
        VECTORS.append(variant(vid, "matrix accepted trusted alternate measurement", lambda s: s["evidence"].update(attestation_measurement="sha256:runtime-accepted-002"), "ACCEPT", "AP-000_ACCEPTED"))
    elif selector == 9:
        VECTORS.append(variant(vid, "matrix expired authority", lambda s: s["authority"].update(expires_at="2026-06-11T11:59:00Z"), "REFUSE", "AP-120_AUTHORITY_EXPIRED"))
    elif selector == 10:
        VECTORS.append(variant(vid, "matrix transparency missing", lambda s: s["evidence"].update(transparency_required=True, transparency_proof_present=False), "HOLD", "AP-200_TRANSPARENCY_PROOF_MISSING"))
    else:
        VECTORS.append(variant(vid, "matrix scope mismatch", lambda s: s["authority"].update(scopes=["approve:orders-api"]), "REFUSE", "AP-122_SCOPE_MISMATCH"))


def main() -> int:
    VECTOR_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    with VECTOR_PATH.open("w", encoding="utf-8") as fh:
        for vector in VECTORS:
            fh.write(canonical_json(vector).decode("utf-8") + "\n")
    examples = {
        "deploy_accept.json": VECTORS[0]["scenario"],
        "hold_approval_required.json": VECTORS[11]["scenario"],
        "refuse_revoked.json": VECTORS[4]["scenario"],
    }
    for name, scenario in examples.items():
        (EXAMPLE_DIR / name).write_text(json.dumps(scenario, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(VECTORS)} vectors to {VECTOR_PATH.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
