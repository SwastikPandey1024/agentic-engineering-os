"""
AgenticOS Doctor — Environment Diagnostics Command.

Inspects virtual environments, toolchains, lockfile hygiene, and AgenticOS assets.
ASCII-safe across all Windows, macOS, and Linux terminal encodings.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Sequence

from agentic_os.guard import ProjectDiagnostics

# ANSI color codes
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def _colorize(text: str, color: str) -> str:
    if sys.stdout.isatty() or os.getenv("TERM") or os.getenv("COLORTERM"):
        return f"{color}{text}{COLOR_RESET}"
    return text


def run_doctor(target_dir: Path | str = ".", strict: bool = False, quiet: bool = False) -> int:
    """Runs diagnostics against target directory and reports formatted health status."""
    path = Path(os.path.abspath(str(target_dir)))
    diag = ProjectDiagnostics(root_dir=path)
    metrics = diag.collect()

    if quiet:
        if diag.errors or (strict and diag.warnings):
            return 1
        return 0

    print(_colorize("\n=======================================================", COLOR_CYAN))
    print(_colorize("           AgenticOS Doctor - Health Check             ", COLOR_BOLD + COLOR_CYAN))
    print(_colorize("=======================================================\n", COLOR_CYAN))

    # 1. Project Context
    print(_colorize("[1/4] Project Context", COLOR_BOLD))
    print(f"  * Root Path:       {metrics['root_dir']}")
    if metrics["is_git"]:
        print(f"  * Git Repository:  {_colorize('[PASS]', COLOR_GREEN)} Initialized (.git)")
    else:
        print(f"  * Git Repository:  {_colorize('[WARN]', COLOR_YELLOW)} Not initialized")

    # 2. AgenticOS Foundations
    print(_colorize("\n[2/4] AgenticOS Invariants & Skills", COLOR_BOLD))
    if metrics["has_agents_md"]:
        print(f"  * Invariant Rules: {_colorize('[PASS]', COLOR_GREEN)} AGENTS.md present")
    else:
        print(f"  * Invariant Rules: {_colorize('[WARN]', COLOR_YELLOW)} AGENTS.md missing (run 'agentic-os init')")

    if metrics["has_skills_dir"] and metrics["skills_count"] > 0:
        print(f"  * Modular Skills:  {_colorize('[PASS]', COLOR_GREEN)} .agents/skills/ ({metrics['skills_count']} skills active)")
    elif metrics["has_skills_dir"]:
        print(f"  * Modular Skills:  {_colorize('[WARN]', COLOR_YELLOW)} .agents/skills/ is empty")
    else:
        print(f"  * Modular Skills:  {_colorize('[WARN]', COLOR_YELLOW)} .agents/skills/ missing (run 'agentic-os init')")

    if metrics["has_hooks_dir"]:
        print(f"  * Guard Hooks:     {_colorize('[PASS]', COLOR_GREEN)} hooks/ directory present")
    else:
        print(f"  * Guard Hooks:     {_colorize('[WARN]', COLOR_YELLOW)} hooks/ missing")

    # 3. Language Toolchain & Environment Isolation
    print(_colorize("\n[3/4] Runtime Isolation & Package Hygiene", COLOR_BOLD))
    py = metrics["python_info"]
    node = metrics["node_info"]

    if not py.get("active") and not node.get("active"):
        print("  * No Python or Node.js project manifests detected.")
    else:
        if py.get("active"):
            print(f"  * Python Tool:     {py['pkg_manager']}")
            print(f"  * Interpreter:     {py['system_python']} ({py['executable']})")

            if py["has_venv"]:
                print(f"  * Virtualenv:      {_colorize('[PASS]', COLOR_GREEN)} Isolated ({py['venv_path']})")
            else:
                print(f"  * Virtualenv:      {_colorize('[FAIL]', COLOR_RED)} Missing .venv/")

            if py["is_isolated"]:
                print(f"  * Active Shell:    {_colorize('[PASS]', COLOR_GREEN)} Running inside virtualenv")
            elif py["has_venv"]:
                print(f"  * Active Shell:    {_colorize('[WARN]', COLOR_YELLOW)} Outside .venv (use 'uv run <cmd>')")

            if py["has_lockfile"]:
                print(f"  * Lockfile:        {_colorize('[PASS]', COLOR_GREEN)} Present ({py['lockfile_name']})")
            elif py["has_pyproject"]:
                print(f"  * Lockfile:        {_colorize('[WARN]', COLOR_YELLOW)} Missing lockfile (run 'uv lock')")

        if node.get("active"):
            if node["has_modules"]:
                print(f"  * Node Modules:    {_colorize('[PASS]', COLOR_GREEN)} node_modules/ present")
            else:
                print(f"  * Node Modules:    {_colorize('[WARN]', COLOR_YELLOW)} node_modules/ missing")

            if node["has_lockfile"]:
                print(f"  * Node Lockfile:   {_colorize('[PASS]', COLOR_GREEN)} Present ({node['lockfile_name']})")
            else:
                print(f"  * Node Lockfile:   {_colorize('[FAIL]', COLOR_RED)} Missing package lockfile")

    # 4. Summary Scorecard
    print(_colorize("\n[4/4] Diagnostic Summary", COLOR_BOLD))
    print(f"  * Passed Checks:   {_colorize(str(len(diag.passes)), COLOR_GREEN)}")
    print(f"  * Warnings:        {_colorize(str(len(diag.warnings)), COLOR_YELLOW if diag.warnings else COLOR_GREEN)}")
    print(f"  * Critical Errors: {_colorize(str(len(diag.errors)), COLOR_RED if diag.errors else COLOR_GREEN)}")

    if diag.errors:
        print(_colorize("\n[FAIL] Critical Issues Requiring Attention:", COLOR_BOLD + COLOR_RED))
        for err in diag.errors:
            print(f"   * [ERROR] {err}")
        print()
        return 1

    if diag.warnings:
        print(_colorize("\n[WARN] Recommendations:", COLOR_YELLOW))
        for warn in diag.warnings:
            print(f"   * [WARN] {warn}")

    if strict and diag.warnings:
        print(_colorize("\nStrict mode enabled: failing due to warnings.\n", COLOR_RED))
        return 1

    print(_colorize("\n[PASS] Environment is healthy for agentic development.\n", COLOR_BOLD + COLOR_GREEN))
    return 0
