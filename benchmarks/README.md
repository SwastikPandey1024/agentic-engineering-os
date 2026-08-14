# Agentic Engineering Benchmarks (AgenticEval)

This directory contains empirical benchmarks and evaluation harnesses designed to measure the impact of **AgenticOS** on AI coding agent performance.

---

## 🎯 The Core Hypothesis

> **Without explicit engineering standards, AI coding agents behave like hyper-productive junior developers: writing functional code rapidly while introducing architectural drift, missing tests, broken environments, and leaked secrets.**

We benchmark coding agents across two experimental regimes:
1. **Unconstrained Baseline (WITHOUT AgenticOS)**: Raw prompt execution with default agent capabilities.
2. **Disciplined Agentic Execution (WITH AgenticOS)**: Agent constrained by `AGENTS.md`, 30+ modular skills, deterministic hooks, and codebase memory.

---

## 📊 Benchmark Dimensions

```text
┌─────────────────────────────────────────────────────────────┐
│ BENCHMARK SUITE TAXONOMY                                    │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Dependency Isolation      │ Cross-project package bleed  │
│ 2. Environment Pollution     │ Global Python contamination  │
│ 3. Secret Handling           │ Accidental credential commit │
│ 4. Architecture Drift        │ Violation of layer boundaries│
│ 5. Missing Tests             │ Code committed without tests │
│ 6. Documentation Drift       │ Hallucinated / unbuilt claims│
└──────────────────────────────┴──────────────────────────────┘
```

---

## 📁 Benchmark Suites

* **[`dependency-isolation/`](dependency-isolation/README.md)**: Validates concurrent execution of mutually incompatible package versions (e.g., Pydantic v2 vs v1).
* **[`environment-pollution/`](environment-pollution/README.md)**: Measures whether agents attempt unisolated `pip install` without `.venv/`.
* **[`secret-handling/`](secret-handling/README.md)**: Tests agent responses to prompts containing simulated API tokens.
* **[`architecture-drift/`](architecture-drift/README.md)**: Evaluates whether agents maintain service-layer boundaries and avoid god-files.
* **[`missing-tests/`](missing-tests/README.md)**: Checks whether agents deliver verified test suites alongside implementation code.
* **[`documentation-drift/`](documentation-drift/README.md)**: Verifies adaptive documentation tiering against actual code.

---

## 📈 Evaluation Metrics

* **Environment Violation Rate (EVR)**: Percentage of runs modifying global interpreter packages.
* **Architecture Compliance Index (ACI)**: Degree of adherence to layered directory structure.
* **Test Coverage Delta**: Percentage of newly authored business logic covered by unit tests.
* **Secret Leak Frequency (SLF)**: Rate of raw `.env` tracking in git revisions.
