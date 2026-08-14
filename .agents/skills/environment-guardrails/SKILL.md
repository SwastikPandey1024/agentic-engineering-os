---
name: environment-guardrails
description: Hard environment isolation, Python version pinning, uv package management, and migration/fallback strategies for pip, venv, conda, poetry, and pipenv.
---

# Environment Guardrails Skill

## 1. When Should I Use This?

Use this skill when:
* Bootstrapping any new Python project or working in an existing repository.
* Setting up, verifying, or repairing virtual environment isolation (`.venv/`).
* Enforcing package management standards (`uv` by default; preserving `conda`/`poetry`/`pip` when mature).
* Diagnosing global package pollution, interpreter mismatches, or lockfile desynchronization.
* Migrating legacy `requirements.txt` or `Pipfile` projects to modern `pyproject.toml` + `uv.lock`.

---

## 2. What Should I Inspect First?

1. **Python Version Requirements**:
   * Inspect `.python-version`, `pyproject.toml` (`requires-python = ">=3.11"`), or `runtime.txt`.
2. **Existing Package Manager & Toolchain**:
   * Look for `uv.lock`, `poetry.lock`, `Pipfile.lock`, `environment.yml`, `requirements.txt`, `pyproject.toml`.
3. **Active Interpreter Location**:
   * Run `python -c "import sys; print(sys.executable)"` to confirm if it points inside `.venv/` or system Python.
4. **IDE Interpreter Settings**:
   * Inspect `.vscode/settings.json` for `"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"` (or `Scripts/python.exe`).

---

## 3. What Workflow Should I Follow?

```text
Detect Python Version Requirements (.python-version, pyproject.toml)
                       ↓
Detect Existing Package Manager:
 ├── New Project / Modern Setup   → Modern uv Workflow
 ├── Mature Poetry / Conda / Venv → Preserve Existing Toolchain
 └── Legacy requirements.txt      → Isolate with venv/uv without breaking
                       ↓
Create Project-Local Virtual Environment (.venv/) BEFORE Dependency Installs
                       ↓
Pin Python Version (.python-version & pyproject.toml)
                       ↓
Synchronize Dependencies via Lockfile (uv sync / uv.lock)
                       ↓
Separate Runtime Dependencies from Dev Dependencies ([project.optional-dependencies])
                       ↓
Configure IDE & Git (.gitignore contains .venv, IDE points to .venv)
                       ↓
Verify Environment Isolation
```

### The 18-Step Standard Environment Protocol

1. **Detect Version**: Read target Python version (`3.11`, `3.12`).
2. **Detect Toolchain**: Check for existing lockfiles (`uv.lock`, `poetry.lock`).
3. **Respect Mature Projects**: If a project heavily relies on Poetry or Conda, use that toolchain unless requested to migrate.
4. **Default to `uv` for New Projects**: `uv` is the standard modern fast package manager.
5. **Create Project-Local `.venv`**: Always create `.venv` directly in the project root.
6. **Create or Maintain `pyproject.toml`**: Single source of truth for build backend, metadata, and dependencies.
7. **Pin Python Version**: Write exact minor version to `.python-version` (e.g. `3.12`).
8. **Maintain Lockfile**: Keep `uv.lock` synchronized and committed to version control.
9. **Separate Dependencies**: Put testing, linting, and formatting tools under `[project.optional-dependencies] dev = [...]`.
10. **Never Install Globally**: Reject any bare `pip install` targeting `/usr/bin/python` or global AppData.
11. **Never Mix Project Dependencies**: Each project must have its own dedicated `.venv`.
12. **Never Use Unmanaged `pip`**: Use `uv add` or `.venv/bin/pip`.
13. **Use `uv add` for Project Dependencies**: Automatically updates `pyproject.toml` and `uv.lock`.
14. **Use `uv sync` for Synchronization**: Synchronizes environment state cleanly to match lockfile.
15. **Use `uv run` for Command Execution**: Runs test runners and scripts inside the managed environment automatically.
16. **Exclude `.venv` from Git**: Ensure `.venv` is in `.gitignore`.
17. **Verify IDE Interpreter**: Configure `.vscode/settings.json` to point to `.venv`.
18. **Document Setup in README**: Provide copy-pasteable environment initialization commands in `README.md`.

---

### Migration & Fallback Protocols

#### Protocol A: Modern `uv` Workflow (Recommended)
```bash
# 1. Pin version
echo "3.12" > .python-version

# 2. Create isolated venv
uv venv .venv --python 3.12

# 3. Add dependencies
uv add "fastapi>=0.110.0" "pydantic>=2.7.0"
uv add --dev "pytest>=8.0.0" "ruff>=0.3.0"

# 4. Synchronize environment
uv sync

# 5. Run commands in environment
uv run pytest -v
```

#### Protocol B: Existing `requirements.txt` / Standard `venv`
```bash
# 1. Create standard venv
python -m venv .venv

# 2. Activate
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# 3. Install requirements
pip install --upgrade pip
pip install -r requirements.txt
if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
```

#### Protocol C: Existing `Conda` Environment
```bash
# 1. Create environment from environment.yml or version
conda env create -f environment.yml -p ./.conda_env || conda create -n my_env python=3.11 -y

# 2. Activate
conda activate my_env
```

#### Protocol D: Existing `Poetry` Project
```bash
# 1. Configure poetry to create .venv inside project root
poetry config virtualenvs.in-project true

# 2. Install and lock
poetry install
poetry run pytest
```

---

## 4. What Decisions Should I Make?

| Scenario | Decision Rule |
| :--- | :--- |
| **New Python Project** | Always use `uv` + `pyproject.toml` + `uv.lock`. |
| **Existing Stable Poetry / Conda** | Keep existing toolchain. Do not force-migrate without user request. |
| **Legacy `requirements.txt`** | If simple, keep `requirements.txt` or migrate to `pyproject.toml` if adding modern tooling like Ruff/Pytest. |
| **Docker Container Build** | Use `uv pip install --system -r requirements.txt` or multi-stage build with `.venv`. |

---

## 5. What Should I Avoid?

* **NEVER run `pip install` without an active `.venv`**: This pollutes system libraries.
* **NEVER delete an existing `poetry.lock` or `Pipfile.lock` to force `uv`** without user consent.
* **NEVER commit `.venv/` or `.conda/` folders to Git**.
* **NEVER use unpinned dependencies without bounds** (e.g. use `pydantic>=2.7.0,<3.0.0`, not `pydantic`).

---

## 6. How Should I Verify Success?

```bash
# 1. Verify python points to local .venv
python -c "import sys; print(sys.executable); assert '.venv' in sys.executable or 'conda' in sys.executable, 'CRITICAL: Running in Global Python!'"

# 2. Verify dependency resolution and lockfile consistency
uv lock --check || pip check

# 3. Verify tool execution inside environment
uv run pytest --version || .venv/bin/pytest --version
```
