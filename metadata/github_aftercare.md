# GitHub Aftercare

After v1.0.0 is public:

1. Confirm the GitHub release page shows the correct tag, commit, assets, and immutable status.
2. Confirm the release asset list matches `metadata/github_release_body_v1.0.0.md`.
3. Confirm `scripts/verify_manifest.py` passes from a fresh clone.
4. Confirm Zenodo has archived the GitHub release and issued a GitHub release archive DOI.
5. Record the GitHub release URL and GitHub-Zenodo archive DOI in MVG's internal launch notes.
6. Do not rewrite v1.0.0 files just to add the GitHub archive DOI. Preserve v1.0.0 as the historical release. Add cross-links on the website, LinkedIn, or a future v1.0.1/v1.1.0 if needed.
7. Pin the repository on the MVG GitHub organization profile if GitHub organization profile curation is being used.

Recommended public phrasing:

> The Zenodo technical note is the canonical citation record. The GitHub release is the source/provenance package for the same public architecture thesis.
