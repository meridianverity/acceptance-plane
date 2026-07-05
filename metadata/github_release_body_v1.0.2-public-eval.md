# Acceptance Plane v1.0.2-public-eval — Verifiable Action Acceptance Before Impact

This release is the hardened public-evaluation source/provenance package for the Acceptance Plane architecture thesis.

The package is designed for one reviewer question:

> Can a fresh clone or fresh archive independently verify that the Acceptance Plane public-eval proof chain is complete, bounded, and reproducible?

For this release, the answer is intended to be yes.

Canonical thesis DOI: https://doi.org/10.5281/zenodo.20645907

## What this release demonstrates

The Acceptance Plane names the architectural function that decides whether a specific autonomous AI action should be accepted by a protected system before impact.

This release turns that concept into a bounded, runnable public-eval proof artifact:

- 64 deterministic ACCEPT / HOLD / REFUSE scenario vectors;
- deterministic receipt digests for evaluated action/evidence/policy envelopes;
- Ed25519-signed public-eval proof receipt;
- signed Merkle transparency bundle over the public-eval results;
- independent recomputation script that does not import the evaluator package;
- source-tree and ZIP-archive release verification;
- scenario-card linter and schema examples;
- shape-only OPA, Envoy, and Kubernetes adapter examples.

## Verify locally

```bash
python -m pip install -e . --no-deps
python -m pip install cryptography pytest
make qa-full
python -m pytest -q
```

Expected headline:

```text
Manifest verification OK
Acceptance Plane public eval: 64 / 64 PASS
transparency bundle: PASS
Acceptance Plane proof receipt: PASS
independent recomputation: 13 / 13 PASS
release gate: PASS
release artifact verification: PASS
```

Archive-level verification, when the release ZIP and SHA256 sidecar are available:

```bash
python tools/verify_release_artifact.py   acceptance-plane-v1_0_2-public-eval-hardened.zip   --sha256-file acceptance-plane-v1_0_2-public-eval-hardened.zip.sha256.txt

python tools/verify_proof_receipt.py   --verify-manifest   --release-zip acceptance-plane-v1_0_2-public-eval-hardened.zip   --sha256-file acceptance-plane-v1_0_2-public-eval-hardened.zip.sha256.txt
```

## Release precision

This release supersedes the v1.0.1 public-eval overlay for GitHub/public-source publishing. The original v1.0.0 PDF/DOCX assets remain historical thesis artifacts under `dist/`; they are not the target release tag for this hardened source archive.

Use these labels consistently:

```text
Tag: v1.0.2-public-eval
Release title: Acceptance Plane v1.0.2-public-eval — Verifiable Action Acceptance Before Impact
Archive role: source/provenance and bounded public-evaluation proof overlay
Canonical thesis DOI: https://doi.org/10.5281/zenodo.20645907
```

## Scope boundary

This is a public architecture thesis and bounded public-evaluation proof package. It is not a formal standard, product implementation, legal opinion, compliance certification, patent claim chart, patent license, production trust root, deployment guarantee, or complete security solution.

Recommended one-line description:

> Fresh-archive-verifiable public-eval proof overlay for action acceptance before impact: 64 deterministic vectors, signed proof receipt, signed transparency bundle, independent recomputation, and release artifact verification.
