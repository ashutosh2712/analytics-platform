# Analytics Platform

Real-time multi-tenant analytics platform built with:

- FastAPI
- PostgreSQL
- Redis
- Celery
- Next.js
- Recharts

## Features

### Authentication & Multi-Tenancy

- JWT Authentication
- Refresh Token Support
- RBAC (Owner / Admin / Analyst / Viewer)
- Organization Isolation
- Frontend Role-based UI Rendering

### Event Ingestion

- Single Event API
- Batch Event API
- CSV Upload
- API Key Authentication
- Async Processing via Celery + Redis

### Analytics

- Dashboard Creation
- Widget Creation
- Dynamic Charts
- Real-time Aggregation
- Dashboard Data APIs

### API Key Management

- Generate API Keys
- Rotate API Keys
- Revoke API Keys

## Tech Stack

Frontend:

- Next.js
- TypeScript
- TailwindCSS
- Recharts

Backend:

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- Alembic

## Architecture

Frontend
↓
FastAPI
↓
Redis Queue
↓
Celery Workers
↓
PostgreSQL
↓
Analytics APIs
↓
Dashboard Visualization

## Environment Variables

Create a `.env` file in the root directory:

```env
POSTGRES_DB=analytics_db

POSTGRES_USER=analytics_user

POSTGRES_PASSWORD=analytics_pass

DATABASE_URL=postgresql+asyncpg://analytics_user:analytics_pass@db:5432/analytics_db

REDIS_URL=redis://redis:6379/0

JWT_SECRET_KEY=b989hhoiuh889huh8hnoi890

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Setup

```bash
docker compose up --build
```

## Application URLs

Frontend:

```text
http://localhost:3000
```

Backend Swagger:

```text
http://localhost:8000/docs
```

## Demo Seed Data

A sample SQL seed file is included:

```text
analytics_platform_seed.sql
```

It contains:

- Demo Organization
- Demo Users
- RBAC Roles
- Dashboard Data
- Widgets
- Analytics Events

## Demo Accounts

Password for all accounts:

```text
secret123
```

| Role    | Email                                       |
| ------- | ------------------------------------------- |
| OWNER   | [owner@test.com](mailto:owner@test.com)     |
| ADMIN   | [admin@test.com](mailto:admin@test.com)     |
| ANALYST | [analyst@test.com](mailto:analyst@test.com) |
| VIEWER  | [viewer@test.com](mailto:viewer@test.com)   |

## Run Seed File

```bash
docker exec -it analytics-db psql -U analytics_user -d analytics_db
```

Then run:

```sql
\i analytics_platform_seed.sql
```
