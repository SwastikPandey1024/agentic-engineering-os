---
name: testing-quality
description: Comprehensive testing strategy across unit, integration, smoke, and regression tests using pytest, fixtures, vitest, and code quality tools.
---

# Testing & Quality Skill

## 1. When Should I Use This?

Use this skill when:
* Writing unit, integration, or regression tests for backend APIs, ML pipelines, or frontend components.
* Verifying code changes after a bug fix or feature addition.
* Setting up testing harnesses, fixtures, mocks, and coverage reporting.
* Enforcing quality gates (linting, formatting, type checking, security static analysis).

Never consider any engineering task complete until tests have been executed and verified.

---

## 2. What Should I Inspect First?

1. **Test Runner & Config**:
   * Python: Check `pytest.ini`, `[tool.pytest.ini_options]` in `pyproject.toml`, or `conftest.py`.
   * Frontend: Check `vitest.config.ts`, `jest.config.js`, or `npm test` script.
2. **Existing Test Fixtures**: Look in `tests/conftest.py` for database mocks, client fixtures (`AsyncClient`, `TestClient`), and synthetic data generators.
3. **Current Test Pass Rate**: Run existing tests before making code changes to establish a clean baseline.

---

## 3. What Workflow Should I Follow?

```text
Establish Baseline Test State
              ↓
Implement / Modify Feature or Fix
              ↓
Write / Update Focused Unit Tests (fast, isolated, mocked I/O)
              ↓
Write / Update Integration Tests (database transactions, API contracts)
              ↓
Run Code Quality Suite (Ruff, ESLint, Mypy/TypeScript)
              ↓
Execute Full Test Suite + Measure Coverage
              ↓
Inspect Diff to Ensure No Test Tampering
```

### The Testing Pyramid Structure

```text
         ▲
        / \        Smoke / E2E Tests (5-10%)
       /   \       - Complete API lifecycle, Docker health, live ping
      /─────\
     /       \     Integration Tests (20-30%)
    /         \    - Real DB queries, Redis cache, multi-service flows
   /───────────\
  /             \  Unit Tests (60-70%)
 /               \ - Pure business logic, schemas, transforms, math
/─────────────────\
```

### Robust Pytest Harness Example (`conftest.py`)

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.dependencies.database import get_db

class MockDB:
    def __init__(self):
        self.storage = {}
    def get(self, item_id: str):
        return self.storage.get(item_id)
    def save(self, item_id: str, data: dict):
        self.storage[item_id] = data
        return data

@pytest.fixture
def mock_db():
    return MockDB()

@pytest.fixture
def client(mock_db):
    def override_get_db():
        return mock_db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

### Writing Deterministic Unit & Integration Tests

```python
# tests/unit/test_validation.py
import pytest
from pydantic import ValidationError
from app.schemas.auth import UserRegisterSchema

def test_user_register_schema_valid():
    data = {"email": "user@example.com", "password": "SecurePassword123!"}
    user = UserRegisterSchema(**data)
    assert user.email == "user@example.com"

def test_user_register_schema_invalid_email():
    with pytest.raises(ValidationError):
        UserRegisterSchema(email="not-an-email", password="123")
```

```python
# tests/integration/test_api_endpoints.py
def test_create_and_fetch_document(client):
    payload = {"title": "Contract Spec", "content": "Sample OCR content"}
    response = client.post("/api/v1/documents", json=payload)
    assert response.status_code == 201
    doc_id = response.json()["id"]

    get_resp = client.get(f"/api/v1/documents/{doc_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Contract Spec"
```

---

## 4. What Decisions Should I Make?

| Testing Need | Tool / Strategy |
| :--- | :--- |
| **HTTP API Testing** | `httpx.AsyncClient` (for async FastAPI) or `fastapi.testclient.TestClient` |
| **External Service Mocking** | `unittest.mock.patch` or `pytest-mock` (for LLMs, Stripe, S3, OCR models) |
| **Frontend UI Testing** | `vitest` + `@testing-library/react` |
| **Coverage Threshold** | Target >= 80% coverage on domain and service layers; 100% on security/auth utilities. |

---

## 5. What Should I Avoid?

* **NEVER delete or skip failing tests**: Fix the underlying regression rather than annotating `@pytest.mark.skip` or commenting tests out.
* **NEVER rely on live network in unit tests**: Unit tests must not call live external APIs (OpenAI, AWS S3, external payment gateways).
* **NEVER make tests order-dependent**: Each test must be completely isolated, creating and destroying its own fixture state.
* **NEVER mock what you want to test**: Mock only external boundary dependencies, not the internal code under test.

---

## 6. How Should I Verify Success?

```bash
# 1. Run full test suite with verbose output
pytest -v --tb=short

# 2. Run coverage report
pytest --cov=app --cov-report=term-missing

# 3. Run linting and static typing
ruff check .
ruff format --check .
mypy app/

# 4. Frontend verification
npm run lint
npm run type-check
npm test -- --run
```
