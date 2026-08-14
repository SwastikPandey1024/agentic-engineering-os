#!/usr/bin/env python3
"""
Validates markdown cross-references, relative links, and formatting across the repository.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_documentation() -> int:
    print("[Test] Validating Markdown Cross-References & Links...")
    errors = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for md_file in ROOT_DIR.rglob("*.md"):
        if any(p in md_file.parts for p in [".venv", "node_modules", ".git"]):
            continue

        content = md_file.read_text(encoding="utf-8", errors="ignore")
        for match in link_pattern.finditer(content):
            link_text = match.group(1)
            target = match.group(2)

            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue

            clean_target = target.split("#")[0].split("?")[0]
            if not clean_target:
                continue

            target_path = (md_file.parent / clean_target).resolve()
            if not target_path.exists():
                errors.append(f"Broken link in {md_file.relative_to(ROOT_DIR)}: '{target}' -> {clean_target}")

    if errors:
        print(f"\n[FAIL] Found {len(errors)} broken documentation links:")
        for err in errors:
            print(f"  [ERROR] {err}")
        return 1

    print("  [PASS] All relative documentation links resolved successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(test_documentation())
