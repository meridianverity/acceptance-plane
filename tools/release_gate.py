#!/usr/bin/env python3
"""Release gate for the Acceptance Plane public package."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = [
    "world #1",
    "world number one",
    "first ever in the world",
    "guaranteed compliance",
    "prevents all harmful",
    "nobel prize",
    "$10m",
    "10m+",
    "99.9",
    "99.99",
    "nobel candidate",
    "big tech",
    "history-making",
    "world-class guaranteed",
]
ALLOWLIST = {
    "docs/public-claims-style-guide.md",
    "tools/release_gate.py",
}
SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", "build", "dist-info"}


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=ROOT, text=True)
    return proc.returncode, ""


def scan_overclaims() -> list[str]:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in ALLOWLIST:
            continue
        if any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".docx", ".zip", ".pyc"}:
            continue
        try:
            text = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        for phrase in FORBIDDEN:
            if phrase in text:
                findings.append(f"{rel}: forbidden overclaim phrase {phrase!r}")
    return findings


def main() -> int:
    checks = [
        [sys.executable, "scripts/verify_manifest.py"],
        [sys.executable, "tools/run_public_eval.py"],
        [sys.executable, "tools/verify_transparency_bundle.py"],
        [sys.executable, "tools/verify_proof_receipt.py"],
        [sys.executable, "tools/independent_recompute.py"],
        [sys.executable, "tools/validate_schema_examples.py"],
    ]
    errors: list[str] = []
    assume_qa = os.environ.get("AP_RELEASE_GATE_ASSUME_QA") == "1"
    if assume_qa:
        print("release gate: assuming prior QA command checks; running claim scan only")
        checks = []
    for cmd in checks:
        print("$ " + " ".join(cmd), flush=True)
        code, out = run(cmd)
        if code != 0:
            errors.append("command failed: " + " ".join(cmd))
    findings = scan_overclaims()
    if findings:
        errors.extend(findings)
    strict_tree = os.environ.get("AP_STRICT_TREE") == "1"
    if strict_tree:
        print("$ " + " ".join([sys.executable, "tools/verify_release_artifact.py", "--tree", "."]), flush=True)
        code, out = run([sys.executable, "tools/verify_release_artifact.py", "--tree", "."])
        if code != 0:
            errors.append("strict tree verification failed")
    if errors:
        print("release gate: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("release gate: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
