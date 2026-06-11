# GitHub Publication Sequence

## Objective

Use GitHub as the public source/provenance repository for the Acceptance Plane thesis, while Zenodo remains the canonical citation record.

## Recommended sequence

1. Create `meridian-verity-group/acceptance-plane` as a private repository.
2. Push this package to `main` using a signed commit.
3. Run `python scripts/verify_manifest.py` locally and confirm the GitHub Action passes.
4. Complete counsel/IP redline.
5. Make the repository public.
6. Enable Zenodo GitHub integration for the public repository.
7. Enable GitHub release immutability before publishing the release.
8. Create a draft release for tag `v1.0.0`.
9. Attach the release assets listed in `metadata/github_release_body_v1.0.0.md`.
10. Publish the release.
11. Wait for Zenodo to archive the GitHub release and issue the source/provenance DOI.
12. Add the canonical Zenodo DOI and GitHub release URL to the MVG website and LinkedIn post.

## Why this order

- Zenodo can only access public repositories for GitHub archiving.
- Zenodo issues a new DOI each time a GitHub release is created.
- GitHub immutable releases protect release assets and the associated tag after publication.
- Signed commits and signed tags help establish provenance for the repository history.
