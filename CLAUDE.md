# Skill Tree Survey - Claude AI Development Guide

## 🚨 CRITICAL INSTRUCTIONS FOR CLAUDE

### **UPDATE THIS FILE AS YOU WORK**
When making significant structural changes, new features, or architectural decisions that would help future Claude sessions, update this file immediately. Don't wait until the end of the session.

### Core Development Principles
1. **Defensive Programming**: ALWAYS use try-catch/try-except blocks with proper error handling
2. **Logging**: Use the shared structured logger — `from app.core.config import settings; logger = settings.logger` — with structured kwargs (e.g. `logger.info("Created question", question_id=q.id)`). It routes to Sentry when `SENTRY_DSN` is set. Never use `print`.
3. **Type Safety**: Use TypeScript strictly in frontend, type hints in Python backend
4. **Componentization**: Break down UI into reusable components, especially in frontend
5. **Separation of Concerns**: Follow DAO → Service → Route pattern in backend
6. **Single Responsibility**: Each function/component should do ONE thing well
7. **Error Recovery**: Graceful error handling with user feedback

## 📁 Project Overview

A gamified employee skills assessment tool that uses branching question logic to efficiently map technical competencies across an organization. Built with Vue 3, TypeScript, FastAPI, and a retro-futuristic terminal UI theme.

### Key Features
- **Branching Survey Logic**: Tree-structured questions where "yes" leads deeper
- **Keyboard-Driven**: Space/Enter for YES, 'N' for NO - optimized for speed
- **Admin Dashboard**: Full CRUD for questions, session analytics, drag-and-drop category ordering
- **Real-time Analytics**: Radar charts, skill depth analysis, performance metrics
- **Session Management**: Individual session analysis, bulk operations, data cleanup
- **Responsive Design**: Mobile-optimized with touch support
- **Stiff Mode**: Professional Apple-style UI alternative to terminal theme

## 🏗️ Architecture & Patterns

### Backend Architecture (FastAPI + SQLAlchemy)

```
backend/
├── app/
│   ├── core/             # Settings + shared logger
│   │   └── config.py     # Pydantic settings; Sentry struct logger as settings.logger
│   ├── database/         # Database configuration
│   │   └── connection.py # SQLAlchemy setup, Base class
│   ├── models/           # SQLAlchemy ORM models
│   │   ├── question.py   # Self-referencing tree structure
│   │   ├── session.py    # Survey session tracking
│   │   ├── response.py   # Individual answers
│   │   └── category_order.py # Display ordering
│   ├── schemas/          # Pydantic validation schemas
│   ├── dao/              # Data Access Objects (database layer)
│   │   ├── factory.py    # DAO Factory pattern
│   │   ├── base.py       # Generic CRUD operations
│   │   └── [model]_dao.py # Model-specific queries
│   ├── services/         # Business logic layer
│   │   └── [model]_service.py # Business rules, validation
│   ├── routes/           # API endpoints (questions, sessions, responses, categories, admin)
│   │   ├── questions.py  # Public question endpoints
│   │   ├── admin.py      # Protected admin endpoints
│   │   └── [...]         # Other route modules
│   └── seeders/          # Database initialization
│       └── initial_questions.json # ~420 seed questions across categories
├── tests/                # pytest (uv run pytest / task test)
├── Dockerfile            # multi-stage: builder → dev → runtime
└── pyproject.toml        # uv-managed deps, ruff, pytest config
```

#### Backend Patterns & Best Practices

**DAO Factory Pattern**:
```python
# Always use factory for DAO access
dao_factory = DAOFactory(db)
question_dao = dao_factory.get_question_dao()

# Proper error handling in DAOs
try:
    result = question_dao.create(data)
    dao_factory.commit()
    logger.info(f"Created question: {result.id}")
except Exception as e:
    dao_factory.rollback()
    logger.error(f"Failed to create question: {str(e)}")
    raise
```

**Service Layer Pattern**:
```python
# Services handle business logic
class QuestionService:
    def __init__(self, dao_factory: DAOFactory):
        self.dao_factory = dao_factory
        self.question_dao = dao_factory.get_question_dao()

    def create_question(self, data: QuestionCreate):
        try:
            # Business validation
            if data.parent_id:
                parent = self.question_dao.get(data.parent_id)
                if not parent:
                    raise HTTPException(404, "Parent not found")

            # Create with logging
            question = self.question_dao.create(**data.dict())
            logger.info(f"Question created: {question.id}")
            return question
        except Exception as e:
            logger.error(f"Service error: {str(e)}")
            raise
```

