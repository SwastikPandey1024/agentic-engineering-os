---
name: code-architecture
description: Layered service-oriented system design, dependency injection boundaries, circular import elimination, and separation of business logic from I/O.
---

# Code Architecture Skill

## 1. When Should I Use This?

Use this skill when:
* Structuring or refactoring a backend API, service layer, data processing pipeline, or frontend feature.
* Designing interactions between endpoints, business logic, databases, external APIs, and ML models.
* Resolving circular imports, monolithic god-files, or tightly coupled components.
* Establishing clean architectural boundaries before writing complex features.

Do NOT use this skill for trivial one-line bug fixes that do not alter system structure.

---

## 2. What Should I Inspect First?

1. **Existing Architecture Style**:
   * Is it layered (API ↔ Service ↔ Repository ↔ Model)?
   * Is it Hexagonal / Ports & Adapters?
   * Is it Feature-Sliced (Frontend: `features/auth/`, `features/documents/`)?
2. **Current Dependency Flow**: Check import statements across modules. Identify where I/O, DB sessions, and external HTTP clients are instantiated.
3. **Existing Shared Utilities**: Check `utils/`, `core/`, `common/`, `lib/` to avoid reinventing existing patterns.
4. **Configuration Access**: Ensure configuration is injected or sourced via a unified settings module (e.g. `core/config.py`), not scattered `os.getenv` calls.

---

## 3. What Workflow Should I Follow?

```text
Map Architectural Boundaries
            ↓
Search Existing Code for Equivalent Services / Helpers
            ↓
Separate Business Logic from I/O & Transport
            ↓
Define Clean Type / Interface Contracts (Pydantic / TS Interfaces)
            ↓
Implement Domain Logic with Dependency Injection
            ↓
Wire into API / Transport Layer
            ↓
Verify Independence with Unit Tests
```

### The Standard 4-Layer Backend Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. API / Transport Layer (routes, controllers, endpoints)   │
│    - Handles HTTP, query params, auth tokens, status codes  │
│    - Validates request schemas; serializes response schemas │
└──────────────────────────────┬──────────────────────────────┘
                               │ calls
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Service / Domain Layer (business logic, orchestration)    │
│    - Pure domain operations, business validation, workflows │
│    - NO direct knowledge of HTTP status codes or FastAPI req │
└──────────────────────────────┬──────────────────────────────┘
                               │ calls via DI
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Data Access / Repository Layer (SQLAlchemy, Prisma, SDK) │
│    - DB queries, transactions, vector store lookups         │
└──────────────────────────────┬──────────────────────────────┘
                               │ operates on
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Core / Domain Models & Config                            │
│    - DB entities, Pydantic schemas, settings, exceptions    │
└─────────────────────────────────────────────────────────────┘
```

### Concrete Dependency Injection Pattern (Python)

```python
# app/services/document_service.py
from app.models.document import Document
from app.schemas.document import DocumentCreate
from typing import Protocol

class DocumentRepository(Protocol):
    def get_by_id(self, doc_id: str) -> Document | None: ...
    def save(self, doc: Document) -> Document: ...

class DocumentService:
    def __init__(self, repo: DocumentRepository, ocr_client) -> None:
        self.repo = repo
        self.ocr_client = ocr_client

    def process_and_store(self, user_id: str, file_bytes: bytes, filename: str) -> Document:
        # 1. Pure domain logic
        extracted_text = self.ocr_client.extract_text(file_bytes)
        if not extracted_text.strip():
            raise ValueError("Document contains no readable text.")
            
        doc = Document(user_id=user_id, filename=filename, content=extracted_text)
        return self.repo.save(doc)
```

```python
# app/api/v1/routes/documents.py (FastAPI wiring)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from app.api.v1.dependencies.services import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile,
    service: DocumentService = Depends(get_document_service)
):
    try:
        content = await file.read()
        return service.process_and_store(user_id="u_123", file_bytes=content, filename=file.filename)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
```

---

## 4. What Decisions Should I Make?

| Architectural Question | Guiding Heuristic |
| :--- | :--- |
| **Where does this code belong?** | If it handles `request`/`status_code` → **API Layer**.<br>If it calculates, transforms, or validates business rules → **Service Layer**.<br>If it executes raw SQL/ORM operations → **Repository/Data Layer**.<br>If it parses `.env` → **Core Config**. |
| **Async vs Sync** | Use `async` for I/O-bound tasks (database queries, network requests, SSE streaming). Use synchronous threads/processes or background workers for heavy CPU-bound tasks (OCR parsing, ML inference). |
| **File Sizing** | Keep modules under 300-400 lines. If a file grows beyond 400 lines, extract sub-services, routers, or helper modules. |

---

## 5. What Should I Avoid?

* **NEVER leak DB sessions into API routes**: Avoid querying raw SQLAlchemy models directly inside endpoint handlers.
* **NEVER import API schemas into database models**: Maintain unidirectional dependencies (API → Services → Models/Core).
* **NEVER use circular imports**: Refactor shared type definitions or protocols into a dedicated `types.py` or `schemas/common.py`.
* **NEVER perform direct I/O in constructors**: Keep `__init__` lightweight and deterministic; instantiate network/file handles in startup lifecycle hooks or explicit connection methods.

---

## 6. How Should I Verify Success?

```bash
# 1. Verify that domain logic is testable without a real database/HTTP server
pytest tests/unit/test_services.py -v

# 2. Check for circular imports and module integrity
python -c "import app.main; print('Architecture import graph clean')"

# 3. Verify clean typing boundaries with Ruff / mypy
mypy app/
```
