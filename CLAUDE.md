# CLAUDE.md

Guidance for Claude Code working in this repo. **Gamified skills-assessment tool:
Vue 3 + TypeScript frontend, FastAPI + sync SQLAlchemy + SQLite backend.**
Package managers: **uv** (backend, never pip) and **pnpm** (frontend, never npm).
Orchestration via **Task** (`task --list`).

This file is about **how to work here**. Reference material (architecture,
patterns, deploy, infra) lives in [docs/](docs/) — load it when a task needs it,
not before.

---

## How to work here

Match planning depth to task size — a one-file fix needs a sentence, not a plan.

### Think before coding
- State assumptions explicitly. If uncertain, **ask** — don't guess and run.
- If multiple interpretations exist, surface them; don't silently pick one.
- If you see a simpler or better approach, say so. **Push back when warranted.**

### Simplicity first
- Minimum code that solves the problem. Nothing speculative.
- **Reuse before reinventing** — search for an existing component, composable,
  service, or helper to extend first.
- No abstractions for single-use code; no config nobody asked for.

### Surgical changes
- Every changed line should trace to the request.
- Match existing style. Don't refactor what isn't broken.
- Notice unrelated dead code? Mention it — don't delete it unasked.

### Evidence before claims
- Run it before you say it works (see [Verification](#verification)).
- If tests fail, say so with the output. If you skipped a step, say that.

---

## Non-negotiables for this codebase

- **Layering, no skipping:** `route → service → dao factory → dao`. Business
  logic only in services; queries only in DAOs; routes stay thin.
- **Logging:** always the shared struct logger —
  `from app.core.config import settings; logger = settings.logger` with
  structured kwargs (`logger.info("Created question", question_id=q.id)`).
  Never `print`, never `logging.getLogger()`. Routes to Sentry when
  `SENTRY_DSN` is set.
- **Defensive DB/IO:** try/except around DB and external calls; rollback then
  **bare `raise`** (preserves tracebacks). Log errors with `exc_info=True`.
- **Types everywhere:** Python type hints; strict TypeScript — no `any` in new code.
- **Frontend:** Composition API (`<script setup>`); componentize; mobile-first;
  verify **both themes** (terminal + stiff mode).
- **Secrets never in git:** they live in 1Password
  (`SKILL-TREE-LOCAL/-PROD/-INFRA`); `.env*` and `prod.tfvars` are generated
  locally (`task env:generate`, `task tf:gen`) and gitignored. Only `VITE_`
  (public) vars go to the frontend.
- **Never push directly to `main`.** Branch, PR, let CI run.

Patterns and code templates: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Orientation

- **Backend** (`backend/app/`): `core/config.py` settings+logger · `routes/` ·
  `services/` · `dao/` (factory) · `models/` (self-referencing question tree) ·
  `schemas/` · `seeders/`. SQLite on a named Docker volume.
- **Frontend** (`frontend/src/`): `views/` · `components/` · `composables/` ·
  `api/` (axios) · `types/`. Tailwind v4, two themes in `style.css`.
- **Deploy model:** merge to `main` → GHCR image (arm64) → Watchtower
  auto-pulls on the EC2 (~5 min). Frontend auto-deploys via Cloudflare Workers Builds. TLS via
  Cloudflare Tunnel — no certs, no inbound ports except SSH.
- **Infra:** one EC2 (Terraform-managed, `infrastructure/terraform/`) +
  Cloudflare (DNS + tunnel + Workers frontend).

---

## Where to find things

Don't memorize these — open the doc when the task touches it.

| Task touches… | Doc |
|-------|-----|
| Patterns, layering, theming, system diagram | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Deploys, secrets rotation, rollback, monitoring | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| EC2 host, tunnel, security group, backups | [docs/AWS_SETUP.md](docs/AWS_SETUP.md) |
| Provisioning/changing the EC2 (Terraform) | [infrastructure/terraform/README.md](infrastructure/terraform/README.md) |
| One-time go-live steps (mostly done) | [docs/GO_LIVE_CHECKLIST.md](docs/GO_LIVE_CHECKLIST.md) |
| DB schema + indexes | [docs/database_schema.sql](docs/database_schema.sql) |
| Env vars + quick start + API overview | [README.md](README.md) |
| Dev workflow, branch/commit conventions | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Commands | `Taskfile.yml` + `tasks/*.yml` — read them, don't memorize |

---

## Docs follow the code

Before finishing any task ask: **does this change make a doc wrong, or create
something a future task needs to know?** If yes, update docs **in the same PR**.
Renamed something? `grep -rn "<old-name>" --include='*.md' .` and fix every hit.
Skip docs for bug fixes/refactors that change no documented claim.

---

## Common tasks

- **Run locally:** `task dev` (backend in Docker + Vite). Backend alone:
  `task start`; frontend alone: `task fe`. No `.env` needed — safe defaults.
- **Add endpoint:** schema → route → service → DAO if needed → tests.
- **Add a setting:** field in `app/core/config.py` → 1Password item →
  `task env:generate`.
- **Deploy code:** merge PR to `main`. That's it (Watchtower + Workers Builds).
- **Deploy secrets/config:** edit 1Password → `task prod:deploy`.
  See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).
- **Change infra:** edit Terraform → `task tf:plan` → `task tf:apply`.

---

## Verification

```bash
task test                                            # backend pytest (in container)
cd backend && uv run ruff check . && uv run ruff format --check .
cd frontend && pnpm lint && pnpm typecheck && pnpm build
```

CI runs exactly these on every PR.

---

**Update this file when behavior/architecture changes — keep it short; push
reference detail to docs/.**
