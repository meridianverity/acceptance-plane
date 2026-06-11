#!/usr/bin/env bash
set -euo pipefail

# Recommended defaults. Change only if the MVG GitHub organization handle differs.
GITHUB_OWNER="${GITHUB_OWNER:-meridian-verity-group}"
GITHUB_REPO="${GITHUB_REPO:-acceptance-plane}"
REMOTE_URL="git@github.com:${GITHUB_OWNER}/${GITHUB_REPO}.git"

# Run from repository root.
python scripts/verify_manifest.py

git init -b main

git config commit.gpgsign true || true
git config tag.gpgsign true || true

git add .
git commit -S -m "Release Acceptance Plane public architecture thesis v1.0.0"
git tag -s v1.0.0 -m "The Acceptance Plane v1.0.0"

git remote add origin "${REMOTE_URL}"
git push -u origin main --follow-tags

echo "Pushed signed v1.0.0 source/provenance package to ${REMOTE_URL}"
