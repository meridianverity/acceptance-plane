# GitHub Publication Sequence — v1.0.2-public-eval

## Objective

Use GitHub as the public source/provenance and public-evaluation verification repository for the Acceptance Plane thesis, while Zenodo remains the canonical citation record.

## Recommended sequence

1. Create `meridianverity/acceptance-plane` as a private repository.
2. Push this package to `main` using a signed commit.
3. Run `make qa-full` and `python -m pytest -q` from a fresh clone.
4. Complete counsel/IP redline and public-claims review.
5. Make the repository public.
6. Enable release immutability before publishing the release.
7. Create a draft release for tag `v1.0.2-public-eval`.
8. Use `metadata/github_release_body_v1.0.2-public-eval.md` as the release notes.
9. Attach the assets listed in `metadata/release_pointer_lock_v1.0.2.md` and `GITHUB_UPLOAD_PLAN.md`.
10. Publish the release after verifying the ZIP SHA256 sidecar.
11. If Zenodo GitHub archiving is enabled, wait for the source/provenance archive DOI.
12. Add the canonical thesis DOI and GitHub release URL to the MVG website and LinkedIn post.

## Why this order

- The canonical thesis DOI remains stable and citable.
- The GitHub release provides the runnable proof package and archive-level verification.
- Immutable releases, signed commits, signed tags, manifest verification, and SHA256 sidecars strengthen provenance.
- Publishing as `v1.0.2-public-eval` avoids confusion with historical v1.0.0 thesis assets.
