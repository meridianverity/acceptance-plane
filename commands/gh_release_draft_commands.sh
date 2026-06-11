#!/usr/bin/env bash
set -euo pipefail

# Requires GitHub CLI authenticated with permissions for the MVG repository.
# Run after the repository is public, Zenodo integration is enabled, and release immutability is enabled.

GITHUB_OWNER="${GITHUB_OWNER:-meridian-verity-group}"
GITHUB_REPO="${GITHUB_REPO:-acceptance-plane}"
REPO="${GITHUB_OWNER}/${GITHUB_REPO}"

python scripts/verify_manifest.py

gh release create v1.0.0 \
  --repo "${REPO}" \
  --title "v1.0.0 — The Acceptance Plane: Public Architecture Thesis" \
  --notes-file metadata/github_release_body_v1.0.0.md \
  --draft \
  --latest \
  dist/MVG_The_Acceptance_Plane_v1.0.0.pdf \
  dist/MVG_Acceptance_Plane_One_Workflow_v1.0.0.pdf \
  figures/acceptance-plane-stack.png \
  figures/acceptance-plane-workflow.png \
  provenance/MANIFEST.sha256

echo "Draft release created. Review assets and notes in GitHub UI, then publish the draft release."
