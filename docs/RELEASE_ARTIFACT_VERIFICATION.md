# Release Artifact Verification

The hardened package includes source-tree and archive-level verification.

## Source tree

```bash
python scripts/verify_manifest.py
python tools/verify_release_artifact.py --tree .
```

## Release ZIP

After publishing a ZIP and SHA-256 sidecar:

```bash
python tools/verify_release_artifact.py acceptance-plane-v1_0_1-hardened.zip \
  --sha256-file acceptance-plane-v1_0_1-hardened.zip.sha256.txt

python tools/verify_proof_receipt.py \
  --verify-manifest \
  --release-zip acceptance-plane-v1_0_1-hardened.zip \
  --sha256-file acceptance-plane-v1_0_1-hardened.zip.sha256.txt
```

The proof receipt intentionally does not claim archive verification unless the archive and sidecar are supplied.
