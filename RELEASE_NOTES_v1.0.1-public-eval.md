# Release Notes - v1.0.1-public-eval

This release adds a hardened public-evaluation proof overlay to the Acceptance Plane public architecture package.

Canonical DOI: https://doi.org/10.5281/zenodo.20645907

## Included

- 64 deterministic ACCEPT/HOLD/REFUSE scenario vectors.
- Runnable scenario-card linter.
- Deterministic receipt-core digests for each vector.
- Signed Merkle transparency bundle.
- Signed public-eval proof receipt.
- Independent recomputation script.
- Source/archive release artifact verifier.
- Makefile and pytest QA path.
- Shape-only OPA, Envoy, and Kubernetes adapter sketches.

## Status

This is a public-evaluation and provenance overlay. It does not change the canonical v1.0.0 thesis DOI and is not a formal standard, product implementation, legal opinion, compliance certification, patent claim chart, or patent license.

## Verification

```bash
make qa-full
python -m pytest -q
```

Expected headline:

```text
Acceptance Plane public eval: 64 / 64 PASS
independent recomputation: 13 / 13 PASS
release gate: PASS
```
