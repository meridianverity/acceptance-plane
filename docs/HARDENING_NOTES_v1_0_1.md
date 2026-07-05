# Acceptance Plane Hardening Notes v1.0.1-public-eval

This overlay turns the v1.0.0 public architecture package into a fresh-archive-verifiable public-evaluation artifact.

It does not change the canonical v1.0.0 Zenodo thesis. It adds a bounded, runnable proof layer that reviewers can execute locally.

## Fixed release-integrity defects

- Restored missing repository hygiene files that were listed in the manifest but absent from the ZIP:
  - `.github/ISSUE_TEMPLATE/config.yml`
  - `.github/workflows/verify-manifest.yml`
  - `.gitignore`
  - `.zenodo.json`
- Regenerated `provenance/MANIFEST.sha256` from the final tree.
- Regenerated `provenance/FILE_TREE.txt` from the final tree.
- Hardened `scripts/verify_manifest.py` with strict mode and build-artifact ignores.

## Added proof artifacts

- `vectors/public_eval_vectors.jsonl` contains 64 deterministic ACCEPT/HOLD/REFUSE scenario vectors.
- `tools/run_public_eval.py` evaluates the vector suite and writes deterministic public-eval results.
- `receipts/public_eval_results.json` stores the generated result digest and per-vector receipt digests.
- `receipts/transparency-bundle.json` binds vector results into a signed Merkle tree head.
- `receipts/acceptance-plane-proof-receipt.json` binds the eval result digest and transparency root into an Ed25519-signed receipt.
- `tools/independent_recompute.py` recomputes the proof chain without importing the evaluator package.

## Added reviewer workflow

```bash
python scripts/verify_manifest.py
python tools/run_public_eval.py
python tools/verify_transparency_bundle.py
python tools/verify_proof_receipt.py --verify-manifest
python tools/independent_recompute.py
python tools/release_gate.py
```

The same checks are available through:

```bash
make qa-full
python -m pytest -q
```

## Claims boundary

This overlay is a public-evaluation proof pack. It is not a formal standard, product implementation, legal opinion, compliance certification, patent claim chart, or patent license.
