# Acceptance Plane v1.0.1-public-eval

This release adds a hardened public-evaluation proof overlay to the v1.0.0 Acceptance Plane public architecture thesis.

Canonical DOI remains: https://doi.org/10.5281/zenodo.20645907

## Verify locally

```bash
python -m pip install -e . --no-deps
python -m pip install cryptography pytest
make qa-full
```

Expected headline:

```text
Acceptance Plane public eval: 64 / 64 PASS
independent recomputation: 13 / 13 PASS
release gate: PASS
```

## Added

- deterministic scenario-card linter;
- 64 public-eval vectors;
- Ed25519-signed public-eval proof receipt;
- signed Merkle transparency bundle;
- independent recomputation;
- source/archive release verification;
- OPA, Envoy, and Kubernetes adapter-shape sketches.

## Scope

Public-evaluation and provenance overlay only. Not a formal standard, product implementation, legal opinion, compliance certification, patent claim chart, or patent license.

## Superseded for public GitHub release polish

For the final public source/provenance release flow, use `metadata/github_release_body_v1.0.2-public-eval.md` and tag `v1.0.2-public-eval`.
