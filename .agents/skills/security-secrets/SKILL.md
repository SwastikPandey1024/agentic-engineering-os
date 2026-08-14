---
name: security-secrets
description: Zero-secret leakage standards, environment variable security, secret scanning, CORS protection, and secure coding practices.
---

# Security & Secrets Skill

## 1. When Should I Use This?

Use this skill when:
* Handling authentication, API tokens, database connection strings, passwords, or encryption keys.
* Creating or updating `.env`, `.env.example`, or configuration loaders.
* Auditing codebases and git history for accidentally leaked credentials.
* Hardening API endpoints against OWASP Top 10 vulnerabilities (Injection, broken auth, CORS, sensitive data exposure).

---

## 2. What Should I Inspect First?

1. **Git Tracking & Ignore Files**: Verify `.env`, `.env.local`, `*.pem`, `*.key`, `id_rsa` are in `.gitignore`.
2. **Environment Variable Loaders**: Inspect `app/core/config.py` to ensure credentials are parsed via strongly-typed settings (e.g. Pydantic `BaseSettings`) without fallback to default hardcoded plaintext passwords.
3. **Frontend Source Bundles**: Check frontend code to ensure no secret API keys (e.g. database admin keys, payment secret keys) are prefixed with `VITE_` or embedded in client JS bundles.

---

## 3. What Workflow Should I Follow?

```text
Audit Secrets in Environment (.env vs .env.example)
                  ↓
Ensure Clean Pydantic Settings Validation
                  ↓
Audit Git Staged Changes (git diff --cached)
                  ↓
Run Secret Scanning (Detect-secrets / Gitleaks patterns)
                  ↓
Verify CORS, Rate Limiting & Auth Header Handling
                  ↓
Verify Secure Password Hashing (Argon2 / Bcrypt)
```

### Secure Configuration Pattern (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: SecretStr
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def validate_db_url(cls, v: SecretStr) -> SecretStr:
        url_str = v.get_secret_value()
        if not url_str.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite://")):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL or SQLite connection string.")
        return v

settings = Settings()
```

### Standard Sanitized `.env.example`

```bash
# Environment Configuration Template
ENVIRONMENT=development
PORT=8000

# Database Credentials (replace with real credentials in .env)
DATABASE_URL=postgresql://postgres:your_secure_password@localhost:5432/app_db

# Security & Authentication
JWT_SECRET_KEY=generate_with_openssl_rand_hex_32
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# External AI / LLM APIs
OPENAI_API_KEY=sk-placeholder-do-not-commit-real-key
OLLAMA_BASE_URL=http://localhost:11434

# CORS Allowed Origins (Comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 4. What Decisions Should I Make?

| Security Area | Mandatory Rule |
| :--- | :--- |
| **Password Storage** | Use `bcrypt` or `argon2-cffi`. Never use MD5, SHA-1, or plain SHA-256 for password hashing. |
| **Secrets in Memory** | Use Pydantic `SecretStr` to prevent secrets from leaking in string representations, error logs, or JSON dumps. |
| **CORS Origins** | Never use `allow_origins=["*"]` when `allow_credentials=True` in production. Always specify exact domains. |
| **SQL Injection** | Always use parameterized queries (ORM models or prepared statements). Never concatenate raw strings into SQL queries. |

---

## 5. What Should I Avoid?

* **NEVER commit a real `.env` file to version control**: Keep `.env` strictly git-ignored.
* **NEVER output secret values in error messages or logs**: Redact tokens from exception handlers.
* **NEVER expose private API keys in client-side code**: Any key inside a React/Vite frontend is public and readable by users.
* **NEVER bypass security checks to pass tests**: Do not disable authentication middleware or CSRF tokens in production configurations.

---

## 6. How Should I Verify Success?

```bash
# 1. Check for tracked .env files in git (Cross-Platform)
python -c "import subprocess; files = subprocess.check_output(['git', 'ls-files'], text=True).splitlines(); tracked = [f for f in files if f.endswith('.env')]; assert not tracked, f'CRITICAL: .env files tracked in git: {tracked}'; print('Git ignore check passed: No .env tracked.')"

# 2. Search codebase for accidental hardcoded secret patterns
python -c "
import os, re
pattern = re.compile(r'(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z-_]{35}|ghp_[a-zA-Z0-9]{36})')
found = False
for root, _, files in os.walk('.'):
    if any(p in root for p in ['.git', '.venv', 'node_modules']): continue
    for f in files:
        if f.endswith(('.py', '.js', '.ts', '.tsx', '.json', '.yaml', '.yml', '.env.example')):
            content = open(os.path.join(root, f), errors='ignore').read()
            if pattern.search(content):
                print(f'ALERT: Potential secret found in {os.path.join(root, f)}')
                found = True
if not found: print('Secret scan clean!')
"
```
