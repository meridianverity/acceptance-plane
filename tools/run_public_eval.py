#!/usr/bin/env python3
"""Run the Acceptance Plane public-evaluation vector suite."""
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

DEFAULT_VECTOR_PATH = ROOT / "vectors" / "public_eval_vectors.jsonl"
DEFAULT_RESULTS_PATH = ROOT / "receipts" / "public_eval_results.json"


def load_vectors(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run(vectors: list[dict]) -> tuple[list[dict], int]:
    seen: set[str] = set()
    results: list[dict] = []
    failures = 0
    for vector in vectors:
        got = evaluate_scenario(vector["scenario"], seen_nonces=seen)
        expected = vector["expected"]
        ok = got["decision"] == expected["decision"] and got["reason_code"] == expected["reason_code"]
        if not ok:
            failures += 1
        results.append({
            "vector_id": vector["vector_id"],
            "ok": ok,
            "expected": expected,
            "observed": {"decision": got["decision"], "reason_code": got["reason_code"]},
            "receipt_digest": got["receipt_digest"],
            "action_digest": got["receipt_core"]["action_digest"],
            "evidence_digest": got["receipt_core"]["evidence_digest"],
        })
    return results, failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", type=Path, default=DEFAULT_VECTOR_PATH)
    ap.add_argument("--write-results", type=Path, default=None)
    args = ap.parse_args()
    vectors = load_vectors(args.vectors)
    results, failures = run(vectors)
    passed = len(results) - failures
    summary = {
        "profile": "AP-PUBLIC-EVAL-v1",
        "vector_count": len(results),
        "passed": passed,
        "failed": failures,
        "results_digest": digest_json(results),
        "results": results,
    }
    out = args.write_results
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Acceptance Plane public eval: {passed} / {len(results)} PASS")
    if failures:
        for item in results:
            if not item["ok"]:
                print(f"FAIL {item['vector_id']}: expected={item['expected']} observed={item['observed']}")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
