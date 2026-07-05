# Acceptance Plane Hardening Notes v1.0.2-public-eval

This polish overlay makes the v1.0.1 public-eval proof package release-facing and archive-ready.

## Fixed release-facing defects

- Restored missing dotfiles that were referenced by the manifest but absent from the submitted ZIP:
  - `.github/ISSUE_TEMPLATE/config.yml`
  - `.github/workflows/verify-manifest.yml`
  - `.gitignore`
  - `.zenodo.json`
- Replaced v1.0.0-centered GitHub launch commands with a `v1.0.2-public-eval` release flow.
- Added exact release title, release body, public release copy, and pointer-lock metadata.
- Updated package, SBOM, release attestation, proof receipt, QA report, and manifest metadata to v1.0.2-public-eval.
- Clarified that v1.0.0 PDF/DOCX files are historical thesis assets, while v1.0.2-public-eval is the hardened runnable proof release.
- Rewrote the Permit Receipt / HaltSeal relationship note as a public-safe boundary note rather than a private strategy note.

## Verification posture

The release should be judged by fresh-verification properties:

```text
Manifest verification OK
Acceptance Plane public eval: 64 / 64 PASS
transparency bundle: PASS
Acceptance Plane proof receipt: PASS
independent recomputation: 13 / 13 PASS
schema example validation: PASS
release gate: PASS
release artifact verification: PASS
pytest: PASS
editable install: PASS
```

## Claims boundary

The package is intentionally strong but bounded. It should not use prize, ranking, valuation, guarantee, standardization, certification, or production-deployment claims. The release is a public architecture thesis and bounded public-evaluation proof overlay.