### Frontend Architecture (Vue 3 + TypeScript)

```
frontend/
├── src/
│   ├── api/              # API client layer
│   │   ├── client.ts     # Axios setup, interceptors, logging
│   │   ├── questions.ts  # Question-specific API calls
│   │   └── [...]         # Other API modules
│   ├── components/       # Reusable UI components
│   │   ├── admin/        # Admin-specific components
│   │   │   ├── AnalyticsDashboard.vue
│   │   │   ├── CategoryOrderManager.vue
│   │   │   ├── QuestionTreeItem.vue
│   │   │   └── SessionsTable.vue
│   │   └── [...]         # Other shared components
│   ├── views/            # Page-level components
│   │   ├── SurveyView.vue    # Main survey interface
│   │   ├── AdminView.vue     # Admin dashboard
│   │   └── SessionStatsView.vue # Individual session analysis
│   ├── composables/      # Shared Vue composition functions
│   │   └── useAdminAuth.ts # Authentication state management
│   ├── types/            # TypeScript type definitions
│   │   └── index.ts      # Centralized types
│   └── style.css         # Global styles (Tailwind v4 import + theme layers)
├── vercel.json           # Vite SPA config for Vercel
└── package.json          # pnpm-managed deps (Vue 3, Vite, Tailwind v4)
```

## 📊 Database Schema

See `/docs/database_schema.sql` for complete SQL schema with indexes and sample queries.

### Core Tables
1. **questions**: Self-referencing tree structure with categories
2. **survey_sessions**: User session tracking with timestamps
3. **responses**: Individual answers linking sessions to questions
4. **category_orders**: Display ordering for report categories

### Key Relationships
- Questions → Questions (parent-child tree)
- Sessions → Responses (one-to-many)
- Questions → Responses (one-to-many)
- Unique constraint: One response per question per session

## 🐳 Docker & Deployment

Full details in [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md). Quick model:

### Secrets & environment

No committed `.env` files. Secrets live in **1Password** (vaults `SKILL-TREE-LOCAL`,
`SKILL-TREE-PROD`); `task env:generate [ENV=local|prod]` writes `.env.<env>`. Every
setting has a safe default in `app/core/config.py`, so the app runs locally with no
`.env` at all. Non-secret project constants live in the committed `.setup.config`.

Internal infra IDs (VPC/subnet, AWS account, old instance/SG) live in a third vault,
**`SKILL-TREE-INFRA`** — `task tf:gen` writes the **gitignored**
`infrastructure/terraform/environments/prod.tfvars` from items tagged `tfvar`
(titles lowercased). These are Terraform inputs only; they are **not** part of
`.env.prod`. Only `prod.tfvars.example` is committed.

### Docker Compose

- `docker-compose.yml`: local **backend only** (`target: dev`, hot-reload, named
  `sqlite_data` volume). The frontend runs separately via `pnpm dev` (`task fe`).
- `docker-compose.prod.yml`: production stack — `backend` (GHCR image) + `cloudflared`
  (Cloudflare Tunnel, TLS at the edge) + `watchtower` (auto-pull from GHCR). No nginx.

### Key Environment Variables
```bash
# Backend (see app/core/config.py for the full list + defaults)
DATABASE_URL=sqlite:////app/data/skill_survey.db
ADMIN_PASSWORD=admin123        # CHANGE IN PRODUCTION (sent as X-Admin-Password header)
CORS_ORIGINS=["http://localhost:5173"]
ENVIRONMENT=development
SENTRY_DSN=                     # unset locally → logs to stdout only
RESET_DATABASE=false
API_PREFIX=/api

# Frontend (public VITE_ vars only — NEVER secrets)
VITE_API_URL=http://localhost:8000
VITE_CLOUDFRONT_URL=           # icon-asset host
```

### TLS / routing — Cloudflare Tunnel (no nginx, no certs)
The `cloudflared` container opens an outbound tunnel; Cloudflare terminates TLS at
its edge and routes the public hostname to `backend:8000`. The only inbound port on
the EC2 is SSH. TLS certs are never managed on the box.

## 🚀 GitHub Actions Workflows

### CI (`ci.yml`)
- Triggers: PRs to `main`/`develop` (+ manual)
- Backend: `uv sync` → `ruff check` → `ruff format --check` → `pytest`
- Frontend: `pnpm lint` → `pnpm typecheck` → `pnpm build`

