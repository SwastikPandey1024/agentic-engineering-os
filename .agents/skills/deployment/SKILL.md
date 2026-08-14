---
name: deployment
description: Production deployment to Render, Vercel, Streamlit Community Cloud, pre-flight environment checks, and post-deployment smoke testing.
---

# Deployment Skill

## 1. When Should I Use This?

Use this skill when:
* Deploying applications or services to cloud hosting platforms (Render, Vercel, Streamlit Community Cloud, Docker VPS).
* Creating or updating deployment configuration files (`render.yaml`, `vercel.json`, `deploy.sh`).
* Performing pre-flight deployment audits (environment variables, database migrations, CORS, build scripts).
* Executing post-deployment smoke tests to verify real endpoint availability.

---

## 2. What Should I Inspect First?

1. **Target Platform & Service Type**:
   * Render Web Service / Background Worker / Managed PostgreSQL.
   * Vercel Frontend SPA / Serverless API.
   * Streamlit Community Cloud Dashboard.
2. **Configuration Manifests**:
   * Look for `render.yaml`, `vercel.json`, `Procfile`, `.streamlit/config.toml`.
3. **Environment Variable Parity**: Cross-reference `.env.example` with platform dashboard secrets to ensure zero missing variables.
4. **Database Migration State**: Ensure migrations are automated or run prior to serving live traffic.

---

## 3. What Workflow Should I Follow?

```text
Local Test & Build Verification (Ensure clean build & test pass)
                   ↓
Environment Variable Audit (Compare .env.example with Target Env)
                   ↓
Generate / Validate Platform Manifest (render.yaml / vercel.json)
                   ↓
Database Migration Execution Strategy
                   ↓
Deploy Artifact / Trigger Git-based Cloud Build
                   ↓
Post-Deployment Smoke Test (Live Health Check & Endpoint Verification)
```

### Render Blueprint Configuration (`render.yaml`)

```yaml
# render.yaml
services:
  # FastAPI Backend Service
  - type: web
    name: app-backend
    env: python
    region: singapore
    plan: free
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /api/v1/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: ENVIRONMENT
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: app-postgres
          property: connectionString

  # React Frontend SPA (or static site)
  - type: web
    name: app-frontend
    env: static
    region: singapore
    plan: free
    buildCommand: cd frontend && npm ci && npm run build
    staticPublishPath: ./frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_API_BASE_URL
        value: https://app-backend.onrender.com

databases:
  - name: app-postgres
    plan: free
    region: singapore
```

### Vercel SPA Routing Configuration (`vercel.json`)

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://your-backend.onrender.com/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

### Streamlit Deployment Checklist

1. Create `.streamlit/config.toml` for theme and headless server configuration:
   ```toml
   [server]
   headless = true
   enableCORS = false
   enableXsrfProtection = true
   ```
2. Keep lightweight `requirements.txt` specifically for Streamlit Cloud (avoid bloated CUDA/torch libraries unless GPU instance is allocated).

---

## 4. What Decisions Should I Make?

| Platform Choice | Ideal Use-Case |
| :--- | :--- |
| **Render** | Fullstack web apps (Dockerized FastAPI backend, PostgreSQL database, background workers). |
| **Vercel** | High-performance React/Vite SPAs and Next.js frontends with global edge CDN. |
| **Streamlit Cloud** | Interactive ML prototypes, data forecasting dashboards, internal analytical tools. |
| **Docker VPS** | Self-hosted multi-container systems needing custom GPU/CPU allocation (Ollama + OCR + FAISS). |

---

## 5. What Should I Avoid?

* **NEVER deploy without checking CORS configuration**: Ensure backend `allow_origins` includes the production frontend domain (e.g. `https://myapp.vercel.app`).
* **NEVER claim deployment succeeded without testing live URLs**: You must ping the live production URL and verify `200 OK`.
* **NEVER run destructive database syncs in production**: Use non-destructive migration commands (`alembic upgrade head` or `prisma migrate deploy`), never `db push --force-reset`.
* **NEVER rely on ephemeral filesystem for persistent files**: Deployments on Render/Vercel have ephemeral disks; use S3, Supabase Storage, or mounted Docker volumes for persistent uploads.

---

## 6. How Should I Verify Success?

Run post-deployment smoke verification:

```bash
# 1. Health check probe & payload assertion (Cross-Platform Python)
python -c "
import urllib.request, json
url = 'https://app-backend.onrender.com/api/v1/health'
try:
    with urllib.request.urlopen(url, timeout=10) as res:
        assert res.status == 200, f'Status {res.status}'
        data = json.loads(res.read().decode('utf-8'))
        assert data.get('status') == 'ok', f'Unexpected: {data}'
        print('Deployment Live Smoke Test: PASSED (200 OK)')
except Exception as e:
    print(f'Deployment Smoke Test FAILED: {e}')
"

# 2. Check frontend SPA response headers
curl -I https://myapp.vercel.app/
```
