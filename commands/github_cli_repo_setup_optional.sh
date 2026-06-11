#!/usr/bin/env bash
set -euo pipefail

# Optional helper. Many teams should create/configure the repository manually in GitHub UI.
# Requires GitHub CLI authenticated with organization permissions.

GITHUB_OWNER="${GITHUB_OWNER:-meridian-verity-group}"
GITHUB_REPO="${GITHUB_REPO:-acceptance-plane}"
REPO="${GITHUB_OWNER}/${GITHUB_REPO}"

# Create private first. Make public only after counsel/IP redline and final launch approval.
gh repo create "${REPO}" \
  --private \
  --description "Public architecture thesis and reference workflow for the Acceptance Plane in agentic AI infrastructure." \
  --homepage "https://doi.org/10.5281/zenodo.20645907" \
  --disable-issues \
  --disable-wiki

# Topics may also be set in the GitHub UI.
gh repo edit "${REPO}" \
  --add-topic acceptance-plane \
  --add-topic agentic-ai \
  --add-topic ai-agents \
  --add-topic ai-infrastructure \
  --add-topic autonomous-agents \
  --add-topic ai-trust \
  --add-topic zero-trust \
  --add-topic confidential-computing \
  --add-topic remote-attestation \
  --add-topic cybersecurity \
  --add-topic enterprise-ai \
  --add-topic devsecops || true

echo "Created ${REPO} as a private repository."
