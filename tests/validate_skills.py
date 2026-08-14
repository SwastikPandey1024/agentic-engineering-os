#!/usr/bin/env python3
"""
Validates that all skills in .agents/skills/ have valid YAML frontmatter,
kebab-case naming, trigger-oriented descriptions, and all 6 Core Questions.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"


def validate_skills() -> int:
    print("[Test] Validating Modular Skills (.agents/skills/)...")
    if not SKILLS_DIR.is_dir():
        print(f"  [ERROR] Skills directory not found: {SKILLS_DIR}")
        return 1

    skills = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
    print(f"  [INFO] Found {len(skills)} modular skills.")
    errors = []

    for s in sorted(skills, key=lambda x: x.name):
        skill_file = s / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"Missing SKILL.md in {s.name}")
            continue

        content = skill_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            errors.append(f"{s.name}/SKILL.md does not start with '---'")
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(f"{s.name}/SKILL.md has malformed YAML frontmatter")
            continue

        frontmatter = parts[1].strip()
        body = parts[2]

        name_match = re.search(r"^name:\s*([a-z0-9-]+)", frontmatter, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+)", frontmatter, re.MULTILINE)

        if not name_match or name_match.group(1) != s.name:
            errors.append(f"{s.name}/SKILL.md name mismatch in frontmatter")
        if not desc_match or len(desc_match.group(1).strip()) < 10:
            errors.append(f"{s.name}/SKILL.md missing descriptive trigger summary")

        # Verify presence of the 6 Core Questions
        required_questions = [
            ("Q1: When to use", ["When Should I Use This", "When should I use this"]),
            ("Q2: What to inspect", ["What Should I Inspect First", "What should I inspect first"]),
            ("Q3: Workflow", ["What Workflow Should I Follow", "What workflow should I follow"]),
            ("Q4: Decisions", ["What Decisions Should I Make", "What decisions should I make"]),
            ("Q5: Avoid", ["What Should I Avoid", "What should I avoid"]),
            ("Q6: Verification", ["How Should I Verify Success", "How should I verify success"]),
        ]

        missing_q = []
        for q_label, variants in required_questions:
            if not any(v in body for v in variants):
                missing_q.append(q_label)

        if missing_q:
            errors.append(f"{s.name}/SKILL.md missing core sections: {missing_q}")

    if errors:
        print(f"\n[FAIL] Skill validation failed with {len(errors)} errors:")
        for err in errors:
            print(f"  ❌ {err}")
        return 1

    print(f"  [PASS] All {len(skills)} skills successfully validated against V1.0 standard.")
    return 0


if __name__ == "__main__":
    sys.exit(validate_skills())
