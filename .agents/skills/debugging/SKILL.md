---
name: debugging
description: Systematic 7-step root-cause debugging methodology, error trace diagnosis, environment vs application bug isolation, and regression test authoring.
---

# Debugging Skill

## 1. When Should I Use This?

Use this skill when:
* Diagnosing any runtime error, failing test, unhandled exception, 500 server crash, or unexpected behavior.
* Investigating memory leaks, race conditions, or performance degradation.
* Troubleshooting dependency, environment, or configuration mismatches.

Never apply speculative patches or guess solutions without first isolating the root cause.

---

## 2. What Should I Inspect First?

1. **Exact Error Traceback & Logs**:
   * Inspect the full stack trace: file path, line number, exception type, and error message.
   * Look for the *first* failure in a cascading error stack.
2. **Environment & Context**:
   * What was the exact input or state when the error occurred?
   * Does it fail locally, inside Docker, or only in CI?
3. **Recent Changes**:
   * Run `git diff` or `git log -n 5` to inspect what modified right before the failure began.

---

## 3. What Workflow Should I Follow?

```text
1. REPRODUCE: Create a minimal, deterministic reproduction script or test case.
      ↓
2. OBSERVE: Capture exact inputs, outputs, log statements, and stack traces.
      ↓
3. CLASSIFY: Is it an Environment, Configuration, Data, or Logic bug?
      ↓
4. ROOT CAUSE: Trace the data flow backward to find where the bad state originated.
      ↓
5. MINIMAL FIX: Apply the smallest, surgically precise fix addressing the root cause.
      ↓
6. REGRESSION TEST: Turn the reproduction into a permanent test case.
      ↓
7. VERIFY: Run the entire test suite and verify no secondary regressions exist.
```

### Bug Classification Guide

```text
┌─────────────────┬───────────────────────────────────┬────────────────────────────────────┐
│ Bug Class       │ Common Symptoms                   │ Diagnostic Action                  │
├─────────────────┼───────────────────────────────────┼────────────────────────────────────┤
│ Environment     │ ModuleNotFoundError, CUDA out of  │ Check .venv, lockfiles, CUDA       │
│                 │ memory, missing shared C library  │ drivers, node_modules.             │
├─────────────────┼───────────────────────────────────┼────────────────────────────────────┤
│ Configuration   │ KeyError in settings, NoneType in │ Check .env, .env.example, Pydantic │
│                 │ DB URL, CORS blocked by origin    │ Settings schema defaults.          │
├─────────────────┼───────────────────────────────────┼────────────────────────────────────┤
│ Data Contract   │ ValidationError, schema mismatch, │ Check Pydantic/Zod schemas, null   │
│                 │ NaN in features, unparsed JSON    │ handling, API response types.      │
├─────────────────┼───────────────────────────────────┼────────────────────────────────────┤
│ Logic / State   │ AssertionError, off-by-one, race  │ Step through logic with debugger   │
│                 │ condition, stale cache hits       │ or inspect intermediate state.     │
└─────────────────┴───────────────────────────────────┴────────────────────────────────────┘
```

### Python Debugging Techniques

```python
# 1. Surgical Logging (Temporary Debugging)
import logging
logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)

def process_data(records: list[dict]):
    logger.debug(f"Processing {len(records)} records. First record: {records[0] if records else None}")
    for idx, rec in enumerate(records):
        if "amount" not in rec or rec["amount"] is None:
            logger.error(f"Malformed record at index {idx}: {rec}")
            raise ValueError(f"Record at index {idx} missing 'amount'")
```

```python
# 2. Permanent Regression Test
def test_regression_issue_42_null_amount_handled(client):
    """Ensure API returns 422 with meaningful error when amount is null."""
    payload = {"sender": "u1", "amount": None}
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 422
    assert "amount" in response.text
```

---

## 4. What Decisions Should I Make?

| Debugging Scenario | Decision Rule |
| :--- | :--- |
| **Repeated Command Failure** | If a command fails twice, **STOP**. Do not run it a 3rd time without altering the diagnosis or inputs. |
| **Symptom vs Cause** | Never just wrap a broken line in a bare `try...except: pass` or `if obj is not None`. Find *why* `obj` was `None` in the first place. |
| **Flaky / Non-deterministic Failures** | Check for unseeded random state, time-dependent logic (`datetime.now()` without mocking), race conditions in async tasks, or shared mutable global state. |

---

## 5. What Should I Avoid?

* **NEVER suppress errors silently**: Bare `except:` or discarding stack traces hides bugs and corrupts data downstream.
* **NEVER modify multiple unrelated files during debugging**: Keep debugging diffs isolated to the specific bug surface.
* **NEVER leave temporary debug prints or hardcoded test values in production code**: Clean up all print statements before committing.
* **NEVER declare a bug fixed without a passing test**: If you can't prove it failed before and passes now, it's not fixed.

---

## 6. How Should I Verify Success?

```bash
# 1. Run the new regression test specifically
pytest tests/unit/test_regression.py -k "test_regression_issue" -v

# 2. Run the entire test suite to guarantee zero side-effects
pytest -v

# 3. Check git diff to ensure minimal, clean changes
git diff
```
