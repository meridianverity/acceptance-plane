# GitHub Aftercare — v1.0.2-public-eval

After `v1.0.2-public-eval` is public:

1. Confirm the GitHub release page shows the correct tag, commit, assets, and immutable status.
2. Confirm the release title exactly matches `metadata/release_pointer_lock_v1.0.2.md`.
3. Confirm the release asset list includes the ZIP and SHA256 sidecar if those assets are published.
4. Download the release ZIP and sidecar from the public release page and run archive-level verification.
5. Confirm `make qa-full` passes from a fresh clone.
6. Confirm Zenodo has archived the GitHub release if GitHub-Zenodo integration is enabled.
7. Record the GitHub release URL, release archive SHA256, and any GitHub-Zenodo archive DOI in MVG internal launch notes.
8. Do not rewrite a published immutable release. Publish a new version for changes.

Recommended public phrasing:

> The Zenodo technical note is the canonical thesis citation. The GitHub release is the runnable source/provenance and public-evaluation proof package.
