#!/usr/bin/env python3
"""
Tests the canonical environment guard hook against simulated project structures.
Uses workspace-local fixtures directory for cross-platform and sandboxed compatibility.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "hooks"))

try:
    from environment_guard import EnvironmentGuard
except ImportError as e:
    print(f"[FAIL] Could not import EnvironmentGuard from hooks: {e}")
    sys.exit(1)


def test_hooks() -> int:
    print("[Test] Validating Environment Guard Hook Logic (hooks/environment_guard.py)...")
    errors = []

    fixtures_dir = ROOT_DIR / "tests" / "fixtures" / "_hook_test_scratch"
    if fixtures_dir.exists():
        shutil.rmtree(fixtures_dir, ignore_errors=True)
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Test Case 1: Unisolated Python Project (Should Fail)
        proj_unisolated = fixtures_dir / "unisolated"
        proj_unisolated.mkdir(exist_ok=True)
        (proj_unisolated / "pyproject.toml").write_text('[project]\nname="test"\nversion="0.1.0"')
        
        guard_fail = EnvironmentGuard(root_dir=proj_unisolated)
        code_fail = guard_fail.run_all_checks()
        if code_fail == 0:
            errors.append("EnvironmentGuard failed to flag unisolated Python project without .venv/")
        else:
            print("  [PASS] Correctly blocked project missing .venv/")

        # Test Case 2: Isolated Python Project (Should Pass)
        proj_isolated = fixtures_dir / "isolated"
        proj_isolated.mkdir(exist_ok=True)
        (proj_isolated / "pyproject.toml").write_text('[project]\nname="test"\nversion="0.1.0"')
        (proj_isolated / ".venv").mkdir(exist_ok=True)
        (proj_isolated / "uv.lock").write_text("# uv.lock")
        (proj_isolated / ".python-version").write_text("3.12")

        guard_pass = EnvironmentGuard(root_dir=proj_isolated)
        code_pass = guard_pass.run_all_checks()
        if code_pass != 0:
            errors.append(f"EnvironmentGuard incorrectly failed isolated project (code {code_pass})")
        else:
            print("  [PASS] Correctly validated isolated project with .venv and lockfile")

    finally:
        shutil.rmtree(fixtures_dir, ignore_errors=True)

    if errors:
        print(f"\n[FAIL] Hook tests failed with {len(errors)} errors:")
        for err in errors:
            print(f"  ❌ {err}")
        return 1

    print("  [PASS] Environment Guard passed all mock test scenarios.")
    return 0


if __name__ == "__main__":
    sys.exit(test_hooks())
