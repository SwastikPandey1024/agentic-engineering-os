#!/usr/bin/env python3
"""
Scans all repository files for potential secret leaks, private keys, or credentials.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),  # OpenAI-like API keys
    re.compile(r"AIza[0-9A-Za-z-_]{35}"),  # Google API keys
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),  # GitHub PATs
    re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,}"),  # Slack tokens
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),  # Private keys
]

IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


def scan_secrets() -> int:
    print("[Test] Scanning repository for secrets & sensitive tokens...")
    leaks = []

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            file_path = Path(root) / f
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for pattern in SECRET_PATTERNS:
                    if pattern.search(content):
                        # Verify it is not an intentional placeholder
                        if "YOUR_API_KEY" not in content and "${API_KEY}" not in content:
                            leaks.append(f"Secret pattern match in {file_path.relative_to(ROOT_DIR)}")
            except Exception as e:
                print(f"  [WARN] Could not read {file_path}: {e}")

    if leaks:
        print(f"\n[FAIL] Found {len(leaks)} potential secrets:")
        for leak in leaks:
            print(f"  ❌ {leak}")
        return 1

    print("  [PASS] Zero secrets or private keys detected across all files.")
    return 0


if __name__ == "__main__":
    sys.exit(scan_secrets())
