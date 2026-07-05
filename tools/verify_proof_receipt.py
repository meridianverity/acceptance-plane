#!/usr/bin/env python3
"""Verify the Acceptance Plane proof receipt.

Receipt self-check and release-archive binding are deliberately separate.  Use
--release-zip plus --sha256-file when verifying a published archive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from acceptance_plane_eval.canonical import canonical_json, digest_json
from acceptance_plane_eval.crypto_profile import verify

RECEIPT = ROOT / "receipts" / "acceptance-plane-proof-receipt.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sidecar(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("empty sha256 sidecar")
    return text.split()[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-manifest", action="store_true")
    ap.add_argument("--release-zip", type=Path)
    ap.add_argument("--sha256-file", type=Path)
    args = ap.parse_args()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    errors: list[str] = []
    core = receipt["receipt_core"]
    if digest_json(core) != receipt["receipt_core_digest"]:
        errors.append("receipt core digest mismatch")
    try:
        verify(canonical_json(core), receipt["receipt_core_signature_base64"], core["public_eval_key"]["public_key_base64"])
    except Exception as exc:
        errors.append(f"receipt signature failed: {exc}")
    if core["public_eval"]["failed"] != 0:
        errors.append("public eval contains failures")
    if args.verify_manifest:
        proc = subprocess.run([sys.executable, "scripts/verify_manifest.py"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            errors.append("manifest verification failed:\n" + proc.stdout)
    if args.release_zip or args.sha256_file:
        if not args.release_zip or not args.sha256_file:
            errors.append("archive verification requires both --release-zip and --sha256-file")
        else:
            got = sha256_file(args.release_zip)
            expected = parse_sidecar(args.sha256_file)
            if got != expected:
                errors.append(f"release archive sha256 mismatch: got {got} expected {expected}")
    if errors:
        print("HALT: Acceptance Plane proof receipt: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Acceptance Plane proof receipt: PASS")
    print("Receipt self-check: OK")
    if args.verify_manifest:
        print("Manifest verification: OK")
    if args.release_zip and args.sha256_file:
        print("Release archive verification: OK")
    else:
        print("Release archive verification: not requested; use --release-zip plus --sha256-file for archive binding")
    print(f"Public evaluation: {core['public_eval']['passed']} / {core['public_eval']['vector_count']} PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
