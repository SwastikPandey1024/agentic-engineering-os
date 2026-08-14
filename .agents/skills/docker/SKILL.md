---
name: docker
description: Production-grade containerization, multi-stage Dockerfiles, non-root user execution, docker-compose orchestration, and health checks.
---

# Docker Skill

## 1. When Should I Use This?

Use this skill when:
* Creating or optimizing `Dockerfile` and `docker-compose.yml` configurations for backend, frontend, or ML services.
* Implementing multi-stage builds to minimize container image sizes and eliminate build tools from runtime images.
* Setting up container healthchecks, non-root security contexts, and `.dockerignore` files.
* Running and debugging local multi-service container environments.

---

## 2. What Should I Inspect First?

1. **Service Runtime & Dependencies**:
   * Python: Requires system C-libraries? (e.g. `libgomp1`, `ffmpeg`, `libgl1` for OpenCV/PaddleOCR).
   * Frontend: Node build step vs static file server (Nginx/Caddy).
2. **Environment Variables**: Inspect `.env.example` for required runtime variables and database hostnames.
3. **Port Mappings & Health Endpoints**: Identify HTTP listening ports and health check endpoints (e.g. `/api/v1/health` or `/ready`).

---

## 3. What Workflow Should I Follow?

```text
Create .dockerignore (Exclude .venv, node_modules, .git, datasets)
                  ↓
Write Multi-Stage Dockerfile (Builder Stage → Runtime Stage)
                  ↓
Configure Non-Root User & Working Directory
                  ↓
Define HEALTHCHECK Instruction
                  ↓
Configure docker-compose.yml (Environment, Ports, Volumes, Depends_on)
                  ↓
Build & Test Container Locally (Run smoke tests against exposed port)
```

### Production Multi-Stage Python Backend Dockerfile

```dockerfile
# Dockerfile.backend
# ==========================================
# Stage 1: Build stage
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# Stage 2: Minimal Runtime stage
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Install minimal runtime system libraries (e.g., for OpenCV/OCR)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application source code
COPY --chown=appuser:appuser app/ ./app/

USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-Stage React Frontend Dockerfile with Nginx

```dockerfile
# Dockerfile.frontend
# ==========================================
# Stage 1: Build React SPA
# ==========================================
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ==========================================
# Stage 2: Serve via Nginx Unprivileged
# ==========================================
FROM nginx:alpine-slim
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:80/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

### Mandatory `.dockerignore`

```text
.git
.github
.venv
venv
__pycache__
*.pyc
node_modules
dist
build
datasets/raw
datasets/processed
ml/artifacts/*.pt
*.log
.env
.env.local
.pytest_cache
.coverage
```

---

## 4. What Decisions Should I Make?

| Strategy | Recommendation |
| :--- | :--- |
| **Base Image** | Always use `-slim` (Debian) or `-alpine` for minimal surface area and fast pull times. |
| **Security User** | Never run containers as `root` in production. Always create and switch to a non-root `appuser`. |
| **Signal Handling** | Use `exec` form for `CMD` (`CMD ["uvicorn", ...]`), ensuring PID 1 receives `SIGTERM` and `SIGINT` cleanly. |
| **Data Persistence** | Mount persistent storage (e.g. SQLite databases, uploaded PDFs, FAISS indexes) using named Docker volumes. |

---

## 5. What Should I Avoid?

* **NEVER copy `.env` into the Docker image**: Environment variables must be injected at container runtime.
* **NEVER run `pip install` without `--no-cache-dir`**: Avoid inflating image size with cached wheel downloads.
* **NEVER omit `.dockerignore`**: Sending huge `.git/` and dataset folders as build context slows down builds significantly.
* **NEVER use `latest` tag in production base images**: Pin major/minor versions (e.g. `python:3.12-slim`, `node:20-alpine`).

---

## 6. How Should I Verify Success?

```bash
# 1. Build container image
docker build -t my-app:test -f Dockerfile.backend .

# 2. Run container in detached mode
docker run -d --name test-container -p 8000:8000 --env-file .env.example my-app:test

# 3. Verify health status and logs
docker ps --filter "name=test-container"
docker logs test-container

# 4. Smoke test exposed HTTP port
curl -i http://localhost:8000/api/v1/health

# 5. Clean up
docker stop test-container && docker rm test-container
```
