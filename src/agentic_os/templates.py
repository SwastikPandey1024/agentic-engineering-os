"""
AgenticOS Starter Templates Engine.

Manages discovery and scaffolding of canonical starter archetypes
(python-service, ai-ml, rag-llm, fullstack, production-service).
ASCII-safe across all Windows, macOS, and Linux terminal encodings.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ANSI color codes
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_GRAY = "\033[90m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

TEMPLATE_DESCRIPTIONS: Dict[str, str] = {
    "python-service": "FastAPI microservice with Pydantic v2 validation, health probes, and pytest suite.",
    "ai-ml": "Tabular ML pipeline with Scikit-Learn baselines, leak-free preprocessing, and evaluation tests.",
    "rag-llm": "Retrieval-Augmented Generation pipeline with FAISS vector indexing and typed query contracts.",
    "fullstack": "Fullstack application with React 19 SPA frontend, Vite, FastAPI backend, and Docker Compose.",
    "production-service": "Enterprise microservice with OpenTelemetry tracing, structured JSON logging, and Dockerfile.",
}


def _colorize(text: str, color: str) -> str:
    if sys.stdout.isatty() or os.getenv("TERM") or os.getenv("COLORTERM"):
        return f"{color}{text}{COLOR_RESET}"
    return text


def find_templates_root() -> Path:
    """Locates the canonical templates directory in package or repo."""
    # 1. Environment variable
    env_root = os.getenv("AGENTIC_OS_ROOT")
    if env_root:
        cand = Path(os.path.abspath(env_root)) / "templates"
        if cand.is_dir():
            return cand

    # 2. Installed wheel package location (src/agentic_os/templates or site-packages/agentic_os/templates)
    pkg_cand = Path(os.path.abspath(Path(__file__).parent)) / "templates"
    if pkg_cand.is_dir():
        return pkg_cand

    # 3. Source repository location (src/agentic_os/templates.py -> ../../templates)
    repo_cand = Path(os.path.abspath(Path(__file__).parent.parent.parent)) / "templates"
    if repo_cand.is_dir():
        return repo_cand

    # 4. Current working directory
    cwd_cand = Path(os.path.abspath(".")) / "templates"
    if cwd_cand.is_dir():
        return cwd_cand

    raise RuntimeError(
        "Could not locate canonical AgenticOS templates directory. "
        "Ensure AgenticOS is installed properly or AGENTIC_OS_ROOT is set."
    )


def list_templates() -> Dict[str, str]:
    """Returns a dictionary of available template names and descriptions."""
    try:
        root = find_templates_root()
        available: Dict[str, str] = {}
        for item in sorted(root.iterdir()):
            if item.is_dir() and not item.name.startswith((".", "_")):
                desc = TEMPLATE_DESCRIPTIONS.get(item.name, "Starter archetype template.")
                available[item.name] = desc
        return available
    except Exception:
        return TEMPLATE_DESCRIPTIONS.copy()


def print_template_catalog() -> None:
    """Prints the available templates formatted in a clean ASCII table."""
    templates = list_templates()
    print(_colorize("\n=======================================================", COLOR_CYAN))
    print(_colorize("        AgenticOS Starter Archetypes Catalog          ", COLOR_BOLD + COLOR_CYAN))
    print(_colorize("=======================================================\n", COLOR_CYAN))
    for name, desc in templates.items():
        print(f"  * {_colorize(name, COLOR_BOLD + COLOR_GREEN):<30} {desc}")
    print(_colorize("\nTo scaffold a project, run:", COLOR_GRAY))
    print(_colorize("  agentic-os new <project-name> --template <template-name>\n", COLOR_CYAN))


def validate_project_name(name: str) -> None:
    """Ensures project name is valid and does not perform path traversal."""
    if not name or not name.strip():
        raise ValueError("Project name cannot be empty.")

    clean_name = name.strip()
    # Check for path traversal characters
    if ".." in clean_name or clean_name.startswith(("/", "\\")):
        raise ValueError(f"Invalid project name '{name}'. Path traversal and absolute paths are prohibited.")

    if not re.match(r"^[a-zA-Z0-9_-]+$", clean_name):
        raise ValueError(
            f"Invalid project name '{name}'. Only alphanumeric characters, dashes, and underscores are permitted."
        )


def collect_template_files(template_dir: Path) -> List[Tuple[Path, Path]]:
    """Returns list of (source_file, rel_path) excluding caches, venvs, and metadata."""
    ignore_names = {
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".git",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".DS_Store",
        "Thumbs.db",
    }
    ignore_exts = {".pyc", ".pyo", ".egg-info"}

    files_to_copy: List[Tuple[Path, Path]] = []
    for root, dirs, files in os.walk(template_dir):
        # Filter out directories to prevent traversing into them
        dirs[:] = [d for d in dirs if d not in ignore_names]

        for file in files:
            if file in ignore_names or any(file.endswith(ext) for ext in ignore_exts):
                continue
            src_file = Path(root) / file
            rel_path = src_file.relative_to(template_dir)
            files_to_copy.append((src_file, rel_path))

    return files_to_copy


def run_new(
    project_name: str,
    template_name: Optional[str] = None,
    target_dir: Optional[Path | str] = None,
    force: bool = False,
    dry_run: bool = False,
    init_git: bool = False,
    quiet: bool = False,
) -> int:
    """
    Scaffolds a new project from a canonical template archetype.

    Returns:
        0 on success or clean dry-run
        1 on invalid arguments or safety conflict
    """
    # 1. Validate project name
    try:
        validate_project_name(project_name)
    except ValueError as e:
        if not quiet:
            print(_colorize(f"[FAIL] {e}", COLOR_RED))
        return 1

    # 2. Check template existence
    available = list_templates()
    if not template_name:
        if not quiet:
            print(_colorize("[FAIL] Missing required argument '--template <template-name>'.", COLOR_RED))
            print_template_catalog()
        return 1

    if template_name not in available:
        if not quiet:
            print(_colorize(f"[FAIL] Unknown template '{template_name}'.", COLOR_RED))
            print_template_catalog()
        return 1

    # 3. Locate template directory
    try:
        templates_root = find_templates_root()
        template_dir = templates_root / template_name
        if not template_dir.is_dir():
            raise RuntimeError(f"Template directory '{template_dir}' not found on disk.")
    except Exception as e:
        if not quiet:
            print(_colorize(f"[FAIL] {e}", COLOR_RED))
        return 1

    # 4. Resolve and validate target path
    if target_dir:
        dest = Path(os.path.abspath(str(target_dir)))
    else:
        dest = Path(os.path.abspath(project_name))

    if dest.exists() and any(dest.iterdir()) and not force:
        if not quiet:
            print(
                _colorize(
                    f"[FAIL] Destination directory '{dest}' already exists and is not empty. "
                    "Use '--force' to overwrite existing files.",
                    COLOR_RED,
                )
            )
        return 1

    if not quiet:
        print(_colorize("\n=======================================================", COLOR_CYAN))
        print(_colorize("          AgenticOS New - Project Generator            ", COLOR_BOLD + COLOR_CYAN))
        print(_colorize("=======================================================\n", COLOR_CYAN))
        print(f"  * Project Name:    {project_name}")
        print(f"  * Archetype:       {template_name} ({available.get(template_name, '')})")
        print(f"  * Target Location: {dest}")
        print(f"  * Mode:            {'DRY-RUN (Preview)' if dry_run else 'ACTIVE GENERATION'}")
        print(f"  * Force Overwrite: {'ENABLED' if force else 'DISABLED'}")
        print(f"  * Initialize Git:  {'YES' if init_git else 'NO'}\n")

    # 5. Collect template files
    files = collect_template_files(template_dir)
    if not files:
        if not quiet:
            print(_colorize(f"[FAIL] No template files found in '{template_dir}'.", COLOR_RED))
        return 1

    created: List[Path] = []
    for src_file, rel_path in files:
        dst_file = dest / rel_path
        if not dry_run:
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            if rel_path.name.endswith(".sh") and os.name != "nt":
                try:
                    dst_file.chmod(0o755)
                except Exception:
                    pass
        created.append(rel_path)
        if not quiet:
            print(f"  {_colorize('[CREATE]', COLOR_GREEN)} {rel_path}")

    # 6. Optional Git Init
    if init_git and not dry_run:
        try:
            subprocess.run(["git", "init", str(dest)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not quiet:
                print(f"\n  {_colorize('[GIT]', COLOR_GREEN)} Initialized empty Git repository in {dest}")
        except Exception:
            pass

    if not quiet:
        print(_colorize("\nGeneration Summary:", COLOR_BOLD))
        print(f"  * Created Files:   {len(created)}")
        if dry_run:
            print(_colorize("\n[PASS] Dry-run complete. No files were written to disk.\n", COLOR_CYAN))
        else:
            print(_colorize(f"\n[PASS] Successfully generated project '{project_name}' from template '{template_name}'!\n", COLOR_BOLD + COLOR_GREEN))
            print(_colorize("Next Steps:", COLOR_BOLD))
            print(f"  1. cd {project_name}")
            print("  2. uv venv .venv --python 3.12")
            print("  3. uv sync")
            print("  4. uv run pytest\n")

    return 0
