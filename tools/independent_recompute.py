#!/usr/bin/env python3
"""Independent recomputation of the public proof chain.

This script deliberately does not import acceptance_plane_eval.  It duplicates the
small canonicalization, evaluator, Merkle, and signature checks so reviewers can
see whether the generated proof artifacts are self-consistent from first
principles.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
except Exception as exc:  # pragma: no cover
    ed25519 = None
    CRYPTO_ERROR = exc
else:
    CRYPTO_ERROR = None

ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "vectors" / "public_eval_vectors.jsonl"
RESULTS_PATH = ROOT / "receipts" / "public_eval_results.json"
TRANSPARENCY_PATH = ROOT / "receipts" / "transparency-bundle.json"
RECEIPT_PATH = ROOT / "receipts" / "acceptance-plane-proof-receipt.json"

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
LEAF_PREFIX = b"AP-MERKLE-LEAF-v1\x00"
NODE_PREFIX = b"AP-MERKLE-NODE-v1\x00"


def c14n(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_json(obj: Any) -> str:
    return hashlib.sha256(c14n(obj)).hexdigest()


def parse_utc(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def policy_digest(policy: dict[str, Any]) -> str:
    return digest_json(policy)


def result_for(scenario: dict[str, Any], decision: str, reason_code: str) -> dict[str, Any]:
    action = scenario.get("action", {})
    evidence = scenario.get("evidence", {})
    policy = scenario.get("policy", {})
    core = {
        "profile": "AP-RECEIPT-CORE-v1",
        "scenario_id": scenario.get("scenario_id", "UNKNOWN"),
        "decision": decision,
        "reason_code": reason_code,
        "action_digest": digest_json(action),
        "evidence_digest": digest_json(evidence),
        "policy_digest": policy_digest(policy),
        "boundary": evidence.get("acceptance_boundary", "unknown"),
    }
    core["receipt_core_digest"] = digest_json({k: v for k, v in core.items() if k != "receipt_core_digest"})
    return {
        "decision": decision,
        "reason_code": reason_code,
        "receipt_digest": digest_json(core),
        "action_digest": core["action_digest"],
        "evidence_digest": core["evidence_digest"],
    }


def required_scope(action: dict[str, Any]) -> str:
    return f"{action.get('operation')}:{action.get('service', action.get('target', '*'))}"


def evaluate(scenario: dict[str, Any], seen: set[str]) -> dict[str, Any]:
    action = scenario.get("action", {})
    authority = scenario.get("authority", {})
    evidence = scenario.get("evidence", {})
    policy = scenario.get("policy", {})
    for obj in (action, authority, evidence, policy):
        if not isinstance(obj, dict):
            return result_for(scenario, "HOLD", "AP-101_MISSING_FIELD")
    if action.get("actor") != authority.get("subject"):
        return result_for(scenario, "REFUSE", "AP-110_SUBJECT_MISMATCH")
    if evidence.get("identity_valid") is not True:
        return result_for(scenario, "REFUSE", "AP-111_IDENTITY_INVALID")
    requested_at = parse_utc(str(action.get("requested_at")))
    if parse_utc(str(authority.get("expires_at"))) < requested_at:
        return result_for(scenario, "REFUSE", "AP-120_AUTHORITY_EXPIRED")
    if authority.get("revoked") is True:
        return result_for(scenario, "REFUSE", "AP-121_AUTHORITY_REVOKED")
    scopes = set(authority.get("scopes", []))
    req = required_scope(action)
    wildcard = f"{action.get('operation')}:*"
    if req not in scopes and wildcard not in scopes:
        return result_for(scenario, "REFUSE", "AP-122_SCOPE_MISMATCH")
    if evidence.get("target_binding") != action.get("target"):
        return result_for(scenario, "REFUSE", "AP-130_TARGET_MISMATCH")
    if evidence.get("runtime_attested") is not True:
        return result_for(scenario, "HOLD", "AP-140_ATTESTATION_MISSING")
    if evidence.get("attestation_measurement") not in set(policy.get("trusted_measurements", [])):
        return result_for(scenario, "REFUSE", "AP-141_ATTESTATION_MEASUREMENT_UNTRUSTED")
    if evidence.get("policy_digest") != policy_digest(policy):
        return result_for(scenario, "REFUSE", "AP-150_POLICY_DIGEST_MISMATCH")
    observed_at = parse_utc(str(evidence.get("observed_at")))
    if abs((requested_at - observed_at).total_seconds()) > int(evidence.get("freshness_window_seconds", 0)):
        return result_for(scenario, "HOLD", "AP-160_EVIDENCE_STALE")
    nonce = str(evidence.get("nonce", ""))
    if not nonce:
        return result_for(scenario, "HOLD", "AP-101_MISSING_FIELD")
    replay_key = f"{action.get('target')}:{nonce}"
    if replay_key in seen:
        return result_for(scenario, "REFUSE", "AP-170_REPLAY_DETECTED")
    seen.add(replay_key)
    if evidence.get("approval_required") is True and evidence.get("approval_present") is not True:
        return result_for(scenario, "HOLD", "AP-180_APPROVAL_REQUIRED")
    if RISK_ORDER.get(str(action.get("risk", "low")), 999) > RISK_ORDER.get(str(authority.get("max_risk", "low")), -1):
        return result_for(scenario, "HOLD", "AP-190_RISK_EXCEEDS_AUTHORITY")
    if evidence.get("transparency_required") is True and evidence.get("transparency_proof_present") is not True:
        return result_for(scenario, "HOLD", "AP-200_TRANSPARENCY_PROOF_MISSING")
    return result_for(scenario, "ACCEPT", "AP-000_ACCEPTED")


def leaf_hash(data: bytes) -> str:
    return hashlib.sha256(LEAF_PREFIX + data).hexdigest()


def node_hash(left: str, right: str) -> str:
    return hashlib.sha256(NODE_PREFIX + bytes.fromhex(left) + bytes.fromhex(right)).hexdigest()


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return hashlib.sha256(b"AP-MERKLE-EMPTY-v1").hexdigest()
    level = leaves[:]
    while len(level) > 1:
        level = [node_hash(level[i], level[i + 1] if i + 1 < len(level) else level[i]) for i in range(0, len(level), 2)]
    return level[0]


def verify_inclusion(leaf: str, proof: list[dict[str, str]], root: str) -> bool:
    cur = leaf
    for step in proof:
        if step["side"] == "left":
            cur = node_hash(step["hash"], cur)
        elif step["side"] == "right":
            cur = node_hash(cur, step["hash"])
        else:
            return False
    return cur == root


def verify_sig(message: bytes, signature_b64: str, public_key_b64: str) -> None:
    if ed25519 is None:
        raise RuntimeError(f"cryptography Ed25519 backend unavailable: {CRYPTO_ERROR}")
    key = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
    key.verify(base64.b64decode(signature_b64), message)


def check(name: str, ok: bool, failures: list[str]) -> None:
    if not ok:
        failures.append(name)


def main() -> int:
    failures: list[str] = []
    checks = 0
    vectors = [json.loads(line) for line in VECTOR_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    transparency = json.loads(TRANSPARENCY_PATH.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))

    checks += 1; check("vector count is 64", len(vectors) == 64, failures)
    seen: set[str] = set()
    recomputed_items = []
    for vector in vectors:
        got = evaluate(vector["scenario"], seen)
        expected = vector["expected"]
        ok = got["decision"] == expected["decision"] and got["reason_code"] == expected["reason_code"]
        recomputed_items.append({
            "vector_id": vector["vector_id"],
            "ok": ok,
            "expected": expected,
            "observed": {"decision": got["decision"], "reason_code": got["reason_code"]},
            "receipt_digest": got["receipt_digest"],
            "action_digest": got["action_digest"],
            "evidence_digest": got["evidence_digest"],
        })
    checks += 1; check("all vectors match expected", all(x["ok"] for x in recomputed_items), failures)
    checks += 1; check("results items match recomputation", results["results"] == recomputed_items, failures)
    checks += 1; check("results digest matches", results["results_digest"] == digest_json(recomputed_items), failures)
    checks += 1; check("results summary count", results["passed"] == 64 and results["failed"] == 0, failures)

    leaves = []
    for idx, item in enumerate(recomputed_items):
        payload = {"index": idx, "vector_id": item["vector_id"], "receipt_digest": item["receipt_digest"], "observed": item["observed"]}
        leaves.append(leaf_hash(c14n(payload)))
    root = merkle_root(leaves)
    checks += 1; check("transparency root matches", root == transparency["tree_head"]["root_hash"], failures)
    checks += 1; check("transparency leaves match", [x["leaf_hash"] for x in transparency["leaves"]] == leaves, failures)
    checks += 1; check("transparency selected proofs verify", all(verify_inclusion(p["leaf_hash"], p["proof"], root) for p in transparency["selected_inclusion_proofs"]), failures)
    try:
        verify_sig(c14n(transparency["tree_head"]), transparency["tree_head_signature_base64"], transparency["tree_head"]["public_eval_key"]["public_key_base64"])
        sig_ok = True
    except Exception:
        sig_ok = False
    checks += 1; check("transparency tree head signature", sig_ok, failures)

    core = receipt["receipt_core"]
    checks += 1; check("proof receipt digest", digest_json(core) == receipt["receipt_core_digest"], failures)
    try:
        verify_sig(c14n(core), receipt["receipt_core_signature_base64"], core["public_eval_key"]["public_key_base64"])
        receipt_sig_ok = True
    except Exception:
        receipt_sig_ok = False
    checks += 1; check("proof receipt signature", receipt_sig_ok, failures)
    checks += 1; check("proof receipt binds results digest", core["public_eval"]["results_digest"] == results["results_digest"], failures)
    checks += 1; check("proof receipt binds transparency root", core["transparency"]["root_hash"] == root, failures)

    passed = checks - len(failures)
    if failures:
        print(f"independent recomputation: {passed} / {checks} PASS")
        for failure in failures:
            print(f"- FAIL {failure}")
        return 1
    print(f"independent recomputation: {passed} / {checks} PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
