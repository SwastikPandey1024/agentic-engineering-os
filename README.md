# AgenticOS

<div align="center">

### **The Engineering Operating System for AI Coding Agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org)
[![OS: Windows | macOS | Linux](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-green)]()
[![toolchain: uv](https://img.shields.io/badge/toolchain-uv-purple?logo=astral)](https://github.com/astral-sh/uv)
[![Skills: 30+](https://img.shields.io/badge/Skills-30%2B%20Loaded-emerald)](SKILLS_INDEX.md)
[![CI Quality Gate](https://img.shields.io/badge/CI-Quality%20Gate-emerald)](.github/workflows/ci.yml)

<br/>

> **Turn AI coding from ad-hoc code generation into a repeatable engineering workflow.**

[Origin Story](#-where-agenticos-came-from) • [Quickstart](#-quickstart) • [CLI Tooling](#-developer-cli-reference) • [Architecture](#-architecture) • [Skills Catalog](SKILLS_INDEX.md) • [Case Studies](docs/case-studies/dependency-isolation.md) • [Benchmarks](benchmarks/) • [Contributing](CONTRIBUTING.md)

</div>

---

## 🌱 Where AgenticOS Came From

AgenticOS started as an experiment after learning about the **Agent Skills paradigm**: if an AI coding agent can be equipped with specialized knowledge and repeatable task workflows, could the same principle be applied to software engineering itself?

AI coding assistants are capable of generating syntax rapidly. However, building reliable, long-lived software requires more than raw model intelligence—it requires engineering context, deterministic boundaries, verification discipline, and institutional memory.

What began as an exploration evolved into a cohesive, open-source engineering operating system:
* **Developer CLI (`agentic-os`)**: Lightweight, zero-dependency toolkit for bootstrapping, environment health checks, starter archetypes, and multi-agent IDE integration.
* **30+ Modular Skills** encoding procedural engineering workflows and decision matrices.
* **Deterministic Guardrails & Hooks** that block unisolated or broken environments before commands execute.
* **Project Memory & MCP Schemas** for persisting durable architectural decisions across sessions.
* **Adaptive Documentation** scaling documentation depth to actual project complexity.
* **Automated Verification & Secret Scanners** maintaining a strict zero-secret invariant.
* **5 Production Starter Archetypes** providing clean foundations across services, ML, and fullstack apps.

> *Note: AgenticOS is an independent open-source project inspired by the broader agent skills movement and is not affiliated with, sponsored by, or endorsed by Anthropic.*

---

## ⚡ The Problem: Speed Without Structure

Modern AI coding agents generate code at extraordinary speed. But without explicit engineering standards and guardrails, they behave like hyper-productive junior developers:

* **Fast ≠ Reliable**: They install unpinned packages globally, polluting system environments and breaking neighboring projects.
* **Correct ≠ Maintainable**: They produce 2,000-line monolithic files instead of clean, layered domain boundaries.
* **Passing Tests ≠ Architecture-Compliant**: They bypass dependency injection, hardcode configuration values, and skip error handling.
* **Generated ≠ Production-Ready**: They omit rollback plans, expose sensitive keys in manifests, and hallucinate unbuilt features in documentation.

> **AI coding agents can write code. They still need engineering discipline.**

---

## 💡 The Thesis

> **AgenticOS treats engineering discipline as infrastructure for AI agents.**

The goal of AgenticOS is not to add bureaucracy or slow coding agents down. The goal is to make sound engineering behavior **reusable**, **deterministic**, and **repeatable**—turning ad-hoc prompt reminders into executable system invariants.

---

## 🚀 Quickstart

Get started with AgenticOS in under 60 seconds using the `agentic-os` developer CLI.

### 1. Install AgenticOS
```bash
pip install agentic-os
```

### 2. Option A: Bootstrap into an Existing Project
Initialize invariant rules, 30+ engineering skills, and deterministic hooks in your current workspace:

```bash
# Bootstrap AgenticOS assets into the workspace
agentic-os init

# Verify environment isolation & toolchain health
agentic-os doctor

# Configure AI assistant adapters (Antigravity, Cursor, Copilot, Claude)
agentic-os ide configure --target all
```

### 3. Option B: Scaffold from a Verified Starter Archetype
Create a new, production-ready project pre-configured with virtualenv isolation, tests, and formatting:

```bash
# List available starter templates
agentic-os new --list-templates

# Scaffold a FastAPI microservice with test suite and isolation
agentic-os new my-api-service --template python-service

# Initialize environment and run tests
cd my-api-service
uv venv .venv --python 3.12
uv sync
uv run pytest -v
```

---

## 🛠️ Developer CLI Reference

The `agentic-os` CLI is built using standard-library Python (zero heavy runtime dependencies) and works seamlessly across Windows, macOS, and Linux.

### Commands Overview

| Command | Syntax | Description |
| :--- | :--- | :--- |
| **`doctor`** | `agentic-os doctor [dir] [--strict] [-q]` | Inspects virtual environment, lockfile status, toolchain (`uv`/`poetry`/`npm`), Git status, and rules. |
| **`init`** | `agentic-os init [dir] [-f] [-n] [-q]` | Bootstraps `.agents/skills/`, `hooks/`, and `AGENTS.md` into target directory with conflict safety. |
| **`new`** | `agentic-os new <name> -t <tmpl> [-f] [-n] [--git]` | Scaffolds a new project from a verified starter archetype. |
| **`ide list`** | `agentic-os ide list` | Lists all supported AI coding assistant and IDE integration targets. |
| **`ide configure`**| `agentic-os ide configure -t <target> [dir] [-f] [-n]` | Generates thin configuration adapters for target assistants (`antigravity`, `cursor`, `copilot`, `claude`, `all`). |
| **`ide doctor`** | `agentic-os ide doctor [dir] [-q]` | Diagnoses configured IDE adapters in the current workspace. |

### Operational Safety & Flags

- **Dry-Run Mode (`-n` / `--dry-run`)**: Previews all actions and file operations without writing any bytes to disk (exits with code `0`).
- **Conflict Safety & Force Mode (`-f` / `--force`)**: If an existing file contains conflicting modifications, operations safely halt (exit code `1`) to prevent data loss unless `--force` is explicitly provided.
- **Idempotent Execution**: Running `init`, `configure`, or `new` repeatedly on clean or matching targets automatically skips identical files (`[SKIP] (identical)`) and exits cleanly with code `0`.

---

## 🏛️ Architecture

AgenticOS decouples engineering into clear, specialized operational layers:

```text
                        HUMAN / DEVELOPER
                                │
                                ▼
                       DEVELOPER CLI
                     (agentic-os entrypoint)
                                │
                                ▼
                      ┌──────────────────┐
                      │    AGENTS.md     │
                      │ Always-on rules  │
                      └────────┬─────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
           SKILLS            HOOKS             MCP
         Knowledge        Enforcement      Tools/Memory
         (30+ modules)    (Python engine)  (Graph schemas)
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                           SUBAGENTS
                          Delegation
                               │
                               ▼
                        AI CODING AGENT
                               │
                               ▼
                       VERIFIED SOFTWARE
                               │
                               ▼
                      EMPIRICAL BENCHMARKS
```

### 🔒 Single Source of Truth Model

```text
CLI Layer (agentic-os)
    ↓
Python Standard-Library Engines (doctor, init, templates, ide, guard)
    ↓
Canonical Repository Assets (Single Source of Truth)
    ├── .agents/skills/   (30+ modular domain skills)
    ├── hooks/            (environment guard isolation engine)
    ├── templates/        (5 production starter archetypes)
    └── AGENTS.md         (universal non-negotiable invariants)
```

> **Asset Integrity Invariant**: The 30+ skills, 5 starter templates, and invariant rules are maintained as **canonical filesystem assets**. The CLI dynamically discovers, validates, and packages these assets directly from disk—**they are never duplicated or hardcoded into Python source strings**.

---

## 🔌 AI Agent & IDE Compatibility

AgenticOS provides first-class compatibility across major AI coding assistants and IDEs:

| Assistant / IDE | Integration Mode | Generated Adapter File | Mechanism & Behavior |
| :--- | :--- | :--- | :--- |
| **Google Antigravity (AGY)** | **Native / Zero-config** | `.agents/rules/agentic-os.md` *(Optional)* | Automatically discovers `.agents/skills/` catalog and root `AGENTS.md` rules out-of-the-box. Optional rule adapter provides explicit context pointer. |
| **Cursor IDE** | **Convention-based** | `.cursorrules` | Injects universal invariant rules and `.agents/skills/` trigger catalog into Cursor agent context. |
| **VS Code + GitHub Copilot** | **Convention-based** | `.github/copilot-instructions.md` | Provides workspace-wide instructions for GitHub Copilot Chat in VS Code. |
| **Claude Code (CLI)** | **Convention-based** | `CLAUDE.md` | Directs Claude Code to use `uv run` isolation and references `AGENTS.md` and skills. |
| **OpenAI Codex / Custom Agents** | **Prompt Injection** | Custom Context | Ingest `AGENTS.md` and relevant `SKILL.md` workflows into system prompt context. |

```bash
# Configure all IDE adapters simultaneously
agentic-os ide configure --target all

# Inspect IDE integration status
agentic-os ide doctor
```

---

## 🧩 Core Components

| Component | Location | Role in the System |
| :--- | :--- | :--- |
| **Universal Invariants** | [`AGENTS.md`](AGENTS.md) | High-priority rules: hard environment isolation, inspection before modification, zero-secret leakage. |
| **Modular Skills** | [`.agents/skills/`](.agents/skills/) | 30 domain-specific engineering guides with triggers, checklists, step-by-step workflows, and verification steps. |
| **Deterministic Hooks** | [`hooks/`](hooks/) | Canonical validation engine (`environment_guard.py`) with PowerShell (`.ps1`) and Bash (`.sh`) wrappers. |
| **Developer CLI** | [`src/agentic_os/`](src/agentic_os/) | Python CLI package (`doctor`, `init`, `new`, `ide`) distributed via PyPI / wheels. |
| **Codebase Memory MCP** | [`mcp/`](mcp/) | 7-entity graph schema (`ArchitectureDecision`, `ServiceBoundary`, `RootCauseAnalysis`) for persistent knowledge. |
| **Documentation Orchestrator** | [`.agents/skills/documentation-orchestrator/`](.agents/skills/documentation-orchestrator/SKILL.md) | 5-tier adaptive documentation framework preventing documentation drift. |
| **Testing & Quality** | [`.agents/skills/testing-quality/`](.agents/skills/testing-quality/SKILL.md) | Standardized testing pyramid (Unit, Integration, Regression) with strict execution verification. |
| **Security & Secrets** | [`SECURITY.md`](SECURITY.md) / [`.agents/skills/security-secrets/`](.agents/skills/security-secrets/SKILL.md) | Enforced Zero-Secret Invariant, `.env.example` templates, and automated regex scanning. |
| **Release Engineering** | [`.agents/skills/release-engineering/`](.agents/skills/release-engineering/SKILL.md) | SemVer release gates, changelog automation, and verified rollback runbooks. |
| **Starter Archetypes** | [`templates/`](templates/) | 5 production starter templates pre-configured with `pyproject.toml`, test suites, and strict isolation. |

---

## ⚖️ Before vs. After AgenticOS

| Engineering Dimension | Raw Coding Agent (Before) | AgenticOS Workflow (After) | Evidence / Validation |
| :--- | :--- | :--- | :--- |
| **Environment Management** | Bare `pip install` in global Python. | Strictly isolated `.venv/`, `.python-version` pinned, `uv sync` lockfiles. | Blocked by deterministic `hooks/environment_guard.py` & `agentic-os doctor`. |
| **Cross-Project Isolation** | Upgrading Package A breaks Package B. | Independent lockfiles; no cross-project bleed observed in controlled tests. | Validated in [Case Study](docs/case-studies/dependency-isolation.md). |
| **Architecture Design** | Sprawling monolithic single-file code. | Layered domain boundaries, dependency injection, typed schema validation. | Governed by `code-architecture` skill. |
| **Testing Discipline** | "I wrote the code, it should work." | Mandatory Pytest/Vitest suites executed and verified prior to completion. | Validated via `tests/` self-verification suite. |
| **Security & Secrets** | Real API keys committed in code or `.env`. | Zero-secret invariant, `.env.example` templates, automated regex scanning. | Validated via `tests/scan_secrets.py`. |
| **Documentation** | Stale, unverified, or decorative bloat. | Adaptive 5-tier documentation tied strictly to verified capabilities. | Validated via `tests/test_documentation.py`. |

---

## 🔬 Empirical Evidence: Controlled Dependency Isolation

Can two concurrent projects with conflicting major dependencies (e.g., **Pydantic v2.7.4** vs **Pydantic v1.10.13**) coexist in the same workspace without contaminating each other or modifying global Python?

```text
Project A (Pydantic 2.7.4) ───┐
                               ├── Isolated (.venv / uv.lock) ──► Host Environment Clean
Project B (Pydantic 1.10.13) ─┘
```

In our controlled experiment across Windows, macOS, and Linux:
* **Result**: **8/8 verification metrics passed**. Both projects resolved distinct lockfiles and executed in-environment tests concurrently with zero cross-project pollution observed under the tested conditions.
* Read the full scientific report: **[docs/case-studies/dependency-isolation.md](docs/case-studies/dependency-isolation.md)**.

---

## 📦 Starter Archetypes

AgenticOS includes 5 pre-configured, tested starter templates in [`templates/`](templates/):

1. **[`python-service`](templates/python-service/)**: FastAPI microservice starter with Pydantic v2 validation, health probes, and pytest suite.
2. **[`ai-ml`](templates/ai-ml/)**: Tabular ML pipeline template with Scikit-Learn baselines, leak-free preprocessing, and evaluation tests.
3. **[`rag-llm`](templates/rag-llm/)**: Retrieval-Augmented Generation template with FAISS vector indexing, chunking, and typed query contracts.
4. **[`fullstack`](templates/fullstack/)**: Complete fullstack application with React 19 SPA, Vite, FastAPI backend, and Docker Compose.
5. **[`production-service`](templates/production-service/)**: Enterprise microservice template with OpenTelemetry, structured JSON logging, correlation IDs, and multi-stage Dockerfile.

Scaffold any archetype instantly:
```bash
agentic-os new my-service --template production-service
```

---

## 🐕 Dogfooding & Repository Verification

AgenticOS is built and verified using its own engineering principles. Every pull request executes a self-verification test suite:

```bash
# Run CLI and repository self-verification suite
py ./tests/test_cli.py              # Validates CLI parser, doctor, init, template generator, and IDE adapters
py ./tests/validate_skills.py       # Validates YAML frontmatter, triggers & 6 Core Questions for all 30 skills
py ./tests/scan_secrets.py          # Scans repository for secrets, credentials, and sensitive tokens
py ./tests/test_templates.py        # Compiles all template code and validates test suite completeness
py ./tests/test_hooks.py            # Tests environment guard engine against unisolated and isolated projects
py ./tests/test_documentation.py    # Asserts 100% resolution of relative documentation cross-references
```

---

## 🛣️ Roadmap

* **v1.0 (Foundation — Released)**: 30+ Modular Skills, Deterministic Hooks, MCP memory layer, 5 templates, multi-OS support, and self-verification suite.
* **v1.1 (Developer Experience — Current)**: Developer CLI (`agentic-os init`, `doctor`, `new`, `ide`), automated archetype generator, and multi-agent IDE integration layer.
* **v1.2 (Evidence & Benchmarks — Upcoming)**: Automated `AgenticEval` benchmark harness, empirical quality scorecards, and comparative evaluation suites.
* **v2.0 (Ecosystem — Planned)**: Public skill registry, community plugins, multi-agent coordination protocols, and custom organization profiles.

See **[ROADMAP.md](ROADMAP.md)** for detailed milestone tracking.

---

## 🤝 Contributing & Community

We welcome contributions from the community! Please review:
* **[CONTRIBUTING.md](CONTRIBUTING.md)** for our 6 Core Questions skill authoring standard.
* **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** for our community standards.
* **[SECURITY.md](SECURITY.md)** for our vulnerability disclosure policy and Zero-Secret Invariant.

---

## 📄 License

AgenticOS is open-source software licensed under the **[MIT License](LICENSE)**.

---

<div align="center">

*AI agents are getting better at writing software. AgenticOS explores what happens when we give them an engineering system to work within.*

**Build with your agent. Engineer with AgenticOS.**

</div>
