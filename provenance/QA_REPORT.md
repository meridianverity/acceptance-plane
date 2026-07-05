# QA Report - MVG Acceptance Plane Public Package v1.0.1-public-eval

## Hardened public-eval checks

- Manifest/source-tree drift fixed.
- Missing `.github`, `.gitignore`, and `.zenodo.json` files restored.
- `scripts/verify_manifest.py` hardened with strict mode.
- `pyproject.toml` and `Makefile` added.
- 64-vector ACCEPT/HOLD/REFUSE public-eval suite generated.
- Scenario-card linter added and exercised against three example cards.
- Ed25519 public-eval proof receipt generated and verified.
- Merkle transparency bundle generated and verified.
- Independent recomputation script added.
- Source/archive verifier added.
- pytest suite added.

## Local verification commands

```text
python scripts/verify_manifest.py
python tools/run_public_eval.py
python tools/verify_transparency_bundle.py
python tools/verify_proof_receipt.py --verify-manifest
python tools/independent_recompute.py
python tools/validate_schema_examples.py
python -m pytest -q
python tools/release_gate.py
python tools/verify_release_artifact.py --tree .
```

## Publication note

This package remains suitable as a public architecture and provenance package after MVG completes counsel/IP review and final publisher-side checks.

The v1.0.1-public-eval overlay is not a formal standard, product implementation, legal opinion, compliance certification, patent claim chart, or patent license.
