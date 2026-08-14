"""
AgenticOS Environment Guard Engine and Diagnostics.

Provides environment isolation inspection, toolchain detection,
and lockfile verification for Python and Node.js projects.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class ProjectDiagnostics:
    """Collects and analyzes environment health metrics for a target project."""

    def __init__(self, root_dir: Path | str | None = None) -> None:
        if root_dir is None:
            self.root_dir = Path(os.path.abspath("."))
        else:
            self.root_dir = Path(os.path.abspath(str(root_dir)))
        self.metrics: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passes: List[str] = []

    def collect(self) -> Dict[str, Any]:
        """Collect all diagnostic information without printing."""
        self.metrics = {
            "root_dir": str(self.root_dir),
            "is_git": (self.root_dir / ".git").exists(),
            "has_agents_md": (self.root_dir / "AGENTS.md").is_file(),
            "has_skills_dir": (self.root_dir / ".agents" / "skills").is_dir(),
            "skills_count": self._count_skills(),
            "has_hooks_dir": (self.root_dir / "hooks").is_dir(),
            "is_python": self._is_python_project(),
            "is_node": (self.root_dir / "package.json").is_file(),
            "python_info": self._collect_python_info(),
            "node_info": self._collect_node_info(),
        }
        self._evaluate()
        return self.metrics

    def _count_skills(self) -> int:
        skills_dir = self.root_dir / ".agents" / "skills"
        if not skills_dir.is_dir():
            return 0
        return sum(1 for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())

    def _is_python_project(self) -> bool:
        indicators = [
            self.root_dir / "pyproject.toml",
            self.root_dir / "requirements.txt",
            self.root_dir / "setup.py",
            self.root_dir / "Pipfile",
            self.root_dir / "environment.yml",
            self.root_dir / "environment.yaml",
            self.root_dir / "app",
            self.root_dir / "src",
        ]
        return any(p.exists() for p in indicators)

    def _collect_python_info(self) -> Dict[str, Any]:
        if not self._is_python_project():
            return {"active": False}

        # Package manager detection
        pkg_manager = "pip/venv"
        pyproject = self.root_dir / "pyproject.toml"
        if (self.root_dir / "uv.lock").exists() or pyproject.exists():
            pkg_manager = "uv"
        elif (self.root_dir / "poetry.lock").exists():
            pkg_manager = "poetry"
        elif (self.root_dir / "Pipfile.lock").exists():
            pkg_manager = "pipenv"
        elif (self.root_dir / "environment.yml").exists() or (self.root_dir / "environment.yaml").exists():
            pkg_manager = "conda"

        # Virtualenv detection
        venv_dir = self.root_dir / ".venv"
        alt_venv = self.root_dir / "venv"
        has_venv = venv_dir.is_dir() or alt_venv.is_dir()

        # Active interpreter check
        current_exe = sys.executable
        is_isolated = (
            ".venv" in current_exe
            or "venv" in current_exe
            or "conda" in current_exe
            or "virtualenvs" in current_exe
            or (venv_dir.exists() and os.path.abspath(current_exe) == os.path.abspath(str(venv_dir / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python"))))
        )

        # Lockfile status
        has_lockfile = False
        lockfile_name = None
        if (self.root_dir / "uv.lock").exists():
            has_lockfile = True
            lockfile_name = "uv.lock"
        elif (self.root_dir / "poetry.lock").exists():
            has_lockfile = True
            lockfile_name = "poetry.lock"
        elif (self.root_dir / "Pipfile.lock").exists():
            has_lockfile = True
            lockfile_name = "Pipfile.lock"

        # Version pinning
        pinned_version = None
        if (self.root_dir / ".python-version").is_file():
            try:
                pinned_version = (self.root_dir / ".python-version").read_text(encoding="utf-8").strip()
            except Exception:
                pass

        return {
            "active": True,
            "system_python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "executable": current_exe,
            "pkg_manager": pkg_manager,
            "has_venv": has_venv,
            "venv_path": str(venv_dir if venv_dir.is_dir() else alt_venv if alt_venv.is_dir() else ""),
            "is_isolated": is_isolated,
            "has_lockfile": has_lockfile,
            "lockfile_name": lockfile_name,
            "pinned_version": pinned_version,
            "has_pyproject": pyproject.is_file(),
        }

    def _collect_node_info(self) -> Dict[str, Any]:
        pkg_json = self.root_dir / "package.json"
        if not pkg_json.is_file():
            return {"active": False}

        has_modules = (self.root_dir / "node_modules").is_dir()
        lockfile = None
        for candidate in ["pnpm-lock.yaml", "package-lock.json", "yarn.lock", "bun.lockb", "bun.lock"]:
            if (self.root_dir / candidate).exists():
                lockfile = candidate
                break

        return {
            "active": True,
            "has_node_modules": has_modules,
            "has_lockfile": lockfile is not None,
            "lockfile_name": lockfile,
        }

    def _evaluate(self) -> None:
        self.errors.clear()
        self.warnings.clear()
        self.passes.clear()

        # Git evaluation
        if self.metrics["is_git"]:
            self.passes.append("Git repository detected")
        else:
            self.warnings.append("Directory is not a Git repository (run 'git init')")

        # AgenticOS structure
        if self.metrics["has_agents_md"]:
            self.passes.append("AGENTS.md rules file present")
        else:
            self.warnings.append("AGENTS.md missing (run 'agentic-os init' to bootstrap)")

        if self.metrics["has_skills_dir"] and self.metrics["skills_count"] > 0:
            self.passes.append(f".agents/skills/ present ({self.metrics['skills_count']} skills active)")
        elif self.metrics["has_skills_dir"]:
            self.warnings.append(".agents/skills/ directory is empty")
        else:
            self.warnings.append(".agents/skills/ missing (run 'agentic-os init' to bootstrap)")

        # Python evaluation
        py = self.metrics["python_info"]
        if py.get("active"):
            if py["has_venv"]:
                self.passes.append("Project virtual environment (.venv/) verified")
            else:
                self.errors.append("No project-local virtual environment (.venv/) found! Run: uv venv .venv --python 3.12 (or python -m venv .venv)")

            if py["is_isolated"]:
                self.passes.append("Active Python interpreter is isolated in virtualenv")
            elif py["has_venv"]:
                self.warnings.append(f"Active Python ({py['executable']}) is outside .venv. Run commands using 'uv run' or activate .venv first.")

            if py["has_lockfile"]:
                self.passes.append(f"Lockfile hygiene verified ({py['lockfile_name']})")
            elif py["pkg_manager"] == "uv" and py["has_pyproject"]:
                self.warnings.append("pyproject.toml exists but uv.lock is missing. Run 'uv lock' or 'uv sync'.")
            elif py["pkg_manager"] == "poetry":
                self.warnings.append("poetry.lock is missing. Run 'poetry lock'.")

            if py["pinned_version"]:
                self.passes.append(f"Python version pinned ({py['pinned_version']})")
            elif not py["has_pyproject"]:
                self.warnings.append("No .python-version file found. Consider pinning with 'echo 3.12 > .python-version'.")

        # Node evaluation
        node = self.metrics["node_info"]
        if node.get("active"):
            if node["has_modules"]:
                self.passes.append("node_modules/ directory verified")
            else:
                self.warnings.append("package.json exists but node_modules/ is missing. Run 'npm ci' or 'pnpm install'.")

            if node["has_lockfile"]:
                self.passes.append(f"Node lockfile verified ({node['lockfile_name']})")
            else:
                self.errors.append("No package lockfile (package-lock.json / pnpm-lock.yaml / yarn.lock / bun.lock) found!")