### Build and Push (`build-and-push.yml`)
- Triggers: push to `main` (paths `backend/**`) + manual
- Builds the **linux/arm64** backend image, pushes to GHCR (`:latest` + `:prod-<sha>`)
- Watchtower on the EC2 pulls `:latest` within ~5 min → auto-deploy

### Cleanup Old Images (`cleanup-images.yml`)
- Triggers: weekly (Sun 02:00 UTC) + manual
- Keeps the last 5 `prod-*` images, deletes the rest + untagged layers

### Claude PR Review (`claude-pr-review.yml`)
- Org-synced; AI review on PRs

> Frontend deploys via **Vercel's Git integration** (no Action). There is no
> SSH-based deploy workflow — code ships through GHCR + Watchtower.

## 🎨 Styling & UI

### Design System
- **Terminal Theme**: Green-on-black retro-futuristic
- **Stiff Mode**: Clean Apple-style professional theme
- **Responsive**: Mobile-first with Tailwind breakpoints
- **Animations**: Smooth transitions, no jarring movements

### Global Styles Location
- `/frontend/src/style.css`: Main styles, theme definitions
- Component-scoped styles: Use `<style scoped>` in .vue files
- Tailwind utilities: Use inline classes for common patterns

### Key CSS Classes
```css
/* Text colors */
.text-primary       /* Green in terminal, gray in stiff */
.text-accent        /* Amber in terminal, blue in stiff */
.text-danger        /* Red in both themes */

/* Buttons */
.btn-primary        /* Primary action button */
.btn-secondary      /* Secondary action button */
.btn-view-stats     /* Smaller utility button */

/* Containers */
.glass-card         /* Main content container */
.analytics-card     /* Stats container */
.stat-card          /* Metric display */
```

## 📝 Development Workflow

### Git Branching Strategy
```
feature/<username>/<ticket>/<description> → develop → main → build + auto-deploy
                                                                ↓
                                          GHCR + Watchtower (backend) · Vercel (frontend)
```

### Branch Naming
- Format: `<username>/<ticket-id>/<feature-name>`
- Example: `nate/HEA-123/add-user-dashboard`

### Commit Message Format
```bash
feat: add new feature
fix: resolve bug
docs: update documentation
style: formatting changes
refactor: code restructuring
test: add tests
chore: maintenance
```

## 🔍 Common Patterns to Follow

### Error Handling Pattern
```python
# Backend
try:
    result = await some_operation()
    logger.info(f"Operation successful: {result.id}")
    return result
except ValidationError as e:
    logger.warning(f"Validation error: {e}")
    raise HTTPException(400, str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise HTTPException(500, "Internal server error")
```

```typescript
// Frontend
try {
  const data = await api.fetchData()
  logger.info('Data fetched successfully')
  return data
} catch (error) {
  logger.error('Failed to fetch data', error)
  // Show user-friendly error
  showNotification('Failed to load data. Please try again.')
  throw error
}
```

### Component Creation Pattern
```vue
<!-- New component checklist -->
1. Check existing components for similar functionality
2. Define props and emits with TypeScript types
3. Use Composition API (script setup)
4. Extract reusable logic to composables
5. Add proper logging for debugging
6. Include loading and error states
7. Make it responsive (mobile-first)
8. Test with both themes (terminal and stiff mode)
```

## 🛠️ Useful Commands

### Development
```bash
task dev                 # backend (Docker) + frontend (Vite) together
task start               # backend only (Docker); generates .env.local from 1Password if signed in
task fe                  # frontend dev server (Vite)
task logs                # tail backend container logs
task test                # backend tests (pytest in the container)
task down                # stop the dev environment
task clean:all           # wipe containers, volumes, images, caches

# Backend, outside Docker
cd backend && uv sync && uv run uvicorn app.main:app --reload
cd backend && uv run ruff check . && uv run pytest

# Reset the local DB: RESET_DATABASE=true on the backend, or `task down` then remove the volume
```

### Production
Code deploys automatically (push to `main` → GHCR → Watchtower). You do NOT deploy
code by hand. `task prod:*` is only for config/secrets and inspection:
```bash
task prod:deploy:dry-run # preview
task prod:deploy         # regenerate .env.prod from 1Password, ship + restart on the EC2
task prod:status         # docker compose ps on the EC2
task prod:logs           # tail backend logs on the EC2

task tf:gen              # write gitignored prod.tfvars from 1Password (SKILL-TREE-INFRA)
task tf:plan             # terraform plan (auto-generates tfvars if missing)
task tf:apply            # terraform apply

# Rollback: pin backend image to :prod-<good-sha> in docker-compose.prod.yml, then task prod:deploy
# (see docs/DEPLOYMENT.md)
```

