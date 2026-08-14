---
name: database-postgresql
description: PostgreSQL relational schema design, Prisma ORM and SQLAlchemy/Alembic migrations, indexes, transaction boundaries, and pool optimization.
---

# Database (PostgreSQL) Skill

## 1. When Should I Use This?

Use this skill when:
* Designing or modifying relational database tables, foreign key constraints, and indexes in PostgreSQL.
* Managing schema migrations using **Prisma ORM** (`schema.prisma`) or **SQLAlchemy 2.0** + **Alembic**.
* Optimizing SQL queries, eliminating N+1 query bottlenecks, and managing transactional integrity.
* Configuring connection pools (Supabase transaction poolers, SQLAlchemy asyncpg pool sizes).

---

## 2. What Should I Inspect First?

1. **ORM Tooling**:
   * Prisma: Inspect `backend/schema.prisma` and `prisma/migrations/`.
   * SQLAlchemy: Inspect `app/models/`, `alembic.ini`, and `alembic/versions/`.
2. **Connection Semantics**:
   * Inspect `DATABASE_URL` (direct vs pooler port `6543` vs `5432` in Supabase/PgBouncer).
3. **Existing Schema & Indexes**: Inspect primary key conventions (UUIDs vs BigInt) and foreign key relation maps.

---

## 3. What Workflow Should I Follow?

```text
Inspect Existing Schema & Migration History
                    ↓
Draft Schema Changes in Model / Prisma Schema
                    ↓
Add Indexes on Foreign Keys and High-Frequency Query Filters
                    ↓
Generate Migration File (Alembic / Prisma)
                    ↓
Inspect Generated SQL Migration Script for Destructive Actions
                    ↓
Apply Migration (alembic upgrade head / prisma migrate deploy)
                    ↓
Verify with Integration Test
```

### Prisma ORM Workflow (TypeScript / Node)

```prisma
// backend/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id           String        @id @default(uuid())
  email        String        @unique
  name         String
  createdAt    DateTime      @default(now())
  updatedAt    DateTime      @updatedAt
  documents    Document[]
  transactions Transaction[]

  @@index([email])
}

model Document {
  id        String   @id @default(uuid())
  userId    String
  title     String
  ocrText   String   @db.Text
  createdAt DateTime @default(now())
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([createdAt])
}
```

```bash
# Generate and apply migration locally
npx prisma migrate dev --name add_document_ocr_text

# Deploy migration in production (non-destructive)
npx prisma migrate deploy
```

### SQLAlchemy 2.0 + Alembic Workflow (Python)

```python
# app/models/document.py
from datetime import datetime, timezone
import uuid
from sqlalchemy import String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Explicit indexes
    __table_args__ = (
        Index("idx_documents_user_id", "user_id"),
        Index("idx_documents_created_at", "created_at"),
    )
```

```bash
# Generate migration script automatically from model metadata
alembic revision --autogenerate -m "create documents table"

# Upgrade database to latest revision
alembic upgrade head
```

---

## 4. What Decisions Should I Make?

| Database Requirement | Best Practice Decision |
| :--- | :--- |
| **Primary Keys** | Use UUIDv4 (`String(36)` / `uuid`) for distributed API resources to prevent sequential ID scraping. |
| **Indexing Heuristic** | Index every foreign key column (`user_id`, `vendor_id`) and fields used in `WHERE`, `ORDER BY`, or `JOIN` filters. |
| **Transactions** | Always wrap multi-table modifications (e.g. deduct balance + insert transaction record) in an atomic database transaction. |
| **Pool Sizing** | For serverless / Render free tiers: `pool_size=5`, `max_overflow=10`, `pool_recycle=1800` to prevent exhausting PostgreSQL client connection limits. |

---

## 5. What Should I Avoid?

* **NEVER run destructive resets (`prisma db push --force-reset` or `alembic downgrade base`) on live databases**.
* **NEVER query records in a loop (N+1 query problem)**: Use eager loading (`selectinload` in SQLAlchemy or `include: { user: true }` in Prisma).
* **NEVER store large binary blobs (PDFs, images) directly in PostgreSQL columns**: Store files in object storage (S3 / Local storage) and save the file path or URI in the database.
* **NEVER omit timezone in timestamp columns**: Always use `TIMESTAMP WITH TIME ZONE` (`DateTime(timezone=True)`).

---

## 6. How Should I Verify Success?

```bash
# 1. Verify migration status
alembic current
# Or Prisma
npx prisma migrate status

# 2. Run database integration test suite
pytest tests/integration/test_database.py -v
```
