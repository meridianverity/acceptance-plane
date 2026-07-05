from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from acceptance_plane_eval.canonical import canonical_json, digest_json
from acceptance_plane_eval.crypto_profile import verify
from acceptance_plane_eval.transparency import merkle_root, verify_inclusion

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert proc.returncode == 0, proc.stdout
    return proc.stdout


def test_transparency_bundle_verifier():
    out = run([sys.executable, "tools/verify_transparency_bundle.py"])
    assert "PASS" in out


def test_proof_receipt_verifier():
    out = run([sys.executable, "tools/verify_proof_receipt.py"])
    assert "Acceptance Plane proof receipt: PASS" in out


def test_independent_recomputation():
    out = run([sys.executable, "tools/independent_recompute.py"])
    assert "PASS" in out


def test_receipt_signature_binds_core():
    receipt = json.loads((ROOT / "receipts" / "acceptance-plane-proof-receipt.json").read_text(encoding="utf-8"))
    core = receipt["receipt_core"]
    assert digest_json(core) == receipt["receipt_core_digest"]
    assert verify(canonical_json(core), receipt["receipt_core_signature_base64"], core["public_eval_key"]["public_key_base64"])


def test_selected_inclusion_proofs_bind_to_root():
    bundle = json.loads((ROOT / "receipts" / "transparency-bundle.json").read_text(encoding="utf-8"))
    leaves = [item["leaf_hash"] for item in bundle["leaves"]]
    root = merkle_root(leaves)
    assert root == bundle["tree_head"]["root_hash"]
    for proof in bundle["selected_inclusion_proofs"]:
        assert verify_inclusion(proof["leaf_hash"], proof["index"], proof["proof"], root)
