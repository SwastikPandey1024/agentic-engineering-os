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

> **AI coding agents can write code. They still need engineering discipline.**

AgenticOS equips coding agents with **reusable engineering knowledge**, **deterministic guardrails**, **codebase memory integration**, **adaptive documentation**, and **production verification workflows**.

[Quickstart](#-quickstart) • [Architecture](#-architecture) • [Skills Catalog](SKILLS_INDEX.md) • [Case Studies](docs/case-studies/dependency-isolation.md) • [Benchmarks](benchmarks/) • [Contributing](CONTRIBUTING.md)

</div>

---

## ⚡ The Junior Agent Problem

Modern AI coding agents generate code at extraordinary speed. But without explicit engineering standards and guardrails, they behave like hyper-productive junior developers:

* **Fast ≠ Reliable**: They install unpinned packages globally, corrupting system environments.
* **Correct ≠ Maintainable**: They write 2,000-line monoliths instead of clean, layered services.
* **Passing Tests ≠ Architecture-Compliant**: They bypass dependency injection and hardcode configuration.
* **Generated ≠ Production-Ready**: They forget rollback runbooks, leak secrets, and hallucinate unbuilt features in documentation.

**AgenticOS bridges this gap by shifting engineering discipline from repetitive human prompt reminders into an executable operating system.**

---

## 🏛️ Architecture

AgenticOS decouples engineering into clear, specialized operational layers:

```text
                       HUMAN / DEVELOPER
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

### Core Separation of Concerns
* 🧠 **Skills** (`.agents/skills/`): Procedural engineering knowledge and decision matrices.
* 🛡️ **Hooks** (`hooks/`): Deterministic validation scripts that block unisolated or broken operations.
* 🧩 **MCP Layer** (`mcp/`): Structured schemas and protocols connecting project memory tools.
* 🤖 **Subagents**: Isolated context sandboxes for complex, multi-phase tasks.

---

## ⚖️ Before vs. After AgenticOS

| Engineering Dimension | Raw Coding Agent (Before) | AgenticOS Workflow (After) |
| :--- | :--- | :--- |
| **Environment Management** | Bare `pip install` in global Python. | Strictly isolated `.venv/`, `.python-version` pinned, `uv sync` lockfiles. |
| **Cross-Project Isolation** | Upgrading Package A breaks Package B. | Guaranteed zero cross-project bleed ([Validated in Case Study](docs/case-studies/dependency-isolation.md)). |
| **Architecture Design** | Sprawling monolithic god-files. | Layered domain boundaries, dependency injection, Pydantic v2 schemas. |
| **Testing Discipline** | "I wrote the code, it should work." | Mandatory Pytest/Vitest suites executed and verified before completion. |
| **Security & Secrets** | Secrets committed in code or `.env`. | Zero-secret invariant, `.env.example` templates, automated regex scanners. |
| **Documentation** | Stale, unverified, or decorative bloat. | Adaptive 5-tier documentation tied strictly to verified capabilities. |

---

## 🔬 Empirical Case Study: Validated Dependency Isolation

Can two projects with conflicting major dependencies (e.g. **Pydantic v2.7.4** vs **Pydantic v1.10.13**) coexist in the same workspace without contaminating each other?

```text
Project A (Pydantic 2.7.4) ───┐
                              ├── 100% Isolated (0 Bleed) ──► Global Python Clean
Project B (Pydantic 1.10.13) ─┘
```

In our controlled experiment across Windows, macOS, and Linux:
* **Result**: **8/8 verification metrics passed**. Both projects resolved distinct lockfiles and executed in-environment tests concurrently with zero cross-project pollution.
* Read the full scientific report: **[docs/case-studies/dependency-isolation.md](docs/case-studies/dependency-isolation.md)**.

---

## 🚀 Quickstart

### Option 1: Integrate into an Existing Project
Copy the foundational invariants, skills, and deterministic hooks directly into your workspace:

```bash
# Windows PowerShell
Copy-Item -Recurse "path/to/agentic-engineering-os/.agents" "./"
Copy-Item -Recurse "path/to/agentic-engineering-os/hooks" "./"
Copy-Item "path/to/agentic-engineering-os/AGENTS.md" "./"

# Linux / macOS
cp -r path/to/agentic-engineering-os/.agents ./
cp -r path/to/agentic-engineering-os/hooks ./
cp path/to/agentic-engineering-os/AGENTS.md ./
```

### Option 2: Bootstrap from a Production Template
Clone one of our 5 pre-configured starter archetypes:

```bash
# Copy template (e.g., FastAPI Python Service)
cp -r agentic-engineering-os/templates/python-service my-new-api
cd my-new-api

# Initialize environment with uv
uv venv .venv --python 3.12
uv sync
uv run pytest -v
```

---

## 🔌 Supported AI Agents & IDEs

| Assistant / IDE | Integration Method | Configuration Location |
| :--- | :--- | :--- |
| **Google Antigravity (AGY)** | Native Discovery | Automatically loads `.agents/skills/` and `AGENTS.md`. |
| **Cursor IDE** | Rules System | Add `.cursorrules` or symlink into `.cursor/rules/`. |
| **VS Code + GitHub Copilot** | Workspace Instructions | Reference `AGENTS.md` in `.github/copilot-instructions.md`. |
| **Claude Code (CLI)** | System Context | Symlink `AGENTS.md` to `CLAUDE.md` in repository root. |
| **OpenAI Codex / Custom** | Prompt Injection | Ingest `AGENTS.md` and required `SKILL.md` files as system context. |

---

## 🐕 Built with AgenticOS

> **DOGFOODED FROM DAY ONE**:  
> AgenticOS was designed, structured, tested, and validated using its own 30+ skills, deterministic environment guards, and documentation orchestrator. The repository runs its own [self-verification test suite](tests/) on every pull request.

---

## 🛣️ Roadmap

* **v1.0 (Foundation)**: 30+ Skills, Deterministic Hooks, MCP memory layer, 5 templates, multi-OS support.
* **v1.1 (Developer Experience)**: Standalone CLI (`agentic-os init`, `agentic-os doctor`), automated pre-commit integration.
* **v1.2 (Evidence & Benchmarks)**: AgenticEval benchmark suite, agentic quality scorecards.
* **v2.0 (Ecosystem)**: Public skill registry, community plugins, custom organization profiles.

See **[ROADMAP.md](ROADMAP.md)** for detailed milestone tracking.

---

## 🤝 Contributing & Community

We welcome community contributions! Please review:
* **[CONTRIBUTING.md](CONTRIBUTING.md)** for our 6 Core Questions skill authoring standard.
* **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** for our community standards.
* **[SECURITY.md](SECURITY.md)** for vulnerability reporting.

---

## 📄 License

AgenticOS is open-source software licensed under the **[MIT License](LICENSE)**.
