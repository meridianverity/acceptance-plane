# GitHub Upload Plan — v1.0.2 Public-Eval Source/Provenance Release

## Decision

Publish this package as the official MVG organization repository:

```text
meridianverity/acceptance-plane
```

GitHub should be used as the source/provenance and public-evaluation verification layer. The canonical thesis citation remains:

```text
https://doi.org/10.5281/zenodo.20645907
```

## Release role split

- Zenodo manual technical note: canonical citation record for the v1.0.0 thesis.
- `dist/` PDF/DOCX files: historical v1.0.0 thesis assets.
- GitHub tag `v1.0.2-public-eval`: hardened source/provenance and public-evaluation proof release.
- GitHub-Zenodo archive DOI, if enabled: source/provenance DOI for the repository release.

Do not publish this hardened source archive as a new `v1.0.0` release. Use `v1.0.2-public-eval` for the runnable proof package.

## Launch sequence

1. Create the repository private.
2. Push the package using a signed commit and signed tag.
3. Run `make qa-full` and `python -m pytest -q` from a fresh clone.
4. Complete counsel/IP redline and public-claims review.
5. Make the repository public.
6. Enable release immutability.
7. Create the `v1.0.2-public-eval` release as a draft.
8. Use `metadata/github_release_body_v1.0.2-public-eval.md` as the release body.
9. Attach the release ZIP and SHA256 sidecar when available, plus core proof artifacts.
10. Publish the release after the final archive SHA matches `metadata/release_pointer_lock_v1.0.2.md`.
11. If Zenodo GitHub integration is used, wait for the source/provenance archive DOI and record it internally.
12. Link the GitHub release and canonical thesis DOI from MVG website/LinkedIn.

## Recommended release assets

```text
acceptance-plane-v1_0_2-public-eval-hardened.zip
acceptance-plane-v1_0_2-public-eval-hardened.zip.sha256.txt
provenance/MANIFEST.sha256
provenance/FILE_TREE.txt
provenance/QA_REPORT.md
receipts/acceptance-plane-proof-receipt.json
receipts/public_eval_results.json
receipts/transparency-bundle.json
vectors/public_eval_vectors.jsonl
metadata/github_release_body_v1.0.2-public-eval.md
metadata/release_pointer_lock_v1.0.2.md
figures/acceptance-plane-stack.png
figures/acceptance-plane-workflow.png
```

The v1.0.0 PDF/DOCX assets may remain in the repository as historical context, but the public release tag for this archive should be `v1.0.2-public-eval`.

## Do not do

- Do not publish before counsel/IP redline.
- Do not call the GitHub repo a product implementation.
- Do not use prize, investment-size, ranking, or guarantee language.
- Do not put private API schemas, evidence object models, production enforcement pipelines, partner-specific architectures, licensing claim charts, or commercial rights analysis in the repository.
- Do not rewrite a published immutable release. Publish a new version if needed.

## Public positioning

Use this sentence:

> MVG is publishing a fresh-archive-verifiable public-evaluation proof overlay for the Acceptance Plane architecture thesis: action acceptance before impact.

Avoid:

- formal standard;
- compliance guarantee;
- product-ready implementation;
- patent-license language;
- private commercial or partner-specific positioning.
