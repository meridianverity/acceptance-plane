#!/usr/bin/env python3
"""Generate the Acceptance Plane proof receipt."""
from __future__ import annotations

import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from acceptance_plane_eval.canonical import canonical_json, digest_json
from acceptance_plane_eval.crypto_profile import public_eval_key, sign, PROFILE

OUT = ROOT / "receipts" / "acceptance-plane-proof-receipt.json"


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    results = load_json("receipts/public_eval_results.json")
    transparency = load_json("receipts/transparency-bundle.json")
    receipt_core = {
        "profile": "AP-PROOF-RECEIPT-v1",
        "package": "acceptance-plane",
        "version": "1.0.1-hardened-public-eval",
        "canonical_doi": "10.5281/zenodo.20645907",
        "public_eval": {
            "vector_count": results["vector_count"],
            "passed": results["passed"],
            "failed": results["failed"],
            "results_digest": results["results_digest"],
        },
        "transparency": {
            "tree_size": transparency["tree_head"]["tree_size"],
            "root_hash": transparency["tree_head"]["root_hash"],
            "tree_head_signature_base64": transparency["tree_head_signature_base64"],
        },
        "claims_boundary": {
            "not_a_standard": True,
            "not_a_product_implementation": True,
            "not_a_compliance_certification": True,
            "no_patent_license": True,
            "public_eval_only": True,
        },
        "signature_profile": PROFILE,
        "public_eval_key": public_eval_key(),
    }
    receipt = {
        "receipt_core": receipt_core,
        "receipt_core_digest": digest_json(receipt_core),
        "receipt_core_signature_base64": sign(canonical_json(receipt_core)),
        "verification_notes": [
            "Use tools/verify_proof_receipt.py for receipt self-check and optional archive binding.",
            "The Ed25519 key is deterministic and public-eval only; it is not a production trust root.",
        ],
    }
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote proof receipt: {OUT.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
