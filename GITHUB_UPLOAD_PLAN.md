# GitHub Upload Plan — 99.9+ Provenance Path

## Decision

Publish this package as the official MVG organization repository:

```text
meridian-verity-group/acceptance-plane
```

GitHub should be used as the source/provenance layer, not as the primary citation layer. The canonical citation remains:

```text
https://doi.org/10.5281/zenodo.20645907
```

## Repository role

- Zenodo manual technical note: canonical citation record.
- GitHub repository: public source/provenance home.
- GitHub release `v1.0.0`: locked historical release package.
- GitHub-Zenodo archive DOI: source/provenance DOI for the repository release.

## Launch sequence

1. Create the repository private.
2. Push the package using a signed commit and signed tag.
3. Run manifest verification.
4. Complete counsel/IP redline.
5. Make the repository public.
6. Enable Zenodo GitHub integration for the public repository.
7. Enable release immutability.
8. Create the v1.0.0 release as a draft.
9. Attach final release assets.
10. Publish the release.
11. Wait for the Zenodo GitHub archive DOI.
12. Link the GitHub release and canonical DOI from MVG website/LinkedIn.

## Release assets

Attach these to the GitHub release draft:

```text
dist/MVG_The_Acceptance_Plane_v1.0.0.pdf
dist/MVG_Acceptance_Plane_One_Workflow_v1.0.0.pdf
figures/acceptance-plane-stack.png
figures/acceptance-plane-workflow.png
provenance/MANIFEST.sha256
```

## Do not do

- Do not publish before counsel/IP redline.
- Do not call the GitHub repo a product implementation.
- Do not put API schemas, evidence object models, crypto binding methods, enforcement pipelines, hardware claim maps, or partner-specific architectures in the repository.
- Do not rewrite the v1.0.0 release after publication. Publish a new version if needed.

## Public positioning

Use this sentence:

> MVG is publishing the canonical public architecture thesis for the Acceptance Plane in agentic AI infrastructure.

Avoid:

- first ever;
- patent priority;
- formal standard;
- compliance guarantee;
- product-ready implementation.
