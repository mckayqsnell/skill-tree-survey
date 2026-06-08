# Skill Tree Survey

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/HEAL-Engineering/skill-tree-survey/actions/workflows/ci.yml/badge.svg)](https://github.com/HEAL-Engineering/skill-tree-survey/actions/workflows/ci.yml)

A gamified employee skills assessment tool that uses **branching question logic** to
map technical competencies across an organization. Answer "yes" to a skill and the
survey drills deeper; answer "no" and it prunes that branch — so a broad assessment
stays fast. Built with Vue 3 + TypeScript on the front end, FastAPI + SQLite on the
back end, and a retro terminal UI (with a clean "stiff mode" alternative).

## Features

- **Branching survey** — a self-referencing question tree; depth signals expertise.
- **Keyboard-driven** — Space/Enter for YES, `N` for NO; optimized for speed.
- **Admin dashboard** — full CRUD for questions, drag-and-drop category ordering,
  session analytics (radar charts, skill-depth analysis, abandonment rate).
- **Two themes** — retro terminal (green-on-black) and an Apple-style "stiff mode".
- **Zero-config local data** — ~420 seed questions across categories (Backend,
  Frontend, DevOps, Cloud, Data, ML, Security, Architecture, Testing, Leadership, …)
  auto-seed on first run.

## Tech stack

| Layer | Tech |
|-------|------|
| Frontend | Vue 3 (Composition API), TypeScript, Vite, Tailwind v4, vue-router |
| Backend | FastAPI, SQLAlchemy 2 (sync), Pydantic v2, SQLite |
| Tooling | [uv](https://docs.astral.sh/uv/) (Python), [pnpm](https://pnpm.io/) (Node), [Task](https://taskfile.dev/) (orchestration), [1Password CLI](https://developer.1password.com/docs/cli/) (secrets) |
| Observability | Sentry via `sentry-struct-logger` (structured logging) |
| Deploy | Frontend → Vercel · Backend → Docker on AWS EC2, image from GHCR, auto-updated by [Watchtower](https://github.com/nicholas-fedor/watchtower), TLS via [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) |

## Architecture

```
                Browser
                   │
        ┌──────────┴───────────┐
        ▼                      ▼
   Vercel (SPA)        Cloudflare Tunnel  ──TLS at edge──┐
   Vue 3 + Vite                                          │ outbound-only
        │  VITE_API_URL                                  ▼
        └──────── HTTPS ───────────────────►  EC2 (Graviton / AL2023)
                                                 ├─ cloudflared  (tunnel)
                                                 ├─ backend      (FastAPI, :8000)
                                                 └─ watchtower   (auto-pull GHCR)
                                                        │
                                              SQLite on a named volume
```

Code ships automatically: push to `main` → GitHub Actions builds the backend image
and pushes to GHCR → Watchtower on the EC2 pulls it within ~5 minutes. The frontend
auto-deploys from Vercel's Git integration. There is no SSH-based deploy step.

## Quick start (local)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Compose v2
- [Task](https://taskfile.dev/installation/) (`brew install go-task/tap/go-task`)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (backend, if running outside Docker)
- [Node 22.13+](https://nodejs.org/) and [pnpm 11](https://pnpm.io/installation) (via `corepack enable`) for the frontend
- _(optional)_ [1Password CLI](https://developer.1password.com/docs/cli/) — only if you want real secrets; the app ships safe local defaults without it.

### Run it

```bash
git clone https://github.com/HEAL-Engineering/skill-tree-survey.git
cd skill-tree-survey

task dev      # backend (Docker) + frontend (Vite dev server)
```

Or run the two halves separately:

```bash
task start    # backend only, in Docker (generates .env.local from 1Password if signed in)
task fe       # frontend dev server (Vite), proxies /api → localhost:8000
```

| URL | What |
|-----|------|
| <http://localhost:5173> | Frontend (survey) |
| <http://localhost:5173/admin> | Admin dashboard (default password `admin123`) |
| <http://localhost:8000/docs> | Backend API docs (Swagger) |
| <http://localhost:8000/health> | Health check |

### Without Docker

```bash
# Backend
cd backend && uv sync && uv run uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend && pnpm install && pnpm dev
```

Run `task` (or `task --list`) to see every available command.

## Configuration & secrets

Settings are plain environment variables, validated by Pydantic in
[backend/app/core/config.py](backend/app/core/config.py). Every field has a safe
default, so the app runs locally with **no `.env` file at all**.

Secrets are managed with **1Password**, not committed files. Each env var is one
1Password item (title = `VAR_NAME`, value in the password field). `task env:generate`
pulls a vault into a local `.env.<env>` file:

```bash
task env:setup            # one-time: install 1Password CLI + sign in
task env:generate         # writes .env.local from the SKILL-TREE-LOCAL vault
task env:generate ENV=prod  # writes .env.prod from SKILL-TREE-PROD (used by deploy)
```

Key backend variables:

| Variable | Default | Notes |
|----------|---------|-------|
| `DATABASE_URL` | `sqlite:///./skill_survey.db` | SQLite path; container uses `/app/data/…` |
| `ADMIN_PASSWORD` | `admin123` | **Change in production.** Sent by the admin UI as the `X-Admin-Password` header |
| `CORS_ORIGINS` | localhost dev origins | JSON array or comma-separated list |
| `ENVIRONMENT` | `development` | `production` enables prod logging behavior |
| `SENTRY_DSN` | _unset_ | Leave empty to disable Sentry (local logs to stdout) |
| `RESET_DATABASE` | `false` | If `true`, drops + reseeds on startup |

The frontend uses only **public** `VITE_` variables (never put secrets here):
`VITE_API_URL` (backend base URL) and `VITE_CLOUDFRONT_URL` (icon-asset host).

## Project structure

```
backend/
├── app/
│   ├── core/config.py   # Pydantic settings + shared Sentry logger
│   ├── dao/             # Data access layer (factory pattern)
│   ├── services/        # Business logic
│   ├── routes/          # API endpoints (questions, sessions, responses, categories, admin)
│   ├── models/          # SQLAlchemy models (self-referencing question tree)
│   ├── schemas/         # Pydantic request/response validation
│   └── seeders/         # initial_questions.json + seeding logic
├── tests/               # pytest
├── Dockerfile           # multi-stage: builder → dev → runtime
└── pyproject.toml       # uv-managed deps + ruff + pytest config
frontend/
├── src/
│   ├── views/           # Page components (Survey, Admin, SessionStats)
│   ├── components/       # Reusable UI (admin/, shared)
│   ├── composables/      # useAdminAuth, etc.
│   ├── api/             # Axios client + per-resource modules
│   └── types/           # TypeScript definitions
└── vercel.json          # Vite SPA config for Vercel
infrastructure/terraform/ # IaC for the prod EC2 (see its README)
tasks/                    # Task includes: env, helpers, prod
docs/                     # Deployment, AWS, go-live runbook, DB schema
```

## API overview

All routes are prefixed with `/api`. Full interactive docs at `/docs`.

```http
# Public
POST   /api/sessions                      # start a survey session
GET    /api/questions/base                # top-level questions
GET    /api/questions/{id}/children       # branch deeper
POST   /api/responses                     # record an answer
POST   /api/sessions/{id}/complete        # finish a session
GET    /api/sessions/{id}/summary         # session results

# Admin (header: X-Admin-Password: <ADMIN_PASSWORD>)
GET    /api/admin/sessions                # all sessions
GET    /api/admin/analytics               # aggregate stats
POST   /api/admin/questions               # CRUD questions
PUT    /api/admin/questions/move          # re-parent in the tree
PUT    /api/admin/categories/order        # drag-and-drop ordering
DELETE /api/admin/sessions/{id}
```

## Development

```bash
task test                 # backend tests (pytest, in the container)
cd backend && uv run ruff check . && uv run ruff format --check .
cd frontend && pnpm lint && pnpm typecheck && pnpm build
```

CI ([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs the backend lint/format/tests
and the frontend lint/typecheck/build on every PR.

## Deployment

- **Overview & runbook:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Infrastructure (Terraform):** [infrastructure/terraform/README.md](infrastructure/terraform/README.md)
- **EC2 + Cloudflare Tunnel setup:** [docs/AWS_SETUP.md](docs/AWS_SETUP.md)
- **First-time go-live (manual steps):** [docs/GO_LIVE_CHECKLIST.md](docs/GO_LIVE_CHECKLIST.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch/commit conventions, local
setup, and PR process. For deeper architecture and conventions, see
[CLAUDE.md](CLAUDE.md).

## License

[MIT](LICENSE) © HEAL USA Inc.
