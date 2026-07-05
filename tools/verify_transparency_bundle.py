#!/usr/bin/env python3
"""Verify the public-eval transparency bundle."""
from __future__ import annotations

import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from acceptance_plane_eval.canonical import canonical_json
from acceptance_plane_eval.crypto_profile import verify
from acceptance_plane_eval.transparency import merkle_root, verify_inclusion

BUNDLE = ROOT / "receipts" / "transparency-bundle.json"


def main() -> int:
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    leaves = [item["leaf_hash"] for item in bundle["leaves"]]
    root = merkle_root(leaves)
    expected = bundle["tree_head"]["root_hash"]
    errors: list[str] = []
    if root != expected:
        errors.append("root hash mismatch")
    try:
        verify(
            canonical_json(bundle["tree_head"]),
            bundle["tree_head_signature_base64"],
            bundle["tree_head"]["public_eval_key"]["public_key_base64"],
        )
    except Exception as exc:
        errors.append(f"tree head signature failed: {exc}")
    for proof in bundle["selected_inclusion_proofs"]:
        ok = verify_inclusion(proof["leaf_hash"], proof["index"], proof["proof"], expected)
        if not ok:
            errors.append(f"inclusion proof failed: {proof['vector_id']}")
    if errors:
        print("transparency bundle: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("transparency bundle: PASS")
    print("root_hash: OK")
    print("selected inclusion proofs: OK")
    print("signed tree head: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
