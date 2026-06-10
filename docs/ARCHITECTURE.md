# Architecture & Patterns

Reference for how the codebase is structured and the patterns to follow when
extending it. For how to *run* things see the [README](../README.md); for how
things *ship* see [DEPLOYMENT.md](DEPLOYMENT.md).

## System overview

```
        Browser
           │  https://skills-survey.heal.engineering   (frontend, CF Workers)
           │  https://skills-survey-api.heal.engineering (backend, via tunnel)
           ▼
   ① DNS — the heal.engineering zone is served by Cloudflare
           │   (registration stays at Namecheap; Cloudflare answers lookups)
           ▼
   ② Cloudflare edge (nearest datacenter)
        • terminates TLS (universal cert — nothing to renew, ever)
        • hostname → tunnel routing (the CNAME points at
          <tunnel-id>.cfargotunnel.com, a routing label, not a server)
           │
           ▼   ③ delivered DOWN persistent QUIC connections that
           │      cloudflared opened OUTBOUND from the box
   ┌───────┴────────────────────────────────────┐
   │  EC2 (Graviton/arm64) — inbound: SSH only  │
   │                                            │
   │   cloudflared ──▶ http://backend:8000      │   docker compose network
   │                      │                     │
   │                   FastAPI (uvicorn ×4)     │
   │                      │                     │
   │                   SQLite (named volume)    │
   │                                            │
   │   watchtower ──▶ polls GHCR, auto-updates  │
   └────────────────────────────────────────────┘
```

The key property: **nothing connects inbound to the server** — `cloudflared`
dials out and Cloudflare pushes requests down the open connections. No
80/443 in the security group, no certs on the box.

## Backend (FastAPI + sync SQLAlchemy + SQLite)

```
backend/
├── app/
│   ├── core/config.py    # Pydantic settings + shared Sentry struct logger
│   ├── database/         # connection.py — engine, SessionLocal, Base, init_db
│   ├── models/           # SQLAlchemy ORM (question.py is a self-referencing tree)
│   ├── schemas/          # Pydantic request/response validation
│   ├── dao/              # Data access — factory.py, base.py (generic CRUD), per-model DAOs
│   ├── services/         # Business logic (one service per model)
│   ├── routes/           # API endpoints: questions, sessions, responses, categories, admin
│   └── seeders/          # initial_questions.json (~420 questions) + seeder.py
├── tests/                # pytest
├── Dockerfile            # multi-stage: builder → dev → runtime (non-root, uvicorn ×4)
└── pyproject.toml        # uv-managed deps + ruff + pytest config
```

**Layering is strict:** `route → service → dao factory → dao`. Business logic
lives in services, queries in DAOs, HTTP/validation in routes.

### DAO factory pattern

```python
dao_factory = DAOFactory(db)
question_dao = dao_factory.get_question_dao()

try:
    result = question_dao.create(data)
    dao_factory.commit()
    logger.info("Created question", question_id=result.id)
except Exception:
    dao_factory.rollback()
    logger.error("Failed to create question", exc_info=True)
    raise   # bare raise — preserves the traceback
```

### Service layer pattern

```python
class QuestionService:
    def __init__(self, dao_factory: DAOFactory):
        self.dao_factory = dao_factory
        self.question_dao = dao_factory.get_question_dao()

    def create_question(self, data: QuestionCreate):
        if data.parent_id and not self.question_dao.get(data.parent_id):
            raise HTTPException(404, "Parent not found")
        question = self.question_dao.create(**data.model_dump())
        logger.info("Question created", question_id=question.id)
        return question
```

### Logging

Always the shared structured logger — never `print`, never `logging.getLogger()`:

```python
from app.core.config import settings
logger = settings.logger
logger.info("Something happened", session_id=session.id)   # structured kwargs
```

It logs to stdout locally and routes to Sentry when `SENTRY_DSN` is set.

### Admin auth

Admin routes require the `X-Admin-Password` header, checked with
`secrets.compare_digest` (constant-time) against `settings.ADMIN_PASSWORD`.
The app **refuses to boot in production** with the dev-default password.

### Startup behavior (multi-worker)

The runtime image runs `uvicorn --workers 4`; every worker executes the
lifespan (table init + seed-if-empty + cleanup). The seed/cleanup block is
wrapped so a worker that loses the SQLite write race logs a warning instead
of dying — keep that property when touching startup code.

## Frontend (Vue 3 + TypeScript + Vite + Tailwind v4)

```
frontend/
├── src/
│   ├── api/              # client.ts (axios, interceptors) + per-resource modules
│   ├── components/       # Reusable UI (admin/ for dashboard pieces)
│   ├── views/            # SurveyView, AdminView, SessionStatsView, CompleteView
│   ├── composables/      # useAdminAuth (sessionStorage + X-Admin-Password header)
│   ├── types/index.ts    # centralized TS types
│   └── style.css         # Tailwind v4 import + both theme layers
├── wrangler.jsonc        # Cloudflare Workers config (static assets, SPA routing)
└── package.json          # pnpm; packageManager pins the version
```

Only **public** `VITE_` vars exist (never secrets): `VITE_API_URL`,
`VITE_CLOUDFRONT_URL` (icon-asset host).

### New component checklist

1. Check existing components for similar functionality first
2. Props/emits typed; Composition API (`<script setup>`)
3. Extract reusable logic to composables
4. Include loading and error states
5. Responsive (mobile-first)
6. Verify in **both themes** — terminal and stiff mode

### Theming

Two themes, defined in `src/style.css`:

- **Terminal** — green-on-black retro (default)
- **Stiff mode** — clean Apple-style professional

Key classes: `.text-primary` / `.text-accent` / `.text-danger` (theme-aware
colors), `.btn-primary` / `.btn-secondary`, `.glass-card` / `.analytics-card`
/ `.stat-card` (containers). Use Tailwind utilities inline for everything else.

## Database

Full SQL + indexes: [database_schema.sql](database_schema.sql).

| Table | Role |
|-------|------|
| `questions` | self-referencing tree (parent_id) with categories |
| `survey_sessions` | one row per survey run |
| `responses` | answers; unique (session, question) |
| `category_orders` | drag-and-drop display ordering |

## API surface

All routes under `/api`; interactive docs at `/docs` on the backend.
Public: sessions/questions/responses CRUD for taking a survey.
Admin (`X-Admin-Password` header): question CRUD + tree moves, category
ordering, session analytics and cleanup. See [README](../README.md#api-overview)
for the endpoint list.
