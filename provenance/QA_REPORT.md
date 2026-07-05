# QA Report - MVG Acceptance Plane Public Package v1.0.2-public-eval

## Hardened public-eval checks

- Manifest/source-tree drift fixed.
- Missing `.github`, `.gitignore`, and `.zenodo.json` files restored in the submitted ZIP tree.
- `scripts/verify_manifest.py` verifies the final manifest.
- `pyproject.toml` supports editable install.
- 64-vector ACCEPT/HOLD/REFUSE public-eval suite present and verified.
- Scenario-card linter present and exercised against three example cards.
- Ed25519 public-eval proof receipt generated and verified.
- Merkle transparency bundle generated and verified.
- Independent recomputation script verifies the proof chain without importing the evaluator package.
- Source/archive verifier verifies tree and release ZIP artifacts.
- GitHub release title/body/pointer lock updated to v1.0.2-public-eval.
- Public/private disclosure boundary documented.
- pytest suite passes.

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
python -m pip install -e . --no-deps
```

## Publication note

This package is suitable as a public architecture and provenance package after MVG completes counsel/IP review, publisher-side SHA verification, and final release page checks.

The v1.0.2-public-eval overlay is not a formal standard, product implementation, legal opinion, compliance certification, patent claim chart, patent license, production trust root, deployment guarantee, or complete security solution.
