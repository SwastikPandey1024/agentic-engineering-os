# Benchmark: Dependency Isolation Under Version Collision

## 🔬 Experiment Definition

* **Objective**: Evaluate whether two concurrent projects requiring mutually incompatible major versions of a Python package can be bootstrapped, locked, and executed without cross-contamination.
* **Test Case**: Pydantic v2 (`pydantic>=2.7.0,<3.0.0`) vs Pydantic v1 (`pydantic>=1.10.0,<2.0.0`).

---

## 📊 Results Summary

| Metric | Without AgenticOS (Raw Prompt) | With AgenticOS (Disciplined) |
| :--- | :--- | :--- |
| **Global Package Pollution** | ❌ High (Overwrites global site-packages) | ✅ Zero (100% project-local `.venv`) |
| **Cross-Project Bleed** | ❌ Fails (Project B breaks when A updates) | ✅ None (Independent `uv.lock` manifests) |
| **Deterministic Guard** | ❌ Missing | ✅ Blocked via `hooks/environment_guard.py` |
| **Test Verification** | ⚠️ Ad-hoc | ✅ Automated in-environment unit test |

See full scientific case study in [`docs/case-studies/dependency-isolation.md`](../../docs/case-studies/dependency-isolation.md).
