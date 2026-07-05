#!/usr/bin/env bash
set -euo pipefail

# Requires GitHub CLI authenticated with permissions for the MVG repository.
# Run after the repository is public, release immutability is enabled, and final QA passes.

GITHUB_OWNER="${GITHUB_OWNER:-meridianverity}"
GITHUB_REPO="${GITHUB_REPO:-acceptance-plane}"
REPO="${GITHUB_OWNER}/${GITHUB_REPO}"
TAG="${AP_RELEASE_TAG:-v1.0.2-public-eval}"
TITLE="Acceptance Plane v1.0.2-public-eval — Verifiable Action Acceptance Before Impact"
NOTES="metadata/github_release_body_v1.0.2-public-eval.md"

python scripts/verify_manifest.py
python tools/run_public_eval.py
python tools/verify_transparency_bundle.py
python tools/verify_proof_receipt.py --verify-manifest
python tools/independent_recompute.py
python tools/verify_release_artifact.py --tree .

ASSETS=(
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
)

if [[ -n "${AP_RELEASE_ZIP:-}" ]]; then
  ASSETS+=("${AP_RELEASE_ZIP}")
fi
if [[ -n "${AP_RELEASE_SHA256_FILE:-}" ]]; then
  ASSETS+=("${AP_RELEASE_SHA256_FILE}")
fi

gh release create "${TAG}"   --repo "${REPO}"   --title "${TITLE}"   --notes-file "${NOTES}"   --draft   --latest   "${ASSETS[@]}"

echo "Draft release ${TAG} created. Review assets, SHA256 sidecar, and notes in GitHub UI before publishing."
