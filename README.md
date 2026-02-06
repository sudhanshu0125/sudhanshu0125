# InfluencersPlace AI Lead Agent

Production-style full-stack platform for automated lead discovery, qualification, enrichment, storage, and outreach.

## Architecture
- **Frontend:** Next.js 14 + Tailwind dashboard (auth, lead table, scoring, approval, outreach actions).
- **Backend:** FastAPI service with modular agent pipeline.
- **Database:** SQLAlchemy-compatible DB (PostgreSQL in docker-compose, SQLite fallback local).
- **Automation:** APScheduler recurring jobs + manual trigger endpoint.
- **AI/Rule Logic:** Hybrid heuristic scoring with pluggable LLM provider settings.

## Features implemented
- Lead discovery from web search results (DuckDuckGo fallback, SerpAPI optional)
- Data extraction from public websites (email/phone parsing)
- Qualification score (0-100) and status (Hot/Warm/Cold)
- Deduplication on company + links
- JWT auth (register/login)
- Leads CRUD + filter/search
- Outreach trigger endpoint (email/message queue-ready state)
- Scheduled autonomous runs
- Dockerized deployment

## Quick start

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Full stack (Docker)
```bash
docker compose up --build
```

## API documentation
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Key endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/leads`
- `PATCH /api/leads/{lead_id}`
- `POST /api/agent/run`
- `POST /api/outreach/trigger`

## Notes for production hardening
- Add OAuth provider (Google/Microsoft)
- Replace heuristic scorer with LLM grader chain
- Add Redis queue + workers (Celery/RQ)
- Persist outreach logs + campaign templates
- Add observability (OpenTelemetry, Prometheus)