## 📚 Important Files Reference

### Configuration Files
- `/backend/app/core/config.py` - Pydantic settings + shared Sentry logger
- `/.setup.config` - Non-secret project constants (vault prefix, app name, port)
- `/Taskfile.yml` + `/tasks/*.yml` - Task runner (env, helpers, prod)
- `/docker-compose.yml` - Local backend orchestration
- `/docker-compose.prod.yml` - Production stack (backend + cloudflared + watchtower)
- `/infrastructure/terraform/` - Prod EC2 infrastructure as code

### Database
- `/docs/database_schema.sql` - Complete SQL schema
- `/backend/app/models/` - SQLAlchemy models
- `/backend/app/seeders/initial_questions.json` - Seed data

### API Documentation
- Backend Swagger: `http://localhost:8000/docs`
- API routes: `/backend/app/routes/`
- Schemas: `/backend/app/schemas/`

### Frontend Entry Points
- `/frontend/src/main.ts` - App initialization
- `/frontend/src/router/index.ts` - Route definitions
- `/frontend/src/views/` - Page components
- `/frontend/src/api/client.ts` - API client setup

## 🚨 Critical Reminders

1. **ALWAYS UPDATE THIS FILE** when making structural changes
2. **Use proper error handling** - try/catch everywhere
3. **Add logging** for debugging - logger.info(), logger.error()
4. **Componentize** - Don't create monolithic components
5. **Type everything** - No 'any' types in TypeScript
6. **Test on mobile** - Responsive design is required
7. **Check both themes** - Terminal and stiff mode compatibility
8. **Review Docker configs** before deployment changes
9. **Document API changes** in schemas and routes
10. **Maintain backwards compatibility** when updating APIs

## 🔄 Recent Updates Log

### 2026-06 — Modernization & open-source prep
- Backend → **uv** + `pyproject.toml`; settings moved to `app/core/config.py` with the
  Sentry struct logger exposed as `settings.logger`. Kept sync SQLAlchemy + SQLite.
- Frontend **npm → pnpm**, **Tailwind v3 → v4**, latest Vue/Vite/TS; deploys to **Vercel**.
- Adopted **Taskfile** + **1Password**-backed secrets (`task env:generate`); no committed `.env`.
- Prod simplified: **Cloudflare Tunnel** (dropped nginx/certbot) + **Watchtower** auto-pull
  from **GHCR**; dropped the test environment.
- Added **Terraform** IaC for the prod EC2 (`infrastructure/terraform/`).
- Workflows: `ci.yml`, `build-and-push.yml` (arm64), `cleanup-images.yml`; removed the
  SSH-deploy workflows.
- Added **MIT LICENSE** (HEAL USA Inc.) + docs overhaul for open-sourcing.

### 2024-09-19
- Added dynamic category ordering with drag-and-drop admin interface
- Fixed mobile responsiveness issues in admin panel
- Improved analytics with abandonment rate metric
- Added smooth transitions for UI elements (undo button)
- Fixed stiff mode styling inconsistencies
- Created comprehensive database schema documentation
- Updated CLAUDE.md with complete project guide

### Future Enhancements Planned
- [ ] CSV export functionality for analytics
- [ ] WebSocket support for real-time updates
- [ ] Redis integration for session management
- [ ] PostgreSQL migration path for scaling
- [ ] Advanced question branching conditions
- [ ] Multi-language support
- [ ] Email notifications for session completion
- [ ] API rate limiting
- [ ] Automated testing suite
- [ ] Performance monitoring dashboard

## 📖 Additional Documentation

- [README.md](./README.md) - Quick start + architecture
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Dev setup, conventions, PR process
- [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) - GHCR + Watchtower + Cloudflare pipeline
- [docs/AWS_SETUP.md](./docs/AWS_SETUP.md) - EC2 + Docker + Cloudflare Tunnel host
- [docs/GO_LIVE_CHECKLIST.md](./docs/GO_LIVE_CHECKLIST.md) - One-time go-live runbook
- [infrastructure/terraform/README.md](./infrastructure/terraform/README.md) - Provisioning the EC2
- [docs/database_schema.sql](./docs/database_schema.sql) - Database structure
- [LICENSE](./LICENSE) - MIT (HEAL USA Inc.)

---

**Remember**: This is a living document. Update it as the project evolves to help future Claude sessions be more effective!