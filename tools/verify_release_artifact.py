#!/usr/bin/env python3
"""Verify a release ZIP against its in-archive manifest and optional sidecar."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE_SUFFIXES = {".pyc", ".pyo"}
IGNORE_DIRS = {".git", ".pytest_cache", "__pycache__", "build"}
IGNORE_NAMES = {"provenance/MANIFEST.sha256"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sidecar(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    return text.split()[0]


def should_ignore(rel: str) -> bool:
    p = Path(rel)
    if rel in IGNORE_NAMES:
        return True
    if p.suffix in IGNORE_SUFFIXES:
        return True
    if any(part in IGNORE_DIRS or part.endswith(".egg-info") for part in p.parts):
        return True
    return False


def verify_tree(tree: Path) -> list[str]:
    errors: list[str] = []
    manifest = tree / "provenance" / "MANIFEST.sha256"
    if not manifest.exists():
        return ["missing provenance/MANIFEST.sha256"]
    entries = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, rel = line.split("  ", 1)
            entries[rel] = digest
    for rel, expected in entries.items():
        path = tree / rel
        if not path.exists():
            errors.append(f"MISSING {rel}")
        elif sha256_file(path) != expected:
            errors.append(f"MISMATCH {rel}")
    actual = {p.relative_to(tree).as_posix() for p in tree.rglob("*") if p.is_file() and not should_ignore(p.relative_to(tree).as_posix())}
    extra = sorted(actual - set(entries))
    missing = sorted(set(entries) - actual)
    for rel in extra:
        errors.append(f"EXTRA {rel}")
    for rel in missing:
        errors.append(f"MISSING-FROM-TREE {rel}")
    return errors


def verify_zip(zip_path: Path, sha256_file_path: Path | None) -> list[str]:
    errors: list[str] = []
    if sha256_file_path:
        expected = parse_sidecar(sha256_file_path)
        got = sha256_file(zip_path)
        if got != expected:
            errors.append(f"archive sha256 mismatch: got {got} expected {expected}")
    try:
        with zipfile.ZipFile(zip_path) as zf:
            bad = zf.testzip()
            if bad:
                errors.append(f"zip CRC failed at {bad}")
            names = [n for n in zf.namelist() if not n.endswith("/")]
            roots = {n.split("/", 1)[0] for n in names}
            if len(roots) != 1:
                errors.append(f"archive must have one top-level root, found {sorted(roots)}")
                return errors
            root = next(iter(roots))
            manifest_name = f"{root}/provenance/MANIFEST.sha256"
            if manifest_name not in names:
                errors.append("missing in-archive provenance/MANIFEST.sha256")
                return errors
            manifest_text = zf.read(manifest_name).decode("utf-8")
            entries = {}
            for line in manifest_text.splitlines():
                if line.strip():
                    digest, rel = line.split("  ", 1)
                    entries[rel] = digest
            archive_rels = {n.split("/", 1)[1] for n in names if "/" in n and not should_ignore(n.split("/", 1)[1])}
            for rel, expected in entries.items():
                member = f"{root}/{rel}"
                if member not in names:
                    errors.append(f"MISSING {rel}")
                else:
                    got = sha256_bytes(zf.read(member))
                    if got != expected:
                        errors.append(f"MISMATCH {rel}")
            for rel in sorted(archive_rels - set(entries)):
                errors.append(f"EXTRA {rel}")
            for rel in sorted(set(entries) - archive_rels):
                errors.append(f"MISSING-FROM-ARCHIVE {rel}")
    except zipfile.BadZipFile as exc:
        errors.append(f"bad zip: {exc}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("zip", nargs="?", type=Path)
    ap.add_argument("--sha256-file", type=Path)
    ap.add_argument("--tree", type=Path, help="verify a source tree instead of/in addition to a zip")
    args = ap.parse_args()
    errors: list[str] = []
    if args.tree:
        tree = (ROOT / args.tree).resolve() if not args.tree.is_absolute() else args.tree
        errors.extend(verify_tree(tree))
    if args.zip:
        errors.extend(verify_zip(args.zip, args.sha256_file))
    if not args.tree and not args.zip:
        errors.append("provide a zip path or --tree")
    if errors:
        print("release artifact verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("release artifact verification: PASS")
    if args.tree:
        print("source tree: OK")
    if args.zip:
        print("archive manifest: OK")
        if args.sha256_file:
            print("archive sha256 sidecar: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
