# Release Pointer Lock v1.0.2-public-eval

Use these exact public-facing labels for the hardened source/provenance release.

```text
Tag: v1.0.2-public-eval
Release title: Acceptance Plane v1.0.2-public-eval — Verifiable Action Acceptance Before Impact
Canonical thesis DOI: https://doi.org/10.5281/zenodo.20645907
Archive role: source/provenance and bounded public-evaluation proof overlay
Recommended ZIP asset: acceptance-plane-v1_0_2-public-eval-hardened.zip
Recommended SHA256 sidecar: acceptance-plane-v1_0_2-public-eval-hardened.zip.sha256.txt
Release body: metadata/github_release_body_v1.0.2-public-eval.md
```

## Publication rule

Do not publish this hardened archive under a v1.0.0 tag. The v1.0.0 PDF/DOCX files in `dist/` are historical thesis assets. The source/provenance proof release target is `v1.0.2-public-eval`.

## Required verification before publish

```bash
python -m pip install -e . --no-deps
python -m pip install cryptography pytest
make qa-full
python -m pytest -q
python tools/verify_release_artifact.py --tree .
```

If releasing a ZIP asset, also verify:

```bash
python tools/verify_release_artifact.py acceptance-plane-v1_0_2-public-eval-hardened.zip   --sha256-file acceptance-plane-v1_0_2-public-eval-hardened.zip.sha256.txt
python tools/verify_proof_receipt.py --verify-manifest   --release-zip acceptance-plane-v1_0_2-public-eval-hardened.zip   --sha256-file acceptance-plane-v1_0_2-public-eval-hardened.zip.sha256.txt
```

## Public claim boundary

Use strong but bounded proof language. Do not describe the release as a formal standard, production implementation, certification, patent license, claim chart, deployment guarantee, or legal opinion.
