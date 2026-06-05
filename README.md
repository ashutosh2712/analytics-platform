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
- RBAC (Admin / Analyst / Viewer)
- Organization Isolation

### Event Ingestion

- Single Event API
- Batch Event API
- CSV Upload
- API Key Authentication
- Async Processing via Celery

### Analytics

- Dashboard Creation
- Widget Creation
- Dynamic Charts
- Real-time Aggregation

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

## Setup

```bash
docker compose up --build
```
