from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert proc.returncode == 0, proc.stdout
    return proc.stdout


def test_manifest_verifies():
    out = run([sys.executable, "scripts/verify_manifest.py"])
    assert "OK" in out


def test_schema_examples_validate():
    out = run([sys.executable, "tools/validate_schema_examples.py"])
    assert "PASS" in out


def test_scenario_linter_examples_are_runnable():
    for name in ["deploy_accept.json", "hold_approval_required.json", "refuse_revoked.json"]:
        out = run([sys.executable, "tools/lint_scenario_card.py", f"examples/scenario_cards/{name}"])
        assert "decision:" in out


def test_release_artifact_source_tree_verifies():
    out = run([sys.executable, "tools/verify_release_artifact.py", "--tree", "."])
    assert "PASS" in out
