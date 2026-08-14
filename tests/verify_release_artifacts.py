#!/usr/bin/env python3
"""
Release verification and step summary helper for PyPI Trusted Publishing.
Standard library only: zero shell interpolation, zero external dependencies.
"""

from __future__ import annotations

import glob
import os
import sys
from pathlib import Path

# Python 3.11+ standard library tomllib
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:
        tomllib = None  # type: ignore


def parse_pyproject(project_root: Path) -> dict[str, str]:
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"[ERROR] pyproject.toml not found at {pyproject_path}")
        sys.exit(1)

    if tomllib is not None:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        project = data.get("project", {})
        return {
            "name": project.get("name", ""),
            "version": project.get("version", ""),
        }

    # Fallback basic parser if tomllib is unavailable
    name, version = "", ""
    with open(pyproject_path, "r", encoding="utf-8") as f:
        in_project = False
        for line in f:
            line = line.strip()
            if line == "[project]":
                in_project = True
                continue
            elif line.startswith("[") and in_project:
                break
            if in_project:
                if line.startswith("name ="):
                    name = line.split("=", 1)[1].strip().strip('"\'')
                elif line.startswith("version ="):
                    version = line.split("=", 1)[1].strip().strip('"\'')
    return {"name": name, "version": version}


def verify_release_artifacts(project_root: Path) -> int:
    tag = os.environ.get("GITHUB_REF_NAME", "").strip()
    if not tag:
        print("[ERROR] GITHUB_REF_NAME environment variable is empty or missing.")
        return 1

    if not tag.startswith("v"):
        print(f"[ERROR] Release tag '{tag}' does not start with 'v' (expected vX.Y.Z format).")
        return 1

    tag_version = tag[1:]
    project_meta = parse_pyproject(project_root)
    pkg_name = project_meta["name"]
    pkg_version = project_meta["version"]

    if not pkg_version:
        print("[ERROR] Failed to extract project version from pyproject.toml.")
        return 1

    if tag_version != pkg_version:
        print(
            f"[ERROR] Version mismatch! Git tag version is '{tag_version}', "
            f"but pyproject.toml version is '{pkg_version}'."
        )
        return 1

    dist_dir = project_root / "dist"
    if not dist_dir.exists():
        print(f"[ERROR] Distribution directory '{dist_dir}' does not exist.")
        return 1

    wheels = sorted(glob.glob(str(dist_dir / "*.whl")))
    sdists = sorted(glob.glob(str(dist_dir / "*.tar.gz")))

    if len(wheels) != 1:
        print(f"[ERROR] Expected exactly 1 wheel artifact in dist/, found {len(wheels)}: {wheels}")
        return 1

    if len(sdists) != 1:
        print(f"[ERROR] Expected exactly 1 source distribution (.tar.gz) in dist/, found {len(sdists)}: {sdists}")
        return 1

    wheel_name = Path(wheels[0]).name
    sdist_name = Path(sdists[0]).name

    print("=" * 60)
    print("      AgenticOS Release Artifact Verification")
    print("=" * 60)
    print(f"  [PASS] Package Name:        {pkg_name}")
    print(f"  [PASS] Release Tag:         {tag}")
    print(f"  [PASS] Package Version:     {pkg_version}")
    print(f"  [PASS] Wheel Artifact:      {wheel_name}")
    print(f"  [PASS] Source Distribution: {sdist_name}")
    print(f"  [PASS] Alignment:           Tag '{tag}' matches package version '{pkg_version}'.")
    print("=" * 60)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        summary_content = (
            "### 📦 Build & Release Verification Summary\n\n"
            "| Item | Value |\n"
            "| :--- | :--- |\n"
            f"| **Package Name** | `{pkg_name}` |\n"
            f"| **Release Tag** | `{tag}` |\n"
            f"| **Package Version** | `{pkg_version}` |\n"
            f"| **Wheel Artifact** | `{wheel_name}` |\n"
            f"| **Source Distribution** | `{sdist_name}` |\n"
            "| **Version Alignment** | ✅ Tag matches pyproject.toml |\n"
        )
        try:
            with open(summary_path, "a", encoding="utf-8") as f:
                f.write(summary_content)
            print(f"[PASS] Wrote release summary to {summary_path}")
        except Exception as e:
            print(f"[WARN] Could not write step summary: {e}")

    return 0


def record_publish_summary() -> int:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        print("[INFO] GITHUB_STEP_SUMMARY not set. Skipping publication summary.")
        return 0

    summary_content = (
        "### 🚀 PyPI Trusted Publication Summary\n\n"
        "| Property | Value |\n"
        "| :--- | :--- |\n"
        "| **Target Index** | [PyPI](https://pypi.org/p/agentic-engineering-os) |\n"
        "| **Environment** | `pypi` |\n"
        "| **Auth Mechanism** | PyPI Trusted Publishing (OIDC ID Token) |\n"
        "| **Stage** | Production Release |\n"
        "| **Status** | ✅ Published successfully |\n"
    )

    try:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(summary_content)
        print(f"[PASS] Successfully recorded publication summary to {summary_path}")
    except Exception as e:
        print(f"[WARN] Failed to write publication summary: {e}")

    return 0


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    if "--publish-summary" in sys.argv:
        return record_publish_summary()
    return verify_release_artifacts(project_root)


if __name__ == "__main__":
    sys.exit(main())
