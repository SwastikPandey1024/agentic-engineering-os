---
name: dependency-management
description: Safe addition, pinning, upgrading, and conflict diagnosis for Python and JavaScript dependencies without version thrashing.
---

# Dependency Management Skill

## 1. When Should I Use This?

Use this skill when:
* Adding a new third-party library to a Python or JavaScript project.
* Resolving package version conflicts or peer dependency errors (`pip`, `uv`, `npm`, `pnpm`).
* Upgrading existing dependencies safely.
* Distinguishing between runtime dependencies and development/test dependencies.

Do NOT use this skill for initial environment bootstrapping (use `python-environment`).

---

## 2. What Should I Inspect First?

1. **Manifest Files**:
   * Python: `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `uv.lock`, `poetry.lock`.
   * Node: `package.json`, `package-lock.json`.
2. **Current Constraints & Transitive Trees**:
   * Check if the desired library is already pulled in as a sub-dependency (`uv pip tree` or `npm ls <pkg>`).
3. **Runtime Compatibility**: Check current Python version (e.g. 3.11 vs 3.12) or Node engine version before selecting packages with strict C-extensions or compilation requirements (e.g. `pydantic-core`, `paddlepaddle`, `faiss-cpu`, `tensorflow`).

---

## 3. What Workflow Should I Follow?

```text
Inspect Manifest & Lockfile
           ↓
Check if package already exists indirectly
           ↓
Determine Compatibility with Python / Node version
           ↓
Make the SMALLEST safe change in manifest
           ↓
Update Lockfile (uv lock / npm install)
           ↓
Run Import / Smoke Test Checks
           ↓
Run Full Test Suite to Catch Breaking Changes
```

### Python Dependency Protocol (`pyproject.toml`)

```toml
# pyproject.toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110.0,<1.0.0",
    "pydantic>=2.7.0,<3.0.0",
    "pydantic-settings>=2.2.0",
    "sqlalchemy>=2.0.28",
    "alembic>=1.13.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.3.0",
    "httpx>=0.27.0",
]
```

```bash
# Add a single new dependency cleanly with uv
uv add "scikit-learn>=1.4.0"
# Or for development
uv add --dev "pytest-cov>=5.0.0"
```

### JavaScript / Node Dependency Protocol (`package.json`)

```bash
# Add runtime dependency
npm install @tanstack/react-query@^5.0.0

# Add dev dependency
npm install --save-dev @types/node@^20.0.0
```

---

## 4. What Decisions Should I Make?

| Situation | Decision Rule |
| :--- | :--- |
| **Adding a lightweight helper function** | Prefer writing a small local utility in `utils/` instead of pulling an entire heavy external package. |
| **Version Pinning Strategy** | Use compatible release operator (`~=` or `>=X.Y.Z,<(X+1).0.0`) for libraries; exact pin (`==X.Y.Z`) for critical ML framework combinations (e.g. `tensorflow==2.16.1` + `keras==3.3.3`). |
| **Resolving Conflicts** | Identify the exact conflicting constraint using `uv pip tree` or `pip check`. Never indiscriminately update 10 packages at once. |
| **Dev vs Runtime** | Test runners, linters, formatters, type stubs (`@types/*`, `mypy`, `ruff`, `pytest`) must strictly reside in dev-dependencies. |

---

## 5. What Should I Avoid?

* **NEVER solve conflicts by random version bumping**: Pinpointing the root conflict is mandatory.
* **NEVER add unpinned unbounded dependencies**: Avoid bare package names with no constraints (`requests` vs `requests>=2.31.0,<3.0.0`).
* **NEVER edit `uv.lock` or `package-lock.json` manually**: Always let the package manager generate the lockfile.
* **NEVER use multiple package managers in the same project**: Avoid mixing `pip`, `poetry`, and `conda` concurrently in a single repo.

---

## 6. How Should I Verify Success?

```bash
# 1. Python dependency check
python -m pip check

# 2. Test import of newly added package
python -c "import <new_package>; print('<new_package> imported successfully')"

# 3. Node dependency audit
npm audit --audit-level=high

# 4. Run test suite to verify no transitive breakages
pytest -v
```
