# Publication Readiness Checklist

This replaces the earlier pre-publication TODO file. It is intended as a final go/no-go checklist, not a sign that the package is unfinished.

## GO criteria

- Counsel/IP redline complete.
- License confirmed.
- Canonical DOI embedded in public-facing citation points: https://doi.org/10.5281/zenodo.20645907.
- PDFs, DOCX files, metadata, and manifest regenerated after DOI insertion.
- DOCX/PDF metadata show Scott Lee and Meridian Verity Group.
- Figures render without clipping.
- Manifest verifies.
- GitHub repository settings are correct.
- Zenodo manual record metadata is ready.
- MVG website and LinkedIn canonical links are prepared.

## Canonical DOI rule

Use the manual Zenodo technical report DOI as the canonical citation: https://doi.org/10.5281/zenodo.20645907.

Do not replace the canonical DOI with a GitHub-Zenodo release archive DOI. Treat the GitHub archive DOI as source/provenance.

## DOI-embedded workflow

For v1.0.0, the DOI has been inserted. Before public release, confirm:

1. DOCX/PDF assets have been regenerated after DOI insertion.
2. `provenance/MANIFEST.sha256` has been recalculated.
3. The ZIP has been recreated from the final file tree.
4. The manifest verifies successfully.
5. Publisher-side DOI and license fields match the package metadata.
