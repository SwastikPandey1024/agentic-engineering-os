#!/usr/bin/env python3
"""
Comprehensive tests for AgenticOS CLI: Foundation, Doctor, Init, and New Template Generator.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(os.path.abspath(Path(__file__).parent.parent))
sys.path.insert(0, str(ROOT_DIR / "src"))

from agentic_os import __version__
from agentic_os.cli import create_parser, main
from agentic_os.doctor import run_doctor
from agentic_os.guard import ProjectDiagnostics
from agentic_os.init import find_source_root, run_init
from agentic_os.templates import list_templates, run_new


def test_cli_foundation() -> None:
    print("[Test 1/10] Validating CLI Foundation & Arguments...")
    parser = create_parser()
    assert parser.prog == "agentic-os"
    assert main([]) == 0


def test_doctor_healthy_project(tmp_path: Path) -> None:
    print("[Test 2/10] Validating Doctor on a Healthy Project...")
    proj = tmp_path / "healthy_project"
    proj.mkdir(parents=True, exist_ok=True)

    (proj / ".git").mkdir()
    (proj / "AGENTS.md").write_text("# Invariant Rules", encoding="utf-8")
    (proj / ".agents" / "skills" / "test-skill").mkdir(parents=True, exist_ok=True)
    (proj / ".agents" / "skills" / "test-skill" / "SKILL.md").write_text(
        "---\nname: test-skill\ndescription: Test skill\n---\n", encoding="utf-8"
    )
    (proj / "hooks").mkdir()
    (proj / "pyproject.toml").write_text('[project]\nname="test"\nversion="0.1.0"', encoding="utf-8")
    (proj / ".venv").mkdir()
    (proj / "uv.lock").write_text("# uv.lock", encoding="utf-8")
    (proj / ".python-version").write_text("3.12", encoding="utf-8")

    diag = ProjectDiagnostics(root_dir=proj)
    metrics = diag.collect()
    assert metrics["is_git"] is True
    assert metrics["has_agents_md"] is True
    assert metrics["skills_count"] == 1
    assert metrics["python_info"]["has_venv"] is True
    assert metrics["python_info"]["has_lockfile"] is True
    assert len(diag.errors) == 0

    code = run_doctor(target_dir=proj, quiet=True)
    assert code == 0, f"Doctor should exit 0 on healthy project, got {code}"


def test_doctor_unisolated_project(tmp_path: Path) -> None:
    print("[Test 3/10] Validating Doctor Error Detection on Unisolated Project...")
    proj = tmp_path / "unisolated_project"
    proj.mkdir(parents=True, exist_ok=True)

    (proj / "pyproject.toml").write_text('[project]\nname="test"\nversion="0.1.0"', encoding="utf-8")

    diag = ProjectDiagnostics(root_dir=proj)
    metrics = diag.collect()
    assert metrics["python_info"]["has_venv"] is False
    assert len(diag.errors) > 0

    code = run_doctor(target_dir=proj, quiet=True)
    assert code == 1, f"Doctor should exit 1 on unisolated project, got {code}"


def test_init_bootstrap_and_idempotency(tmp_path: Path) -> None:
    print("[Test 4/10] Validating Init Bootstrap, Idempotency & Dry-Run...")
    target = tmp_path / "bootstrap_target"
    target.mkdir(parents=True, exist_ok=True)

    # 1. Dry Run
    code_dry = run_init(target_dir=target, dry_run=True, quiet=True)
    assert code_dry == 0
    assert not (target / "AGENTS.md").exists(), "Dry-run should not write files"

    # 2. Active Bootstrap
    code_init = run_init(target_dir=target, quiet=True)
    assert code_init == 0, f"Init should succeed on empty dir, got {code_init}"
    assert (target / "AGENTS.md").is_file()
    assert (target / ".agents" / "skills").is_dir()
    assert (target / "hooks" / "environment_guard.py").is_file()

    # 3. Idempotent Second Run (All files identical -> Skipped)
    code_idempotent = run_init(target_dir=target, quiet=True)
    assert code_idempotent == 0, "Idempotent re-run should exit 0 without conflicts"


def test_init_conflict_handling(tmp_path: Path) -> None:
    print("[Test 5/10] Validating Init Conflict Safety & Force Overwrite...")
    target = tmp_path / "conflict_target"
    target.mkdir(parents=True, exist_ok=True)

    # Pre-populate with conflicting modified AGENTS.md
    (target / "AGENTS.md").write_text("# CUSTOM MODIFIED RULES THAT CONFLICT", encoding="utf-8")

    # Run without --force -> Conflict detected, exit 1
    code_conflict = run_init(target_dir=target, force=False, quiet=True)
    assert code_conflict == 1, "Init without force should fail on modified file conflict"
    assert (target / "AGENTS.md").read_text(encoding="utf-8") == "# CUSTOM MODIFIED RULES THAT CONFLICT"

    # Run with --force -> Overwrites conflicting file, exit 0
    code_force = run_init(target_dir=target, force=True, quiet=True)
    assert code_force == 0, "Init with force should overwrite conflicting file and exit 0"
    assert (target / "AGENTS.md").read_text(encoding="utf-8") != "# CUSTOM MODIFIED RULES THAT CONFLICT"


def test_list_templates() -> None:
    print("[Test 6/10] Validating List Available Starter Archetypes...")
    templates = list_templates()
    expected = {"python-service", "ai-ml", "rag-llm", "fullstack", "production-service"}
    assert expected.issubset(templates.keys()), f"Missing templates in {templates.keys()}"


def test_all_five_templates_generation(tmp_path: Path) -> None:
    print("[Test 7/10] Validating Scaffolding for All 5 Production Archetypes...")
    all_templates = ["python-service", "ai-ml", "rag-llm", "fullstack", "production-service"]

    for tmpl in all_templates:
        proj_dir = tmp_path / f"gen_{tmpl}"
        code = run_new(
            project_name=f"gen_{tmpl}",
            template_name=tmpl,
            target_dir=proj_dir,
            quiet=True,
        )
        assert code == 0, f"Template generation for '{tmpl}' failed with code {code}"
        assert proj_dir.is_dir(), f"Generated directory '{proj_dir}' does not exist"
        assert (proj_dir / "README.md").is_file(), f"Missing README.md in {tmpl}"

        # Assert no .git created by default
        assert not (proj_dir / ".git").exists(), f"Generated '{tmpl}' should not contain .git"

        # Assert no bytecode or cache
        for root, dirs, files in os.walk(proj_dir):
            assert "__pycache__" not in dirs, f"__pycache__ found in {root}"
            for f in files:
                assert not f.endswith((".pyc", ".pyo")), f"Bytecode file {f} found in {root}"


def test_template_safety_and_conflicts(tmp_path: Path) -> None:
    print("[Test 8/10] Validating Template Non-Empty Conflict & Dry-Run Safety...")
    target = tmp_path / "conflict_app"
    target.mkdir(parents=True, exist_ok=True)
    (target / "existing_file.txt").write_text("pre-existing content", encoding="utf-8")

    # 1. Non-empty directory without --force fails with 1
    code_conflict = run_new(
        project_name="conflict_app",
        template_name="python-service",
        target_dir=target,
        force=False,
        quiet=True,
    )
    assert code_conflict == 1, "Non-empty destination directory should fail without --force"

    # 2. Non-empty directory with --force succeeds with 0
    code_force = run_new(
        project_name="conflict_app",
        template_name="python-service",
        target_dir=target,
        force=True,
        quiet=True,
    )
    assert code_force == 0, "Non-empty destination directory with --force should succeed"
    assert (target / "README.md").is_file()

    # 3. Dry-run produces no files on a clean path
    dry_target = tmp_path / "dry_app"
    code_dry = run_new(
        project_name="dry_app",
        template_name="ai-ml",
        target_dir=dry_target,
        dry_run=True,
        quiet=True,
    )
    assert code_dry == 0
    assert not dry_target.exists(), "Dry-run should not create destination directory"


def test_invalid_template_and_path_traversal(tmp_path: Path) -> None:
    print("[Test 9/10] Validating Invalid Template & Path Traversal Rejection...")
    # 1. Invalid template name
    code_invalid_tmpl = run_new(
        project_name="test_bad_tmpl",
        template_name="nonexistent-template",
        target_dir=tmp_path / "test_bad_tmpl",
        quiet=True,
    )
    assert code_invalid_tmpl == 1

    # 2. Path traversal in project name
    for bad_name in ["../escape", "sub/dir", "..\\escape", "/root"]:
        code_bad_name = run_new(
            project_name=bad_name,
            template_name="python-service",
            quiet=True,
        )
        assert code_bad_name == 1, f"Path traversal name '{bad_name}' was not rejected"


def test_cli_subcommands(tmp_path: Path) -> None:
    print("[Test 10/10] Validating CLI Subcommands Execution via main()...")
    target = tmp_path / "cli_subcommand_target"

    # 1. Test 'init' via CLI main
    code_cli_init = main(["init", str(target), "-q"])
    assert code_cli_init == 0
    assert (target / "AGENTS.md").is_file()

    # 2. Test 'doctor' via CLI main
    code_bare_doctor = main(["doctor", str(target), "-q"])
    assert code_bare_doctor == 0

    # 3. Test 'new' via CLI main
    cli_app_dir = tmp_path / "cli_new_app"
    code_cli_new = main(["new", "cli_new_app", "-t", "rag-llm", "-q"])
    assert code_cli_new == 0
    # Clean up cli_new_app from wherever cwd was
    if (ROOT_DIR / "cli_new_app").exists():
        shutil.rmtree(ROOT_DIR / "cli_new_app", ignore_errors=True)
    if (Path.cwd() / "cli_new_app").exists():
        shutil.rmtree(Path.cwd() / "cli_new_app", ignore_errors=True)


def run_all_tests() -> int:
    scratch_dir = ROOT_DIR / "tests" / "fixtures" / "_cli_test_scratch"
    if scratch_dir.exists():
        shutil.rmtree(scratch_dir, ignore_errors=True)
    scratch_dir.mkdir(parents=True, exist_ok=True)

    try:
        test_cli_foundation()
        test_doctor_healthy_project(scratch_dir)
        test_doctor_unisolated_project(scratch_dir)
        test_init_bootstrap_and_idempotency(scratch_dir)
        test_init_conflict_handling(scratch_dir)
        test_list_templates()
        test_all_five_templates_generation(scratch_dir)
        test_template_safety_and_conflicts(scratch_dir)
        test_invalid_template_and_path_traversal(scratch_dir)
        test_cli_subcommands(scratch_dir)
        print("\n  [PASS] All 10 CLI, Doctor, Init, and New Template Generator unit tests PASSED successfully!")
        return 0
    finally:
        shutil.rmtree(scratch_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(run_all_tests())
