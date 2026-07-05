"""Deterministic reference evaluator for Acceptance Plane scenario cards."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

from .canonical import digest_json

DECISIONS = {"ACCEPT", "HOLD", "REFUSE"}
RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}

REASON_TEXT = {
    "AP-000_ACCEPTED": "Evidence is current, scoped, target-bound, non-revoked, non-replayed, and sufficient.",
    "AP-101_MISSING_FIELD": "Scenario card is missing a required field.",
    "AP-110_SUBJECT_MISMATCH": "Action actor and authority subject do not match.",
    "AP-111_IDENTITY_INVALID": "Identity evidence is invalid.",
    "AP-120_AUTHORITY_EXPIRED": "Authority expired before the requested action time.",
    "AP-121_AUTHORITY_REVOKED": "Authority has been revoked.",
    "AP-122_SCOPE_MISMATCH": "Requested operation is outside authority scope.",
    "AP-130_TARGET_MISMATCH": "Evidence is not bound to the requested target.",
    "AP-140_ATTESTATION_MISSING": "Runtime or workload attestation evidence is missing.",
    "AP-141_ATTESTATION_MEASUREMENT_UNTRUSTED": "Runtime measurement is not in the trusted measurement set.",
    "AP-150_POLICY_DIGEST_MISMATCH": "Evaluated policy digest does not match the policy digest in evidence.",
    "AP-160_EVIDENCE_STALE": "Evidence is older than the allowed freshness window.",
    "AP-170_REPLAY_DETECTED": "Nonce has already been observed for this action boundary.",
    "AP-180_APPROVAL_REQUIRED": "Step-up approval is required but not present.",
    "AP-190_RISK_EXCEEDS_AUTHORITY": "Action risk exceeds the delegated authority ceiling.",
    "AP-200_TRANSPARENCY_PROOF_MISSING": "Transparency proof is required but missing.",
}

class EvaluationError(ValueError):
    pass


def parse_utc(value: str) -> datetime:
    if not isinstance(value, str):
        raise EvaluationError("timestamp must be a string")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise EvaluationError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def _get(obj: dict[str, Any], path: str) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur


def _policy_digest(policy: dict[str, Any]) -> str:
    return digest_json(policy)


def _required_scope(action: dict[str, Any]) -> str:
    service = action.get("service", action.get("target", "*"))
    return f"{action.get('operation')}:{service}"


def _result(scenario: dict[str, Any], decision: str, reason_code: str, detail: str | None = None) -> dict[str, Any]:
    action = scenario.get("action", {}) if isinstance(scenario, dict) else {}
    evidence = scenario.get("evidence", {}) if isinstance(scenario, dict) else {}
    policy = scenario.get("policy", {}) if isinstance(scenario, dict) else {}
    receipt_core = {
        "profile": "AP-RECEIPT-CORE-v1",
        "scenario_id": scenario.get("scenario_id", "UNKNOWN") if isinstance(scenario, dict) else "UNKNOWN",
        "decision": decision,
        "reason_code": reason_code,
        "action_digest": digest_json(action),
        "evidence_digest": digest_json(evidence),
        "policy_digest": _policy_digest(policy) if isinstance(policy, dict) else digest_json({}),
        "boundary": evidence.get("acceptance_boundary", "unknown") if isinstance(evidence, dict) else "unknown",
    }
    receipt_core["receipt_core_digest"] = digest_json({k: v for k, v in receipt_core.items() if k != "receipt_core_digest"})
    return {
        "scenario_id": receipt_core["scenario_id"],
        "decision": decision,
        "reason_code": reason_code,
        "reason_text": REASON_TEXT.get(reason_code, "Unspecified reason."),
        "detail": detail or REASON_TEXT.get(reason_code, ""),
        "receipt_core": receipt_core,
        "receipt_digest": digest_json(receipt_core),
    }


def evaluate_scenario(scenario: dict[str, Any], seen_nonces: set[str] | None = None) -> dict[str, Any]:
    """Evaluate one scenario card using the public reference profile.

    Decisions are intentionally conservative: incomplete evidence yields HOLD and
    failed evidence yields REFUSE.
    """
    seen_nonces = seen_nonces if seen_nonces is not None else set()
    try:
        action = _get(scenario, "action")
        authority = _get(scenario, "authority")
        evidence = _get(scenario, "evidence")
        policy = _get(scenario, "policy")
    except KeyError as exc:
        return _result(scenario, "HOLD", "AP-101_MISSING_FIELD", f"missing {exc.args[0]}")

    for name, value in (("action", action), ("authority", authority), ("evidence", evidence), ("policy", policy)):
        if not isinstance(value, dict):
            return _result(scenario, "HOLD", "AP-101_MISSING_FIELD", f"{name} must be an object")

    actor = action.get("actor")
    if actor != authority.get("subject"):
        return _result(scenario, "REFUSE", "AP-110_SUBJECT_MISMATCH")

    if evidence.get("identity_valid") is not True:
        return _result(scenario, "REFUSE", "AP-111_IDENTITY_INVALID")

    requested_at = parse_utc(str(action.get("requested_at")))
    expires_at = parse_utc(str(authority.get("expires_at")))
    if expires_at < requested_at:
        return _result(scenario, "REFUSE", "AP-120_AUTHORITY_EXPIRED")

    if authority.get("revoked") is True:
        return _result(scenario, "REFUSE", "AP-121_AUTHORITY_REVOKED")

    scopes = set(authority.get("scopes", []))
    required_scope = _required_scope(action)
    wildcard_scope = f"{action.get('operation')}:*"
    if required_scope not in scopes and wildcard_scope not in scopes:
        return _result(scenario, "REFUSE", "AP-122_SCOPE_MISMATCH", f"required {required_scope}")

    if evidence.get("target_binding") != action.get("target"):
        return _result(scenario, "REFUSE", "AP-130_TARGET_MISMATCH")

    if evidence.get("runtime_attested") is not True:
        return _result(scenario, "HOLD", "AP-140_ATTESTATION_MISSING")

    trusted = set(policy.get("trusted_measurements", []))
    measurement = evidence.get("attestation_measurement")
    if measurement not in trusted:
        return _result(scenario, "REFUSE", "AP-141_ATTESTATION_MEASUREMENT_UNTRUSTED")

    expected_policy_digest = _policy_digest(policy)
    if evidence.get("policy_digest") != expected_policy_digest:
        return _result(scenario, "REFUSE", "AP-150_POLICY_DIGEST_MISMATCH")

    observed_at = parse_utc(str(evidence.get("observed_at")))
    freshness_window_seconds = int(evidence.get("freshness_window_seconds", 0))
    age = abs((requested_at - observed_at).total_seconds())
    if age > freshness_window_seconds:
        return _result(scenario, "HOLD", "AP-160_EVIDENCE_STALE", f"age={int(age)}s window={freshness_window_seconds}s")

    nonce = str(evidence.get("nonce", ""))
    if not nonce:
        return _result(scenario, "HOLD", "AP-101_MISSING_FIELD", "missing evidence.nonce")
    replay_key = f"{action.get('target')}:{nonce}"
    if replay_key in seen_nonces:
        return _result(scenario, "REFUSE", "AP-170_REPLAY_DETECTED")
    seen_nonces.add(replay_key)

    if evidence.get("approval_required") is True and evidence.get("approval_present") is not True:
        return _result(scenario, "HOLD", "AP-180_APPROVAL_REQUIRED")

    action_risk = str(action.get("risk", "low"))
    max_risk = str(authority.get("max_risk", "low"))
    if RISK_ORDER.get(action_risk, 999) > RISK_ORDER.get(max_risk, -1):
        return _result(scenario, "HOLD", "AP-190_RISK_EXCEEDS_AUTHORITY", f"risk={action_risk} max={max_risk}")

    if evidence.get("transparency_required") is True and evidence.get("transparency_proof_present") is not True:
        return _result(scenario, "HOLD", "AP-200_TRANSPARENCY_PROOF_MISSING")

    return _result(scenario, "ACCEPT", "AP-000_ACCEPTED")


def evaluate_vectors(vectors: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    results: list[dict[str, Any]] = []
    for vector in vectors:
        scenario = vector.get("scenario", vector)
        results.append(evaluate_scenario(scenario, seen_nonces=seen))
    return results
