---
name: observability
description: OpenTelemetry instrumentation, structured JSON logging, correlation IDs, Prometheus metrics, and specialized AI/LLM system telemetry.
---

# Observability Skill

## 1. When Should I Use This?

Use this skill when:
* Adding structured JSON logging, correlation IDs (`X-Request-ID`), or distributed tracing to APIs and background services.
* Integrating **OpenTelemetry** (OTel) metrics, traces, and span instrumentation.
* Tracking AI / LLM pipeline performance: prompt tokens, completion tokens, latency, retrieval count, cache hits/misses, tool calls, and model errors.
* Setting up health probes (`/health`, `/ready`), Prometheus metrics endpoints (`/metrics`), and error tracking.

---

## 2. What Should I Inspect First?

1. **Service Framework**: FastAPI, Flask, Express/Node, or background worker.
2. **Current Logging Setup**: Inspect `logging.basicConfig` or custom logger modules.
3. **Telemetry Target**: Console JSON stdout, Prometheus exporter, OpenTelemetry Collector, Sentry, or Datadog.
4. **Data Privacy Guardrails**: Ensure NO secrets, tokens, PII (Personally Identifiable Information), or raw passwords can be written to logs.

---

## 3. What Workflow Should I Follow?

```text
Install OpenTelemetry / Structured Logging Tooling
                     ↓
Configure JSON Formatter with Correlation / Request ID Middleware
                     ↓
Instrument HTTP & Database Spans (FastAPI, SQLAlchemy, HTTPX)
                     ↓
Implement AI / LLM Telemetry Wrapper (Tokens, Latency, Retrieval Count)
                     ↓
Expose /metrics (Prometheus) & /health Endpoints
                     ↓
Verify with Synthetic Load & Log Inspection
```

### Structured JSON Logging & Request ID Middleware (FastAPI)

```python
# app/core/logging.py
import json
import logging
import time
import uuid
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="system")

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "request_id": request_id_ctx.get(),
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.root.handlers = [handler]
    logging.root.setLevel(logging.INFO)

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        token = request_id_ctx.set(req_id)
        start_time = time.perf_counter()
        
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        response.headers["X-Request-ID"] = req_id
        logging.getLogger("api.access").info(
            f"{request.method} {request.url.path} {response.status_code} - {duration_ms:.2f}ms"
        )
        request_id_ctx.reset(token)
        return response
```

### Specialized AI / LLM Telemetry Tracker

```python
# app/core/telemetry.py
import logging
import time
from dataclasses import dataclass, asdict

logger = logging.getLogger("telemetry.ai")

@dataclass
class LLMTelemetryEvent:
    provider: str            # 'ollama', 'openai', 'anthropic'
    model: str               # 'llama3.2', 'gpt-4o'
    operation: str           # 'rag_chat', 'ocr_summary'
    latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    retrieval_chunks: int
    cache_hit: bool
    status: str              # 'success', 'error'
    error_message: str | None = None

def track_llm_invocation(event: LLMTelemetryEvent):
    # Emit structured metric event to log stream
    logger.info(f"AI_TELEMETRY: {json.dumps(asdict(event))}")
```

---

## 4. What Decisions Should I Make?

| Observability Pillar | Standard Recommendation |
| :--- | :--- |
| **Logs** | Structured JSON emitted to `stdout` (captured seamlessly by Docker, Render, Kubernetes). |
| **Traces** | OpenTelemetry standard spans with context propagation (`traceparent` header). |
| **Metrics** | Prometheus format (`/metrics`) tracking request count, error rates, p95 latency, and token consumption. |
| **Log Levels** | `INFO` in production; `DEBUG` in local development; `ERROR` with full stack traces for unhandled 500s. |

---

## 5. What Should I Avoid?

* **NEVER log secrets, passwords, or bearer tokens**: Redact authorization headers.
* **NEVER log entire document payloads or sensitive user PII**: Log metadata (e.g. `doc_id`, `length_chars`, `page_count`), not raw personal files.
* **NEVER use synchronous network logging inside the request hot path**: Stream logs to stdout and let background log forwarders handle network transport.

---

## 6. How Should I Verify Success?

```bash
# 1. Run server and trigger test request
curl -i -H "X-Request-ID: test-trace-123" http://localhost:8000/api/v1/health

# 2. Verify response contains X-Request-ID header
# 3. Verify console emits valid JSON log with request_id = "test-trace-123"
```
