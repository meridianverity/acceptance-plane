#!/usr/bin/env python3
"""Verify provenance/MANIFEST.sha256 for the Acceptance Plane package."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "provenance" / "MANIFEST.sha256"
IGNORE_DIRS = {".git", ".pytest_cache", "__pycache__", "build"}
IGNORE_SUFFIXES = {".pyc", ".pyo"}
IGNORE_NAMES = {"provenance/MANIFEST.sha256"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_ignore(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in IGNORE_NAMES:
        return True
    if path.suffix in IGNORE_SUFFIXES:
        return True
    parts = path.relative_to(ROOT).parts
    if any(part in IGNORE_DIRS or part.endswith(".egg-info") for part in parts):
        return True
    return False


def read_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        entries[rel] = digest
    return entries


def current_files() -> set[str]:
    return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and not should_ignore(p)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="also reject files not listed in the manifest")
    args = ap.parse_args()
    errors: list[str] = []
    entries = read_manifest()
    count = 0
    for rel, expected in entries.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"MISSING {rel}")
            continue
        got = sha256(path)
        count += 1
        if got != expected:
            errors.append(f"MISMATCH {rel}")
    if args.strict:
        extra = sorted(current_files() - set(entries))
        for rel in extra:
            errors.append(f"EXTRA {rel}")
    if errors:
        print("Manifest verification FAILED")
        for error in errors:
            print(error)
        return 1
    print(f"Manifest verification OK: {count} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
