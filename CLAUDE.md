# Skill Tree Survey - Claude AI Development Guide

## 🚨 CRITICAL INSTRUCTIONS FOR CLAUDE

### **UPDATE THIS FILE AS YOU WORK**
When making significant structural changes, new features, or architectural decisions that would help future Claude sessions, update this file immediately. Don't wait until the end of the session.

### Core Development Principles
1. **Defensive Programming**: ALWAYS use try-catch/try-except blocks with proper error handling
2. **Logging**: Use comprehensive logging (logger.info, logger.error, logger.debug) for debugging
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
│   ├── config/           # Environment settings
│   │   └── settings.py   # Pydantic settings management
│   ├── database/         # Database configuration
│   │   └── connection.py # SQLAlchemy setup, Base class
│   ├── models/           # SQLAlchemy ORM models
│   │   ├── question.py   # Self-referencing tree structure
│   │   ├── session.py    # Survey session tracking
│   │   ├── response.py   # Individual answers
│   │   └── category_order.py # Display ordering
│   ├── schemas/          # Pydantic validation schemas
│   │   └── [matching model schemas with validation]
│   ├── dao/              # Data Access Objects (database layer)
│   │   ├── factory.py    # DAO Factory pattern
│   │   ├── base.py       # Generic CRUD operations
│   │   └── [model]_dao.py # Model-specific queries
│   ├── services/         # Business logic layer
│   │   └── [model]_service.py # Business rules, validation
│   ├── routes/           # API endpoints
│   │   ├── questions.py  # Public question endpoints
│   │   ├── admin.py      # Protected admin endpoints
│   │   └── [...]         # Other route modules
│   └── seeders/          # Database initialization
│       └── initial_questions.json # 60+ seed questions
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
│   └── styles/           # Global styles
│       └── style.css     # Tailwind + custom styles
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

### Environment Files
```
environments/
├── .env.development     # Local development
├── .env.test           # Test environment
└── .env.production     # Production environment
```

### Docker Compose Configurations
- `docker-compose.yml`: Development with hot-reload
- `docker-compose.test.yml`: Test environment
- `docker-compose.prod.yml`: Production with nginx

### Key Environment Variables
```bash
# Backend
DATABASE_URL=sqlite:////app/data/skill_survey.db
ADMIN_PASSWORD=admin123  # CHANGE IN PRODUCTION!
CORS_ORIGINS=["http://localhost:5173"]
RESET_DATABASE=false
API_PREFIX=/api

# Frontend
VITE_API_URL=http://localhost:8000
VITE_ADMIN_PASSWORD=admin123
```

### Nginx Configuration
- SSL termination with Let's Encrypt
- Reverse proxy for frontend (port 80/443) and backend (/api)
- Security headers (CSP, X-Frame-Options, etc.)
- Health check endpoints

## 🚀 GitHub Actions Workflows

### PR Validation (`pr-validation.yml`)
- Triggers: PRs to main/develop
- Builds Docker images
- Runs health checks
- Posts status to PR

### Test Deployment (`deploy-test.yml`)
- Triggers: Push to develop (automatic)
- Deploys to test-skills-survey.heal.engineering
- Container names: test-skill-survey-*

### Production Deployment (`deploy-production.yml`)
- Triggers: Manual only
- Deploys to skills-survey.heal.engineering
- Requires approval
- Automatic backup before deployment

### Docker Cleanup (`docker-cleanup.yml`)
- Runs daily at 3 AM UTC
- Removes unused images/containers
- Cleans build cache
- Maintains last 5 deployment backups

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
feature/<username>/<ticket>/<description> → develop → main
                                                ↓        ↓
                                             Test Env  Production
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
# Start development environment
docker-compose up

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Reset database
docker-compose down -v && docker-compose up

# Run specific service
docker-compose up backend
```

### Production
```bash
# Deploy to production (after PR to main)
# Go to GitHub Actions → Deploy to Production → Run workflow

# SSH to production
ssh ec2-user@skills-survey.heal.engineering

# Check production logs
docker-compose -f docker-compose.prod.yml logs --tail=100

# Rollback if needed
docker tag skill-survey-backend:rollback skill-survey-backend:latest
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Important Files Reference

### Configuration Files
- `/backend/app/config/settings.py` - Environment configuration
- `/frontend/.env` - Frontend environment variables
- `/docker-compose.yml` - Development orchestration
- `/infrastructure/nginx/production.conf` - Production nginx

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

- [README.md](./README.md) - Quick start guide
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Development workflow
- [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) - CI/CD pipeline
- [docs/WORKFLOW_EXAMPLES.md](./docs/WORKFLOW_EXAMPLES.md) - Common scenarios
- [docs/database_schema.sql](./docs/database_schema.sql) - Database structure
- [docs/AWS_SETUP.md](./docs/AWS_SETUP.md) - Infrastructure setup

---

**Remember**: This is a living document. Update it as the project evolves to help future Claude sessions be more effective!