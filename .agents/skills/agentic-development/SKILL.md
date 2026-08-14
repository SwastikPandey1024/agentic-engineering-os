---
name: agentic-development
description: The master meta-skill governing the 8-phase AI coding agent lifecycle, tool execution heuristics, zero-assumption verification, and anti-looping discipline.
---

# Agentic Development (Master Meta-Skill)

## 1. When Should I Use This?

Use this skill continuously across **EVERY** AI-assisted software development task.

This is the central operating discipline for the coding agent. It dictates how the agent investigates codebases, structures plans, writes surgical edits, verifies execution, declares uncertainty, and achieves reliable results without human intervention loops.

---

## 2. What Should I Inspect First?

Before taking any code-modifying action:
1. **Workspace Architecture & Roots**: Inspect directory tree, primary languages, frameworks, package managers, and configuration files.
2. **Universal Rules (`AGENTS.md`)**: Re-align on non-negotiable core invariants.
3. **Active Skills (`.agents/skills/`)**: Identify which specialized skills apply to the current task.
4. **Existing Code & Patterns**: Search for existing utilities, schemas, and abstractions before writing new code.
5. **Git Working Tree**: Verify working tree state (`git status`, active branch).

---

## 3. What Workflow Should I Follow?

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. UNDERSTAND: Parse user intent, extract hard constraints  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. INSPECT: Read files, inspect architecture, check tests   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. PLAN: Formulate minimal, non-breaking implementation path│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. IMPLEMENT: Surgical edits, reuse existing utilities      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 5. TEST: Execute unit/integration/smoke tests               │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 6. VERIFY: Confirm real runtime behavior with zero guessing │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 7. REVIEW: Inspect git diff, verify no unintended changes   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 8. DOCUMENT: Synchronize README, ADRs, schemas, logs        │
└─────────────────────────────────────────────────────────────┘
```

### The 8 Phases in Detail

1. **UNDERSTAND**: Clarify requirements. If requirements are ambiguous, declare uncertainty and present structured options rather than making random assumptions.
2. **INSPECT**: Read relevant source code, manifests, and test fixtures using filesystem/graph tools. Never edit a file without reading it first.
3. **PLAN**: Choose the smallest safe change. Verify how new code will interface with existing modules.
4. **IMPLEMENT**: Write modular, typed code adhering to existing code conventions. Preserve comments and existing style.
5. **TEST**: Run existing tests first to catch pre-existing breakages; write new tests covering the changed code.
6. **VERIFY**: Run real automated tests, linter checks, and runtime verification.
7. **REVIEW**: Review the exact `git diff`. Verify no secrets, temporary debug code, or extraneous files were touched.
8. **DOCUMENT**: Update corresponding documentation, schemas, or changelogs.

---

## 4. What Decisions Should I Make?

| Agent Decision Heuristic | Rule |
| :--- | :--- |
| **Tool Selection** | Use specialized MCP/graph tools for code discovery; use native edit tools for surgical changes; use terminal commands for test execution and linting. |
| **Anti-Looping Protocol** | If a command or edit fails twice with the same error, **STOP**. Do not retry a 3rd time. Step back, re-read the error, check assumptions, and re-diagnose. |
| **Declaration of Uncertainty** | If a third-party API behavior, database state, or requirement is unverified, state: *"I cannot verify X directly because Y; proceeding with assumption Z based on standard pattern W."* |
| **Definition of Done** | A task is DONE when and only when: (1) code is implemented, (2) automated tests pass, (3) linter/type checks pass, and (4) documentation is updated. |

---

## 5. What Should I Avoid?

* **NEVER blind-rewrite large sections of working code**: Make minimal, targeted diffs.
* **NEVER claim code was tested when it was not executed**: Zero hallucination of test results.
* **NEVER install dependencies globally**: Always use local project virtual environments.
* **NEVER commit secrets, tokens, or `.env` files**.

---

## 6. How Should I Verify Success?

```bash
# Standard 4-Point Agent Completion Gate
# 1. Formatting and linting
ruff check . && ruff format --check .

# 2. Type checking
mypy app/ # or npm run type-check

# 3. Test execution
pytest -v

# 4. Clean git diff audit
git status
git diff --stat
```
