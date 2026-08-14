# Core Agent Engineering Rules (AGENTS.md) - V2

Universal, non-negotiable invariant principles governing all AI-assisted software development in this workspace.

---

## 1. Universal Engineering Invariants

### 1.1 Environment Isolation (Hard Requirement)
* **Never install project dependencies globally**. All development must occur inside isolated project virtual environments (`.venv/` or local `node_modules`).
* **Always establish the project environment BEFORE installing dependencies**. Create `.venv` first, then run package manager commands.
* **Never use bare `pip install`** against system Python. Always use managed project tools (`uv add`, `uv sync`, `uv run` or activated `.venv/bin/pip`).
* **Never mix dependency managers** without explicit justification (e.g. do not mix `poetry` and `conda` and `pip` concurrently in one repo).
* **Keep `.venv/` strictly out of Git**. Never commit virtual environments.

### 1.2 Codebase Memory & Durable Knowledge
* **Consult project memory before significant decisions**: Check existing Architecture Decision Records (ADRs), codebase memory graph, or project logs before modifying core architecture, changing major dependencies, altering database schemas, or modifying deployment targets.
* **Record durable decisions**: Capture non-obvious architecture choices, resolved root causes, and rejected alternatives in memory/ADRs immediately after verification.
* **Never store secrets in memory**: API keys, credentials, tokens, passwords, and sensitive personal information must NEVER be written to codebase memory or ADRs.

### 1.3 Inspect Before Modifying
* **Never modify code without reading it first**: Inspect existing files, module boundaries, type contracts, and runtime configurations before generating edits.
* **Reuse existing abstractions**: Search the codebase for existing helpers, schemas, and utilities before creating new ones.

### 1.4 Minimal, Surgical Diffs
* Make the smallest possible change that correctly fulfills the requirement.
* Preserve existing formatting, unrelated comments, docstrings, and code style.
* Preserve backward compatibility for existing APIs, interfaces, and database records unless an intentional breaking change is explicitly mandated.

### 1.5 Truthful & Verified Documentation
* **Documentation must reflect verified reality**: Never document an intended or unbuilt feature as if it were already implemented.
* **Adaptive documentation depth**: Scale documentation appropriately to project complexity (Utility vs ML Platform vs Fullstack vs Enterprise Production).

### 1.6 Verification Before Completion
* **Never claim tests were run unless they were actually executed**: Zero hallucination of test results or syntax validity.
* **Never claim deployment succeeded without live verification**: Always probe health endpoints and verify 200 OK status on live URLs when available.
* A task is ONLY complete when code is implemented, automated tests pass, linters pass, and documentation is updated.

### 1.7 Security & Least Privilege
* **Zero secret leakage**: Never commit `.env`, credentials, tokens, or private keys to version control.
* Always maintain a sanitized `.env.example`.
* Inspect `git diff` before staging and committing.
* Never disable security checks, authentication guards, or tests to make a build pass.

---

## 2. Decision Hierarchy

When resolving conflicts or choosing implementation strategies:

```text
1. Universal Engineering Rules (AGENTS.md) [Highest Priority Invariants]
2. Project Memory & Architecture Decision Records (ADRs / MCP Memory)
3. Specialized Task Skills (.agents/skills/*)
4. Existing Project Conventions & Local Utilities
5. Language & Framework Idioms (PEP 8, Modern TypeScript, FastAPI, React 19)
6. General Industry Best Practices [Lowest Priority]
```

---

## 3. Operational Discipline & Anti-Looping

* **Declare Uncertainty**: If requirements, third-party APIs, or environment states are ambiguous, state the uncertainty explicitly and present concrete options rather than making assumptions.
* **Anti-Looping Gate**: If a command, build, or test fails twice with the same error, **STOP**. Do not retry a 3rd time without altering the diagnosis or modifying inputs.
* **Explain Architectural Rationale**: Focus explanations on trade-offs, design choices, and non-obvious decisions rather than narrating trivial code syntax.
