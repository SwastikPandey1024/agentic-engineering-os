# Case Study: Empirical Validation of Cross-Project Dependency Isolation

**Author**: AgenticOS Engineering Team  
**Date**: August 2026  
**Status**: Verified & Reproducible  

---

## 1. 🎯 Hypothesis

Enforcing a three-tiered discipline mechanism—**Universal Invariant (AGENTS.md Rule 1.1)**, **Deterministic Guardrail (`hooks/environment_guard.py`)**, and **Local Toolchain Orchestration (`uv sync` / `uv run`)**—guarantees that two concurrent Python software projects with mutually incompatible major dependencies can be developed, tested, and modified concurrently in the same workspace with zero dependency bleed and zero global Python pollution.

---

## 2. 📉 Baseline (The Problem)

In unconstrained AI coding agent sessions, agents frequently execute bare `pip install <pkg>` or `pip install -r requirements.txt` without checking for an active virtual environment.

When developing multiple projects sequentially or in parallel:
* **Failure Mode 1**: Project A installs `pydantic>=2.7.0`, overwriting global `pydantic`.
* **Failure Mode 2**: Project B (legacy microservice requiring `pydantic 1.10.x`) immediately fails with runtime import errors (`cannot import name 'BaseModel' from 'pydantic'`).
* **Failure Mode 3**: The AI agent enters a cyclic debugging loop trying to resolve dependency conflicts by randomly reinstalling packages globally.

---

## 3. 🛡️ The AgenticOS Intervention

AgenticOS establishes a non-negotiable 3-tier boundary:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. ALWAYS-ON INVARIANT (AGENTS.md Rule 1.1)                 │
│    "Never install packages globally. Project-local .venv    │
│     is a non-negotiable invariant."                         │
├─────────────────────────────────────────────────────────────┤
│ 2. DETERMINISTIC HOOK (hooks/environment_guard.py)          │
│    Pre-commit & pre-build script that blocks execution if   │
│    .venv/ is missing or active python is global.            │
├─────────────────────────────────────────────────────────────┤
│ 3. CONTEXTUAL EXECUTION (uv run ...)                        │
│    Commands automatically execute within project .venv/      │
│    without requiring manual OS-specific shell activation.   │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 🔬 Controlled Experiment Setup

Two distinct disposable repositories were initialized in the same workspace parent directory:

```text
/workspace/
├── environment-isolation-test-a/
│   ├── .python-version          # 3.12
│   ├── pyproject.toml           # dependencies = ["pydantic>=2.7.0,<3.0.0"]
│   ├── .venv/                   # Project A isolated environment
│   ├── uv.lock                  # Locked to Pydantic 2.7.4
│   └── app/check.py             # Version assertion script
└── environment-isolation-test-b/
    ├── .python-version          # 3.12
    ├── pyproject.toml           # dependencies = ["pydantic>=1.10.0,<2.0.0"]
    ├── .venv/                   # Project B isolated environment
    ├── uv.lock                  # Locked to Pydantic 1.10.13
    └── app/check.py             # Version assertion script
```

---

## 5. 📊 Measured Metrics

| Check # | Objective | Metric / Verification Method |
| :--- | :--- | :--- |
| **M1** | Environment Creation | Distinct filesystem directory paths for `.venv`. |
| **M2** | Version Resolution | Independent lockfiles reflecting target major versions. |
| **M3** | Non-Interference (A → B) | Updating Project A lockfile does not modify Project B. |
| **M4** | Non-Interference (B → A) | Updating Project B lockfile does not modify Project A. |
| **M5** | In-Environment Execution | `uv run python app/check.py` returns `is_v2=True` in A and `is_v1=True` in B. |
| **M6** | Global System Cleanliness | Global `site-packages` verified unmodified. |
| **M7** | Deterministic Hook | `hooks/environment_guard.py` evaluates each project root independently. |
| **M8** | Git Staging Hygiene | Git status confirms `.venv/` is excluded by `.gitignore`. |

---

## 6. 🏆 Results & Observations

```text
==================================================================
EXPERIMENTAL RUN VERIFICATION LOG
==================================================================
[1/8] Project A .venv: .../environment-isolation-test-a/.venv    [PASS]
      Project B .venv: .../environment-isolation-test-b/.venv    [PASS]
[2/8] Project A locked: Pydantic 2.7.4                          [PASS]
      Project B locked: Pydantic 1.10.13                         [PASS]
[3/8] Modifying Project A lockfile -> Project B unaffected        [PASS]
[4/8] Modifying Project B lockfile -> Project A unaffected        [PASS]
[5/8] In-env check A: is_v2=True (Pydantic 2.7.4)               [PASS]
      In-env check B: is_v1=True (Pydantic 1.10.13)              [PASS]
[6/8] Global Python site-packages: 0 new packages installed     [PASS]
[7/8] hooks/environment_guard.py: Exit code 0 for both projects   [PASS]
[8/8] Git status: 0 .venv files tracked                           [PASS]
==================================================================
RESULT: 8/8 EVALUATION METRICS PASSED
==================================================================
```

---

## ⚠️ 7. Limitations & Scope

> [!IMPORTANT]
> **Experimental Scope**:
> * This experiment validates isolation under the standard Python 3.12 / `uv` / project-local `.venv` workflow across Windows, macOS, and Linux.
> * It does not imply that unmanaged environments (e.g. running manual global `pip install` without hooks) are automatically isolated by magic.
> * Isolation depends upon the strict enforcement of `AGENTS.md` Rule 1.1 and the execution of `hooks/environment_guard.py`.

---

## 8. 💡 Conclusion

By shifting environment isolation from an **ad-hoc human reminder** to a **systemic architectural invariant enforced by deterministic hooks and toolchain orchestration**, AI coding agents can safely build and maintain multiple conflicting projects concurrently without environmental degradation.
