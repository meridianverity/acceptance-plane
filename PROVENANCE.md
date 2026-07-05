# Provenance

Package: MVG Acceptance Plane Public Canonical Package  
Canonical thesis version: v1.0.0  
Public-eval overlay: v1.0.2-public-eval  
Release date: 2026-06-11  
Organization: Meridian Verity Group  
Author: Scott Lee  
Canonical DOI: https://doi.org/10.5281/zenodo.20645907

## Canonical Record

The canonical citation is the Zenodo manual technical report record created by Meridian Verity Group for the v1.0.0 thesis package.

Recommended citation:

> Lee, Scott. Meridian Verity Group. (2026). The Acceptance Plane: The Missing Trust Layer for Agentic AI Infrastructure (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.20645907

## Public-Eval Overlay

The v1.0.2-public-eval overlay adds bounded, runnable proof artifacts and release-facing pointer locks:

- `vectors/public_eval_vectors.jsonl`
- `receipts/public_eval_results.json`
- `receipts/transparency-bundle.json`
- `receipts/acceptance-plane-proof-receipt.json`
- `tools/independent_recompute.py`
- `tools/verify_release_artifact.py`
- `metadata/release_pointer_lock_v1.0.2.md`
- `metadata/github_release_body_v1.0.2-public-eval.md`

These files support review and provenance. They do not replace the canonical DOI or create a product specification.

## GitHub Repository

https://github.com/meridianverity/acceptance-plane

## GitHub Release Provenance

The GitHub release tag, commit hash, SHA256 manifest, immutable release status, and Zenodo GitHub release archive DOI should be used as source/provenance signals once the release is published.

The GitHub-Zenodo release archive DOI should not replace the canonical Zenodo manual technical report DOI above.

## Integrity

See `provenance/MANIFEST.sha256` for SHA256 hashes of package files. The manifest intentionally excludes itself to avoid self-referential hashing.
