#!/usr/bin/env python3
"""
Canonical Cross-Platform Environment Validation Engine.

Enforces virtual environment isolation, package manager detection,
lockfile hygiene, and interpreter verification across Windows, macOS, and Linux.
Requires only standard library Python 3.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ANSI color escape codes for terminal output
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_GRAY = "\033[90m"
COLOR_RESET = "\033[0m"


def print_colored(text: str, color: str = COLOR_RESET) -> None:
    """Print text with ANSI colors if stdout is a terminal, else plain text."""
    if sys.stdout.isatty() or os.getenv("TERM") or os.getenv("COLORTERM"):
        print(f"{color}{text}{COLOR_RESET}")
    else:
        print(text)


class EnvironmentGuard:
    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir = root_dir or Path.cwd()
        self.exit_code = 0
        self.warnings: list[str] = []
        self.errors: list[str] = []
        self.info: list[str] = []

    def run_all_checks(self) -> int:
        print_colored("[Environment Guard] Checking environment isolation & configuration...", COLOR_CYAN)
        print_colored(f"  [DIR] Project Root: {self.root_dir}", COLOR_GRAY)

        is_python = self._check_python_project()
        is_node = self._check_node_project()

        if not is_python and not is_node:
            print_colored("  [INFO] No Python or Node.js project manifests detected in current directory.", COLOR_GRAY)
            return 0

        if self.errors:
            print_colored("\n[Environment Guard] FAILED: Critical environment issues detected!", COLOR_RED)
            for err in self.errors:
                print_colored(f"  [ERROR] {err}", COLOR_RED)
            self.exit_code = 1
        else:
            print_colored("\n[Environment Guard] All environment isolation checks passed!", COLOR_GREEN)

        if self.warnings:
            print_colored("\n[Environment Guard] Warnings / Recommended Actions:", COLOR_YELLOW)
            for warn in self.warnings:
                print_colored(f"  [WARN] {warn}", COLOR_YELLOW)

        return self.exit_code

    def _check_python_project(self) -> bool:
        pyproject = self.root_dir / "pyproject.toml"
        requirements = self.root_dir / "requirements.txt"
        setup_py = self.root_dir / "setup.py"
        pipfile = self.root_dir / "Pipfile"
        env_yml = self.root_dir / "environment.yml"
        has_python_src = (self.root_dir / "app").is_dir() or (self.root_dir / "src").is_dir()

        if not (pyproject.exists() or requirements.exists() or setup_py.exists() or pipfile.exists() or env_yml.exists() or has_python_src):
            return False

        print_colored("  [CHECK] Python project detected.", COLOR_GRAY)

        # 1. Package Manager Detection
        pkg_manager = "pip/venv"
        if (self.root_dir / "uv.lock").exists() or pyproject.exists():
            pkg_manager = "uv"
        elif (self.root_dir / "poetry.lock").exists():
            pkg_manager = "poetry"
        elif (self.root_dir / "Pipfile.lock").exists():
            pkg_manager = "pipenv"
        elif env_yml.exists() or (self.root_dir / "environment.yaml").exists():
            pkg_manager = "conda"

        print_colored(f"  [PKG] Detected Package Toolchain: {pkg_manager}", COLOR_GRAY)

        # 2. Virtual Environment Detection (.venv/ or venv/)
        venv_dir = self.root_dir / ".venv"
        alt_venv = self.root_dir / "venv"
        conda_env = self.root_dir / ".conda_env"
        has_venv = venv_dir.is_dir() or alt_venv.is_dir() or conda_env.is_dir()

        if not has_venv and pkg_manager != "conda":
            self.errors.append(
                "No project-local virtual environment (.venv/) found!\n"
                "     Action: Create an isolated environment before running installs:\n"
                "     -> uv venv .venv --python 3.12 (or python -m venv .venv)"
            )
        else:
            print_colored("  [OK] Project virtual environment (.venv/) verified.", COLOR_GREEN)

        # 3. Active Interpreter Isolation Check
        current_exe = sys.executable
        is_isolated = (
            ".venv" in current_exe
            or "venv" in current_exe
            or "conda" in current_exe
            or "virtualenvs" in current_exe
            or (venv_dir.exists() and Path(current_exe).resolve() == (venv_dir / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")).resolve())
        )

        if not is_isolated and has_venv:
            self.warnings.append(
                f"Active shell Python interpreter ({current_exe}) is NOT inside .venv/.\n"
                "     Action: Run commands using 'uv run <command>' or activate .venv first."
            )

        # 4. Lockfile Hygiene Check
        if pkg_manager == "uv" and pyproject.exists() and not (self.root_dir / "uv.lock").exists():
            self.warnings.append(
                "pyproject.toml exists but uv.lock is missing.\n"
                "     Action: Run 'uv lock' or 'uv sync' to create a reproducible lockfile."
            )
        elif pkg_manager == "poetry" and not (self.root_dir / "poetry.lock").exists():
            self.warnings.append("poetry.lock is missing. Run 'poetry lock'.")

        # 5. Version Pinning Check
        if not (self.root_dir / ".python-version").exists() and not pyproject.exists():
            self.warnings.append("No .python-version file found. Consider pinning with 'echo 3.12 > .python-version'.")

        return True

    def _check_node_project(self) -> bool:
        package_json = self.root_dir / "package.json"
        if not package_json.exists():
            return False

        print_colored("  [CHECK] Node.js project detected.", COLOR_GRAY)

        # Check for node_modules
        if not (self.root_dir / "node_modules").is_dir():
            self.warnings.append("package.json exists but node_modules/ is missing. Run 'npm ci' or 'pnpm install'.")

        # Check for lockfile
        has_lockfile = (
            (self.root_dir / "package-lock.json").exists()
            or (self.root_dir / "pnpm-lock.yaml").exists()
            or (self.root_dir / "yarn.lock").exists()
            or (self.root_dir / "bun.lockb").exists()
            or (self.root_dir / "bun.lock").exists()
        )

        if not has_lockfile:
            self.errors.append(
                "No package lockfile (package-lock.json / pnpm-lock.yaml / yarn.lock / bun.lock) found!\n"
                "     Action: Run your package manager install to generate a lockfile."
            )

        return True


if __name__ == "__main__":
    guard = EnvironmentGuard()
    sys.exit(guard.run_all_checks())
