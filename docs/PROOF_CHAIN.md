# Acceptance Plane Proof Chain

The hardened package contains a three-layer proof chain.

## 1. Scenario vectors

`vectors/public_eval_vectors.jsonl` contains 64 deterministic scenario cards. Each vector declares the expected decision and reason code.

Run:

```bash
python tools/run_public_eval.py --write-results receipts/public_eval_results.json
```

Expected result:

```text
Acceptance Plane public eval: 64 / 64 PASS
```

## 2. Transparency bundle

`receipts/transparency-bundle.json` places the vector results into a Merkle tree and signs the tree head with a deterministic public-eval Ed25519 key.

Run:

```bash
python tools/verify_transparency_bundle.py
```

Expected result:

```text
transparency bundle: PASS
```

## 3. Proof receipt

`receipts/acceptance-plane-proof-receipt.json` binds the public-eval digest and transparency root into a signed proof receipt.

Run:

```bash
python tools/verify_proof_receipt.py --verify-manifest
```

Expected result:

```text
Acceptance Plane proof receipt: PASS
```

The signing key is deterministic and public-eval only. It is not a production trust root.
