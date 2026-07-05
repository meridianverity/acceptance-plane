from __future__ import annotations

import json
from pathlib import Path

from acceptance_plane_eval.evaluator import evaluate_scenario

ROOT = Path(__file__).resolve().parents[1]


def load_vectors():
    path = ROOT / "vectors" / "public_eval_vectors.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_vector_suite_has_expected_size_and_passes():
    vectors = load_vectors()
    assert len(vectors) == 64
    seen: set[str] = set()
    for vector in vectors:
        got = evaluate_scenario(vector["scenario"], seen_nonces=seen)
        assert got["decision"] == vector["expected"]["decision"], vector["vector_id"]
        assert got["reason_code"] == vector["expected"]["reason_code"], vector["vector_id"]
        assert len(got["receipt_digest"]) == 64


def test_replay_vector_is_refused():
    vectors = load_vectors()
    replay = [v for v in vectors if v["vector_id"] == "APV-016-REFUSE-REPLAY-DETECTED"][0]
    seen: set[str] = set()
    # Prime the nonce with the baseline vector, then evaluate the replay vector.
    evaluate_scenario(vectors[0]["scenario"], seen_nonces=seen)
    got = evaluate_scenario(replay["scenario"], seen_nonces=seen)
    assert got["decision"] == "REFUSE"
    assert got["reason_code"] == "AP-170_REPLAY_DETECTED"
