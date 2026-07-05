#!/usr/bin/env python3
"""Generate a signed Merkle transparency bundle for public-eval results."""
from __future__ import annotations

import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from acceptance_plane_eval.canonical import canonical_json, digest_json
from acceptance_plane_eval.crypto_profile import public_eval_key, sign, PROFILE
from acceptance_plane_eval.transparency import leaf_hash, merkle_root, inclusion_proof

RESULTS = ROOT / "receipts" / "public_eval_results.json"
OUT = ROOT / "receipts" / "transparency-bundle.json"


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    items = results["results"]
    leaves = []
    for idx, item in enumerate(items):
        payload = {
            "index": idx,
            "vector_id": item["vector_id"],
            "receipt_digest": item["receipt_digest"],
            "observed": item["observed"],
        }
        leaves.append({"index": idx, "vector_id": item["vector_id"], "leaf_hash": leaf_hash(canonical_json(payload)), "payload_digest": digest_json(payload)})
    root = merkle_root([x["leaf_hash"] for x in leaves])
    selected_indices = sorted(set([0, 1, len(leaves)//2, len(leaves)-1]))
    proofs = []
    leaf_hashes = [x["leaf_hash"] for x in leaves]
    for idx in selected_indices:
        proofs.append({
            "index": idx,
            "vector_id": leaves[idx]["vector_id"],
            "leaf_hash": leaves[idx]["leaf_hash"],
            "proof": inclusion_proof(leaf_hashes, idx),
        })
    tree_head = {
        "profile": "AP-TRANSPARENCY-BUNDLE-v1",
        "tree_size": len(leaves),
        "root_hash": root,
        "results_digest": results["results_digest"],
        "hash_algorithm": "SHA-256",
        "signature_profile": PROFILE,
        "public_eval_key": public_eval_key(),
    }
    bundle = {
        "tree_head": tree_head,
        "tree_head_signature_base64": sign(canonical_json(tree_head)),
        "leaves": leaves,
        "selected_inclusion_proofs": proofs,
        "notes": [
            "This is a deterministic public-evaluation transparency bundle.",
            "The signing key is public-eval only and is not a production trust root.",
        ],
    }
    OUT.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote transparency bundle: {OUT.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
