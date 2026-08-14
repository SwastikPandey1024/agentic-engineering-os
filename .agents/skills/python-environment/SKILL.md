---
name: python-environment
description: Virtual environment creation, Python version pinning, and environment reproducibility using uv, venv, or Conda without global package pollution.
---

# Python Environment Skill

## 1. When Should I Use This?

Use this skill when:
* Creating, configuring, or repairing a Python virtual environment.
* Choosing between `uv`, `venv`, and `conda` for a new or existing project.
* Verifying Python runtime compatibility and lockfile state.
* Resolving environment isolation failures or "command not found" interpreter issues.

Do NOT use this skill for general package dependency upgrades (use `dependency-management`).

---

## 2. What Should I Inspect First?

1. **Active Python Interpreter**: Run `python --version` and `which python` / `where python`.
2. **Existing Environment Markers**:
   * Look for `.venv/`, `venv/`, `.python-version`, `pyproject.toml`, `uv.lock`, `requirements.txt`, `Pipfile`, `environment.yml`.
3. **Environment Manager**: Detect whether the project already uses `uv`, `poetry`, `conda`, or standard `venv`.
4. **Platform & Architecture**: Windows vs Linux/macOS, architecture (`x86_64` vs `arm64`), and CUDA availability (`nvidia-smi` or `torch.cuda.is_available()`).

---

## 3. What Workflow Should I Follow?

```text
Inspect Existing Environment Artifacts
                 ↓
Is this a new project or already using uv?
 ├── YES → Modern uv Workflow (uv venv, uv pip / uv sync)
 └── NO  → Respect Existing Toolchain (venv, conda, pip)
                 ↓
Pin Python Version (.python-version / pyproject.toml)
                 ↓
Create Isolated Virtual Environment in .venv/
                 ↓
Verify Interpreter Path & Isolation
```

### Modern Standard Workflow (`uv`)

```bash
# 1. Pin Python version
echo "3.12" > .python-version

# 2. Create isolated virtual environment
uv venv .venv --python 3.12

# 3. Synchronize / Install dependencies deterministically
uv sync

# 4. Execute commands directly inside .venv (Universal Cross-Platform: No activation needed!)
uv run python app/main.py
uv run pytest -v

# (Optional) Manual shell activation if desired:
# Windows (PowerShell): .\.venv\Scripts\Activate.ps1
# Linux / macOS:        source .venv/bin/activate
```

### Fallback Workflow A: Standard Python `venv`

```bash
# 1. Create venv
python -m venv .venv

# 2. Upgrade pip inside venv
.venv/Scripts/python -m pip install --upgrade pip setuptools wheel

# 3. Install requirements
.venv/Scripts/python -m pip install -r requirements.txt
```

### Fallback Workflow B: Conda (for specialized CUDA / legacy C-extensions)

```bash
# 1. Create conda env
conda create -n my-project-env python=3.11 -y

# 2. Activate conda env
conda activate my-project-env

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 4. What Decisions Should I Make?

| Project Scenario | Recommended Environment Tool | Rationale |
| :--- | :--- | :--- |
| **New Python Project** | `uv` (`.venv/` + `uv.lock`) | 10-100x faster resolution, strict lockfile reproducibility, native multi-Python management. |
| **Existing `pyproject.toml` / `requirements.txt`** | Maintain existing tool (`uv` or `venv`) | Avoid gratuitous churn unless requested by user. |
| **GPU / DICOM / C++ extensions (e.g. MedVision/CUDA)** | Virtualenv with pinned wheels or Conda | Ensures binary wheel compatibility with host CUDA drivers. |
| **Docker Container** | `uv pip install --system` or slim `python -m venv` | Reduces image layer size and runtime overhead. |

---

## 5. What Should I Avoid?

* **NEVER install packages globally**: Never run `pip install <package>` without an active virtual environment.
* **NEVER commit `.venv/` to Git**: Always ensure `.venv/` and `venv/` are present in `.gitignore`.
* **NEVER hardcode machine-specific paths**: Avoid relying on absolute user home paths in scripts or configurations.
* **NEVER force-migrate a working project**: Do not delete existing `conda` or `poetry` configurations to force `uv` without explicit user intent.

---

## 6. How Should I Verify Success?

Run these verification commands to ensure complete isolation:

```bash
# 1. Confirm python points to the local virtual environment
python -c "import sys; print(sys.executable); assert '.venv' in sys.executable or 'my-project-env' in sys.executable, 'Global Python detected!'"

# 2. Confirm site-packages location is local
python -c "import site; print(site.getsitepackages())"

# 3. Verify core imports succeed
python -c "import pytest, ruff; print('Environment tooling verified')"
```
