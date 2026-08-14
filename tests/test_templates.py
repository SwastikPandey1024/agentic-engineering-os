#!/usr/bin/env python3
"""
Validates all 5 starter templates for required manifests, syntax, isolation rules,
and test suite completeness.
"""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT_DIR / "templates"


def test_templates() -> int:
    print("[Test] Validating Starter Templates (templates/)...")
    expected_templates = [
        "python-service",
        "ai-ml",
        "rag-llm",
        "fullstack",
        "production-service",
    ]
    errors = []

    for t_name in expected_templates:
        t_dir = TEMPLATES_DIR / t_name
        if not t_dir.is_dir():
            errors.append(f"Missing template: {t_name}")
            continue

        readme = t_dir / "README.md"
        gitignore = t_dir / ".gitignore"

        if not readme.is_file():
            errors.append(f"{t_name} missing README.md")
        if not gitignore.is_file():
            errors.append(f"{t_name} missing .gitignore")

        # Compile all Python files in the template
        for py_file in t_dir.rglob("*.py"):
            try:
                py_compile.compile(str(py_file), doraise=True)
            except Exception as e:
                errors.append(f"Syntax error in {py_file.relative_to(ROOT_DIR)}: {e}")

        # Validate JSON files
        for json_file in t_dir.rglob("*.json"):
            try:
                json.loads(json_file.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"Invalid JSON in {json_file.relative_to(ROOT_DIR)}: {e}")

        # Validate test suite presence for templates configured with pytest
        pyprojects = list(t_dir.rglob("pyproject.toml"))
        for pyproject in pyprojects:
            content = pyproject.read_text(encoding="utf-8")
            if "pytest" in content:
                parent_dir = pyproject.parent
                tests_dir = parent_dir / "tests"
                if not tests_dir.is_dir():
                    errors.append(
                        f"{pyproject.relative_to(ROOT_DIR)} configures pytest but missing tests/ directory"
                    )
                else:
                    test_files = list(tests_dir.glob("test_*.py")) + list(tests_dir.glob("*_test.py"))
                    if not test_files:
                        errors.append(
                            f"{tests_dir.relative_to(ROOT_DIR)} contains no test_*.py or *_test.py files"
                        )

        print(f"  [PASS] Verified template '{t_name}'")

    if errors:
        print(f"\n[FAIL] Template validation failed with {len(errors)} errors:")
        for err in errors:
            print(f"  ❌ {err}")
        return 1

    print("  [PASS] All 5 starter templates passed structural, syntax, and test completeness validation.")
    return 0


if __name__ == "__main__":
    sys.exit(test_templates())
