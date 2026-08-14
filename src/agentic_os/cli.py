"""
AgenticOS Command-Line Interface.

Provides developer tooling, environment diagnostics, project scaffolding,
and starter archetype generation for AI-assisted software engineering.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from agentic_os import __version__
from agentic_os.doctor import run_doctor
from agentic_os.init import run_init
from agentic_os.templates import print_template_catalog, run_new


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentic-os",
        description="AgenticOS: The Engineering Operating System for AI Coding Agents.",
        epilog="For documentation and guides, visit: https://github.com/SwastikPandey1024/agentic-engineering-os",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Display the AgenticOS version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", title="Available Commands")

    # 1. doctor subcommand
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Diagnose workspace environment isolation, toolchain, lockfiles, and AgenticOS assets.",
        description="Inspects project environment health, virtualenvs, lockfiles, and rules.",
    )
    doctor_parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target directory to inspect (default: current directory).",
    )
    doctor_parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail with non-zero exit code on warnings as well as critical errors.",
    )
    doctor_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Run silently, returning exit code only.",
    )

    # 2. init subcommand
    init_parser = subparsers.add_parser(
        "init",
        help="Bootstrap AgenticOS invariants, skills, and hooks into a project directory.",
        description="Installs .agents/skills/, hooks/, and AGENTS.md with conflict protection.",
    )
    init_parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory to bootstrap (default: current directory).",
    )
    init_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwrite existing conflicting files.",
    )
    init_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Preview files that would be created or modified without making changes.",
    )
    init_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress detailed file output, showing only summary.",
    )

    # 3. new subcommand (Starter Archetype Scaffolding)
    new_parser = subparsers.add_parser(
        "new",
        help="Generate a new project from a verified starter archetype.",
        description="Scaffolds a production starter template (python-service, ai-ml, rag-llm, fullstack, production-service).",
    )
    new_parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the new project directory to create.",
    )
    new_parser.add_argument(
        "-t",
        "--template",
        help="Starter archetype name (python-service, ai-ml, rag-llm, fullstack, production-service).",
    )
    new_parser.add_argument(
        "--list-templates",
        action="store_true",
        help="Display all available starter archetypes and descriptions.",
    )
    new_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwrite if destination directory already exists and is non-empty.",
    )
    new_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Preview template files without writing to disk.",
    )
    new_parser.add_argument(
        "--git",
        action="store_true",
        help="Initialize an empty Git repository in the generated project.",
    )
    new_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress detailed file output.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser()
    if argv is None:
        argv = sys.argv[1:]

    # If no arguments provided, display help and exit with 0
    if not argv:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)

    if args.command == "doctor":
        return run_doctor(target_dir=args.target, strict=args.strict, quiet=args.quiet)
    elif args.command == "init":
        return run_init(
            target_dir=args.target,
            force=args.force,
            dry_run=args.dry_run,
            quiet=args.quiet,
        )
    elif args.command == "new":
        if args.list_templates:
            print_template_catalog()
            return 0
        if not args.project_name:
            parser.error("the following arguments are required: project_name (or use --list-templates)")
        return run_new(
            project_name=args.project_name,
            template_name=args.template,
            force=args.force,
            dry_run=args.dry_run,
            init_git=args.git,
            quiet=args.quiet,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
