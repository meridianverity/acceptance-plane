#!/usr/bin/env python3
"""Verify provenance/MANIFEST.sha256 for the MVG Acceptance Plane package."""
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parents[1]
manifest = root / "provenance" / "MANIFEST.sha256"
errors = []
count = 0
for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    digest, rel = line.split("  ", 1)
    path = root / rel
    if not path.exists():
        errors.append(f"MISSING {rel}")
        continue
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    count += 1
    if got != digest:
        errors.append(f"MISMATCH {rel}")
if errors:
    print("Manifest verification FAILED")
    for e in errors:
        print(e)
    sys.exit(1)
print(f"Manifest verification OK: {count} files")
