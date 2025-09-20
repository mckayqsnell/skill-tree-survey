# Skill Tree Survey

Gamified skills assessment tool with branching logic. Built with Vue 3, TypeScript, FastAPI, SQLite.

## Quick Start

```bash
# Clone and run
git clone https://github.com/HEAL-Engineering/skill-tree-survey.git
cd skill-tree-survey
docker-compose up

# Access
http://localhost:5173      # Frontend
http://localhost:8000/docs  # API docs
```

Admin panel: `http://localhost:5173/admin` (password: `admin123`)

## Project Structure

```
backend/
├── app/
│   ├── dao/        # Data access layer (factory pattern)
│   ├── services/   # Business logic
│   ├── routes/     # API endpoints
│   ├── models/     # SQLAlchemy models
│   └── schemas/    # Pydantic validation
frontend/
├── src/
│   ├── views/      # Page components
│   ├── components/ # Reusable UI components
│   ├── api/        # API client layer
│   └── types/      # TypeScript definitions
```

## Development

### Prerequisites
- Docker & Docker Compose
- Git

### Setup
```bash
# Start development environment
docker-compose up

# Reset database (fresh start)
docker-compose down -v && docker-compose up

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Key Files
- **Backend config**: `/backend/app/config/settings.py`
- **Database schema**: `/docs/database_schema.sql`
- **Environment vars**: `/environments/.env.development`
- **API routes**: `/backend/app/routes/`

## Contributing

**READ FIRST**: [CONTRIBUTING.md](./CONTRIBUTING.md) - Branching strategy and workflow

### Branch Format
```
<username>/<ticket-id>/<feature-name>
Example: nate/HEA-123/add-dashboard
```

### Workflow
1. Branch from `develop`
2. Make changes
3. PR to `develop` → Auto-deploys to test
4. PR to `main` → Manual deploy to production

### Commit Format
```bash
feat: add new feature
fix: resolve bug
docs: update documentation
refactor: code restructuring
```

## API Overview

### Public Endpoints
```bash
POST   /api/sessions         # Start survey
GET    /api/questions/base   # Get base questions
GET    /api/questions/{id}/children
POST   /api/responses/session/{id}
GET    /api/sessions/{id}/summary
```

### Admin Endpoints (Header: `X-Admin-Password: admin123`)
```bash
GET    /api/admin/sessions   # All sessions
GET    /api/admin/analytics  # Stats
POST   /api/admin/questions  # CRUD operations
DELETE /api/admin/sessions/{id}
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic, SQLite
- **Frontend**: Vue 3 (Composition API), TypeScript, Vite, Tailwind
- **Infrastructure**: Docker, Nginx, GitHub Actions

## Deployment

- **Test**: Auto-deploys on merge to `develop`
  - URL: https://test-skills-survey.heal.engineering
- **Production**: Manual trigger after merge to `main`
  - URL: https://skills-survey.heal.engineering
  - See [DEPLOYMENT.md](./docs/DEPLOYMENT.md)

## Environment Variables

### Backend
```bash
DATABASE_URL=sqlite:////app/data/skill_survey.db
ADMIN_PASSWORD=admin123  # Change in production!
CORS_ORIGINS=["http://localhost:5173"]
API_PREFIX=/api
```

### Frontend
```bash
VITE_API_URL=http://localhost:8000
VITE_ADMIN_PASSWORD=admin123
```

## Common Tasks

### Add Questions
1. Admin panel → Questions tab
2. Or edit `/backend/app/seeders/initial_questions.json`

### View Analytics
Admin panel → Analytics tab

### Debug Issues
```bash
# Check container status
docker-compose ps

# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Database queries
sqlite3 backend/skill_survey.db
```

## Testing

```bash
# Run backend tests
docker-compose exec backend pytest

# Run frontend tests
docker-compose exec frontend npm test
```

## Documentation

- [Contributing Guidelines](./CONTRIBUTING.md) - **Start here**
- [Deployment Pipeline](./docs/DEPLOYMENT.md)
- [Workflow Examples](./docs/WORKFLOW_EXAMPLES.md)
- [Database Schema](./docs/database_schema.sql)
- [AWS Setup](./docs/AWS_SETUP.md)
- [Development Guide](./CLAUDE.md) - Comprehensive project reference

## Troubleshooting

### Containers not starting
```bash
docker-compose down -v  # Clear everything
docker-compose up --build
```

### Database issues
```bash
# Reset database
docker-compose down -v
docker-compose up
```

### Port conflicts
```bash
# Check what's using ports
lsof -i :5173  # Frontend
lsof -i :8000  # Backend

# Change ports in docker-compose.yml if needed
```

### Can't access admin panel
- Default password: `admin123`
- Check backend logs for auth errors
- Verify ADMIN_PASSWORD env var

## Contact

- GitHub Issues: [Report bugs](https://github.com/HEAL-Engineering/skill-tree-survey/issues)
- Team Slack: #skill-tree-survey

---

**For detailed development patterns and architecture decisions, see [CLAUDE.md](./CLAUDE.md)**