# Contributing to AgenticOS

Thank you for your interest in contributing to **AgenticOS**!

Our mission is to give AI coding agents repeatable engineering standards, deterministic guardrails, project memory, and quality workflows.

---

## 📋 The 6 Core Questions Every Skill Must Answer

Every new skill authored in `.agents/skills/<skill-name>/SKILL.md` must answer these 6 fundamental questions:

1. **When should I use this?** — Clear activation triggers and non-triggers.
2. **What should I inspect first?** — Pre-modification inspection checklist (files, manifests, env vars).
3. **What workflow should I follow?** — Step-by-step execution protocol with diagrams and copy-pasteable commands.
4. **What decisions should I make?** — Concrete decision matrices and default recommendations.
5. **What should I avoid?** — Anti-patterns, destructive commands, and security hazards.
6. **How should I verify success?** — Deterministic test commands, assertions, or health checks.

---

## 🔍 Quality Review Checklist Before Submitting a PR

1. [ ] **Frontmatter**: Valid YAML frontmatter with kebab-case `name` matching the directory name.
2. [ ] **Cross-Platform**: Zero shell-specific assumptions (e.g. no bare `grep` without Python or PowerShell alternatives).
3. [ ] **Zero Secrets**: Contains zero real tokens, private keys, or credentials.
4. [ ] **Self-Verification**: Passes `python ./tests/validate_skills.py` and `python ./tests/scan_secrets.py`.
5. [ ] **Documentation**: Updated `SKILLS_INDEX.md` with trigger conditions and catalog entry.

---

## 🛠️ Local Development & Testing

```bash
# Run the complete test suite locally
python ./tests/validate_skills.py
python ./tests/scan_secrets.py
python ./tests/test_templates.py
python ./tests/test_hooks.py
python ./tests/test_documentation.py
```
