---
name: project-bootstrap
description: Full 17-step lifecycle orchestrator for new and existing projects, environment initialization, stack selection, baseline documentation, and release readiness.
---

# Project Bootstrap Skill (V2 Lifecycle Orchestrator)

## 1. When Should I Use This?

Use this skill when:
* Bootstrapping any brand-new software project, repository, microservice, or system from scratch.
* Orchestrating the end-to-end initialization workflow across architecture, environment, tooling, documentation, and security.
* Restructuring or standardizing an existing disorganized codebase into a production-grade system.

---

## 2. What Should I Inspect First?

1. **Target Domain & Archetype**:
   * Python Backend API (FastAPI)
   * Fullstack Application (React 19 + TypeScript + FastAPI/Node)
   * Machine Learning / Deep Learning Research Platform
   * Time-Series / Data Engineering Platform
   * Small CLI / Automation Script
2. **Runtime & Hardware Constraints**: Python version (>=3.11/3.12), Node.js (>=20), GPU availability (`nvidia-smi`), target hosting platform.
3. **Workspace State**: Ensure clean directory tree before initializing files.

---

## 3. What Workflow Should I Follow?

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. CLASSIFY PROJECT (Utility vs ML vs Fullstack vs Prod)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. SELECT TECH STACK (FastAPI, React, PostgreSQL, uv, etc.) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. ENVIRONMENT SETUP (Create .venv FIRST before packages)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. DEPENDENCY SETUP (pyproject.toml, uv.lock, package.json) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 5. REPOSITORY STRUCTURE (Standard layered directories)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 6. CONFIGURE AGENTS.md & RELEVANT SKILLS (.agents/skills/)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 7. CHECK MCP AVAILABILITY (Memory, Database, DevTools)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 8. DOCUMENTATION PLAN (Adaptive minimum documentation suite)│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 9. TESTING PLAN (Pytest harness, conftest.py, test fixtures)│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 10. SECURITY BASELINE (.env.example, SecretStr, .gitignore) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 11. OBSERVABILITY BASELINE (Structured JSON logs, req IDs)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 12. IMPLEMENTATION (Domain logic, routes, schemas, models)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 13. VERIFICATION (Unit, integration, and linting suites)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 14. DOCUMENTATION EXECUTION (README, ARCHITECTURE, ADRs)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 15. RELEASE READINESS (SemVer, Dockerfile, CI workflow)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Execution Steps

### Step 1: Classify & Select Stack
Determine the project archetype and lock in the toolchain:
* **Python API**: FastAPI + Pydantic v2 + SQLAlchemy/Prisma + `uv`
* **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS + TanStack Query
* **ML / Data**: Scikit-Learn / XGBoost / PyTorch / Pandas / Parquet

### Step 2: Environment Setup (CRITICAL: Before Dependencies)
```bash
# 1. Pin Python version
echo "3.12" > .python-version

# 2. Create isolated virtual environment
uv venv .venv --python 3.12

# 3. Configure IDE interpreter
mkdir -p .vscode
cat << 'EOF' > .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic"
}
EOF
```

### Step 3: Dependency Setup & Manifests
Create `pyproject.toml` with separate runtime and dev dependencies:
```toml
[project]
name = "my-service"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.110.0,<1.0.0",
    "pydantic>=2.7.0,<3.0.0",
    "pydantic-settings>=2.2.0",
    "uvicorn>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.3.0",
    "mypy>=1.9.0",
    "httpx>=0.27.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

```bash
# Sync dependencies and generate lockfile
uv sync
```

### Step 4: Repository Layout & Git Hygiene
Create directory tree and populate `.gitignore`:
```bash
mkdir -p app/{api/v1/{routes,schemas,dependencies},core,services,models,utils} tests/{unit,integration} docs/decisions
```

```text
# .gitignore
.venv/
__pycache__/
*.pyc
.env
.env.local
.pytest_cache/
.coverage
dist/
build/
datasets/raw/*
!datasets/raw/.gitkeep
```

### Step 5: Universal Governance & Quality Baselines
1. Copy or symlink `AGENTS.md` and `.agents/skills/`.
2. Generate `.env.example` with sanitized placeholder keys.
3. Create `tests/conftest.py` with FastAPI `TestClient` fixture.
4. Set up structured logging with correlation IDs in `app/core/logging.py`.
5. Set up health probe `/api/v1/health` in `app/main.py`.

---

## 4. What Decisions Should I Make?

| Decision Point | Standard Recommendation |
| :--- | :--- |
| **Virtual Environment Creation** | ALWAYS create `.venv/` BEFORE running any `pip` or `uv add` commands. |
| **Documentation Scope** | Determine minimum document suite using `documentation-orchestrator`. |
| **Package Manager** | Default to `uv` for new Python projects. |

---

## 5. What Should I Avoid?

* **NEVER install dependencies before creating `.venv/`**: Environment initialization must precede package installation.
* **NEVER commit `.venv/` or raw datasets without `.gitkeep`**: Ensure `.gitignore` is populated immediately.
* **NEVER create monolith god-files**: Split endpoints, services, schemas, and models from day one.
* **NEVER omit `.env.example`**: Always maintain sanitized configuration templates.

---

## 6. How Should I Verify Success?

```bash
# 1. Confirm environment isolation
python -c "import sys; assert '.venv' in sys.executable, 'CRITICAL: Global python detected!'"

# 2. Run initial test suite
uv run pytest -v

# 3. Check linting and formatting
uv run ruff check .
uv run ruff format --check .

# 4. Check git status
git status
```
