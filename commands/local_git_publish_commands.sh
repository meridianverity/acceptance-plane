#!/usr/bin/env bash
set -euo pipefail

# Recommended defaults. Change only if the MVG GitHub organization handle differs.
GITHUB_OWNER="${GITHUB_OWNER:-meridianverity}"
GITHUB_REPO="${GITHUB_REPO:-acceptance-plane}"
REMOTE_URL="git@github.com:${GITHUB_OWNER}/${GITHUB_REPO}.git"
TAG="${AP_RELEASE_TAG:-v1.0.2-public-eval}"

# Run from repository root.
python scripts/verify_manifest.py
python tools/run_public_eval.py
python tools/verify_transparency_bundle.py
python tools/verify_proof_receipt.py --verify-manifest
python tools/independent_recompute.py
python tools/verify_release_artifact.py --tree .

git init -b main

git config commit.gpgsign true || true
git config tag.gpgsign true || true

git add .
git commit -S -m "Release Acceptance Plane public-eval proof overlay v1.0.2"
git tag -s "${TAG}" -m "Acceptance Plane v1.0.2-public-eval"

git remote add origin "${REMOTE_URL}"
git push -u origin main --follow-tags

echo "Pushed signed ${TAG} source/provenance package to ${REMOTE_URL}"
