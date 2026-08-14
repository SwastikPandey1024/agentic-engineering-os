---
name: python-api
description: Production FastAPI application architecture, Pydantic v2 validation, route structuring, dependency injection, async I/O, error handling, and health probes.
---

# Python API Skill

## 1. When Should I Use This?

Use this skill when:
* Building or refactoring REST APIs using **FastAPI** (or Flask when maintaining legacy projects).
* Designing Pydantic v2 schemas for request validation and response serialization.
* Implementing dependency injection for authentication, database sessions, and business services.
* Adding health/readiness endpoints, structured logging, CORS middleware, and custom exception handlers.

---

## 2. What Should I Inspect First?

1. **API Framework & Version**: Check if using FastAPI (>=0.110.0) with Pydantic v2 or Flask.
2. **Current Routing Tree**: Inspect `app/api/v1/` or `routes/` to identify existing endpoint prefixes and versioning conventions.
3. **Dependency Injection Providers**: Check `app/api/v1/dependencies/` for existing `get_db`, `get_current_user`, or service factories.
4. **Error Handling Architecture**: Verify how custom exceptions are caught and formatted into standard JSON error responses.

---

## 3. What Workflow Should I Follow?

```text
Define Pydantic Request & Response Schemas
                   ↓
Implement Domain Service / Business Logic Layer
                   ↓
Create Dependency Injection Providers
                   ↓
Implement APIRouter Endpoints with Proper HTTP Status Codes
                   ↓
Register Router with FastAPI Main Application
                   ↓
Implement Health (/health) & Readiness (/ready) Probes
                   ↓
Write Pytest Integration Tests with TestClient / AsyncClient
```

### Production FastAPI Application Layout

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB pools, load lightweight model caches
    print("Application starting up...")
    yield
    # Shutdown: Close DB pools, cleanup connections
    print("Application shutting down...")

app = FastAPI(
    title="Production API Engine",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=None
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred.", "error_type": exc.__class__.__name__}
    )

# Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["system"])
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
```

### Pydantic v2 Schemas and Endpoint Implementation

```python
# app/api/v1/schemas/documents.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Document title")

class DocumentCreate(DocumentBase):
    content: str = Field(..., min_length=1, description="Extracted OCR content")

class DocumentResponse(DocumentBase):
    id: str
    user_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

```python
# app/api/v1/routes/documents.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.schemas.documents import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService
from app.api.v1.dependencies.services import get_document_service

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    payload: DocumentCreate,
    service: DocumentService = Depends(get_document_service)
):
    try:
        return service.create_document(payload)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err)
        )
```

---

## 4. What Decisions Should I Make?

| API Architectural Requirement | Decision Rule |
| :--- | :--- |
| **Async vs Sync Endpoints** | Use `async def` for I/O operations (database queries, network requests). Use standard `def` for CPU-bound tasks so FastAPI runs them in a background threadpool without blocking the event loop. |
| **HTTP Status Codes** | `200 OK` (Standard Read/Update), `201 Created` (Resource Created), `204 No Content` (Delete), `400 Bad Request`, `401 Unauthorized` (Invalid Auth), `403 Forbidden` (Permission Denied), `404 Not Found`, `422 Unprocessable` (Schema Error). |
| **Response Serialization** | Always specify `response_model` on endpoints to filter out sensitive internal fields and guarantee schema contracts. |

---

## 5. What Should I Avoid?

* **NEVER execute blocking CPU computations inside `async def`**: Blocking the asyncio event loop with OCR parsing or heavy ML loops freezes the entire server for all concurrent clients.
* **NEVER put raw business logic inside route handlers**: Endpoints must only validate requests, invoke domain services, and return responses.
* **NEVER return raw database entity instances directly**: Always serialize through dedicated Pydantic schemas.
* **NEVER expose interactive `/docs` (Swagger UI) publicly in production without authorization**: Disable or protect OpenAPI endpoints in production.

---

## 6. How Should I Verify Success?

```bash
# 1. Run unit and integration tests with pytest (isolated via uv)
uv run pytest tests/ -v

# 2. Run standalone endpoint verification (TestClient - No live server required)
python -c "
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.get('/api/v1/health')
assert response.status_code == 200, f'Expected 200, got {response.status_code}'
assert response.json().get('status') == 'ok', f'Unexpected payload: {response.json()}'
print('FastAPI Health Check: PASSED (Status 200, OK)')
"

# 3. Check code formatting & linting
uv run ruff check .
```
