"""
AgenticOS Init Command.

Bootstraps AgenticOS invariants, modular skills, and deterministic hooks
into a target workspace with conflict safety and dry-run preview.
ASCII-safe across all Windows, macOS, and Linux terminal encodings.
"""

from __future__ import annotations

import filecmp
import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple

# ANSI color codes
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_GRAY = "\033[90m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def _colorize(text: str, color: str) -> str:
    if sys.stdout.isatty() or os.getenv("TERM") or os.getenv("COLORTERM"):
        return f"{color}{text}{COLOR_RESET}"
    return text


def find_source_root() -> Path:
    """Locates the canonical AgenticOS source directory containing .agents, hooks, and AGENTS.md."""
    # 1. Check AGENTIC_OS_ROOT environment variable if set
    env_root = os.getenv("AGENTIC_OS_ROOT")
    if env_root and Path(env_root).is_dir():
        cand = Path(os.path.abspath(env_root))
        if (cand / "AGENTS.md").exists() and (cand / ".agents").is_dir():
            return cand

    # 2. Check installed package location: src/agentic_os/ or site-packages/agentic_os/
    pkg_root = Path(os.path.abspath(Path(__file__).parent))
    if (pkg_root / "AGENTS.md").exists() and (pkg_root / ".agents").is_dir():
        return pkg_root

    # 3. Check repo root relative to this file: src/agentic_os/init.py -> ../../
    repo_root = Path(os.path.abspath(Path(__file__).parent.parent.parent))
    if (repo_root / "AGENTS.md").exists() and (repo_root / ".agents").is_dir():
        return repo_root

    # 4. Check current working directory
    cwd = Path(os.path.abspath("."))
    if (cwd / "AGENTS.md").exists() and (cwd / ".agents").is_dir():
        return cwd

    raise RuntimeError(
        "Could not locate canonical AgenticOS source directory (.agents, hooks, AGENTS.md). "
        "Set AGENTIC_OS_ROOT environment variable or run from the AgenticOS repository."
    )


def _files_are_identical(src: Path, dst: Path) -> bool:
    """Checks if two files have identical content."""
    if not dst.exists():
        return False
    if src.stat().st_size != dst.stat().st_size:
        return False
    h1 = hashlib.sha256(src.read_bytes()).digest()
    h2 = hashlib.sha256(dst.read_bytes()).digest()
    return h1 == h2


def collect_source_files(source_root: Path) -> List[Tuple[Path, Path]]:
    """Returns a list of (source_file, relative_dest_path) pairs to install."""
    files_to_copy: List[Tuple[Path, Path]] = []

    # 1. AGENTS.md
    agents_md = source_root / "AGENTS.md"
    if agents_md.is_file():
        files_to_copy.append((agents_md, Path("AGENTS.md")))

    # 2. .agents/ directory
    agents_dir = source_root / ".agents"
    if agents_dir.is_dir():
        for root, _, files in os.walk(agents_dir):
            for file in files:
                src_file = Path(root) / file
                rel_path = src_file.relative_to(source_root)
                files_to_copy.append((src_file, rel_path))

    # 3. hooks/ directory
    hooks_dir = source_root / "hooks"
    if hooks_dir.is_dir():
        for root, _, files in os.walk(hooks_dir):
            for file in files:
                if file.endswith((".pyc", ".pyo")) or "__pycache__" in root:
                    continue
                src_file = Path(root) / file
                rel_path = src_file.relative_to(source_root)
                files_to_copy.append((src_file, rel_path))

    return files_to_copy


def run_init(
    target_dir: Path | str = ".",
    force: bool = False,
    dry_run: bool = False,
    quiet: bool = False,
) -> int:
    """
    Bootstraps AgenticOS files into target_dir with conflict safety.

    Returns:
        0 on success or clean dry-run
        1 if unresolved conflicts occur or source files cannot be found
    """
    target = Path(os.path.abspath(str(target_dir)))

    try:
        source_root = find_source_root()
    except RuntimeError as e:
        if not quiet:
            print(_colorize(f"[FAIL] {e}", COLOR_RED))
        return 1

    if not quiet:
        print(_colorize("\n=======================================================", COLOR_CYAN))
        print(_colorize("           AgenticOS Init - Project Bootstrap          ", COLOR_BOLD + COLOR_CYAN))
        print(_colorize("=======================================================\n", COLOR_CYAN))
        print(f"  * Source Root:     {source_root}")
        print(f"  * Target Location: {target}")
        print(f"  * Mode:            {'DRY-RUN (Preview)' if dry_run else 'ACTIVE INSTALL'}")
        print(f"  * Force Overwrite: {'ENABLED' if force else 'DISABLED (Conflict-Safe)'}\n")

    files = collect_source_files(source_root)
    if not files:
        if not quiet:
            print(_colorize("[FAIL] No source files found to bootstrap.", COLOR_RED))
        return 1

    created: List[Path] = []
    skipped: List[Path] = []
    overwritten: List[Path] = []
    conflicted: List[Path] = []

    for src_file, rel_path in files:
        dst_file = target / rel_path

        if not dst_file.exists():
            # File does not exist -> Create
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

        elif _files_are_identical(src_file, dst_file):
            # Destination file is identical -> Idempotent skip
            skipped.append(rel_path)
            if not quiet:
                print(f"  {_colorize('[SKIP]', COLOR_GRAY)} {rel_path} (identical)")

        elif force:
            # Different and force enabled -> Overwrite
            if not dry_run:
                shutil.copy2(src_file, dst_file)
                if rel_path.name.endswith(".sh") and os.name != "nt":
                    try:
                        dst_file.chmod(0o755)
                    except Exception:
                        pass
            overwritten.append(rel_path)
            if not quiet:
                print(f"  {_colorize('[OVERWRITE]', COLOR_YELLOW)} {rel_path} (force)")

        else:
            # Different and not force -> Conflict
            conflicted.append(rel_path)
            if not quiet:
                print(f"  {_colorize('[CONFLICT]', COLOR_RED)} {rel_path} (modified, use --force to overwrite)")

    if not quiet:
        print(_colorize("\nBootstrap Summary:", COLOR_BOLD))
        print(f"  * Created:     {len(created)}")
        print(f"  * Skipped:     {len(skipped)} (already identical)")
        print(f"  * Overwritten: {len(overwritten)}")
        print(f"  * Conflicts:   {len(conflicted)}")

    if conflicted:
        if not quiet:
            print(_colorize("\n[FAIL] Bootstrap incomplete due to existing file conflicts.", COLOR_BOLD + COLOR_RED))
            print("   Pass '--force' to overwrite existing modified files.\n")
        return 1

    if not quiet:
        if dry_run:
            print(_colorize("\n[PASS] Dry-run complete. No files were written to disk.\n", COLOR_CYAN))
        else:
            print(_colorize("\n[PASS] AgenticOS bootstrap complete! Workspace is ready.\n", COLOR_BOLD + COLOR_GREEN))

    return 0
