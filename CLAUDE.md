# Skill Tree Survey - Project Context

## Project Overview
A gamified employee skills assessment tool that uses branching logic to efficiently map technical competencies across an organization. The survey is keyboard-driven, takes 5-10 minutes to complete, and provides organizations with a clear view of their technical talent portfolio.

## Core Functionality
- **Branching Survey Logic**: Questions form a tree structure where "yes" answers lead to deeper follow-up questions, while "no" answers return to the next base question
- **Keyboard Navigation**: Space/Enter for "yes", 'N' key for "no" - optimized for speed
- **Question Management**: Admin interface to create, edit, delete, and reorder questions while maintaining tree structure
- **Employee Tracking**: Store responses per session with user information
- **Skills Summary**: Admin view to see aggregated skills data per employee

## Technical Stack
- **Backend**: FastAPI with SQLAlchemy ORM, Pydantic for validation
- **Frontend**: Vue 3 (Composition API), TypeScript, Vite, Tailwind CSS
- **Database**: SQLite with SQLAlchemy
- **Deployment**: Docker Compose with persistent volumes

## Architecture Patterns
- **Backend Structure**: Factory pattern for DAOs, clear separation of concerns
  - `/app/routes/` - API endpoints
  - `/app/services/` - Business logic layer
  - `/app/dao/` - Data access layer with factory pattern
  - `/app/models/` - SQLAlchemy models
  - `/app/schemas/` - Pydantic schemas
  - `/app/config/` - Configuration and settings
- **Frontend Structure**: Single-page application with component-based architecture
  - Focus on single survey component for entire flow
  - Admin panel for question management

## Database Schema

```sql
-- Questions table with self-referencing for tree structure
questions:
  - id (PRIMARY KEY)
  - parent_id (FOREIGN KEY -> questions.id, nullable)
  - text (TEXT, required)
  - is_base (BOOLEAN, default false)
  - category (VARCHAR, nullable) 
  - order_index (INTEGER)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)

-- Survey session tracking
survey_sessions:
  - id (PRIMARY KEY)
  - user_name (VARCHAR)
  - user_email (VARCHAR) 
  - company (VARCHAR)
  - started_at (TIMESTAMP)
  - completed_at (TIMESTAMP, nullable)

-- Individual responses
responses:
  - id (PRIMARY KEY)
  - session_id (FOREIGN KEY -> survey_sessions.id)
  - question_id (FOREIGN KEY -> questions.id)
  - answer (BOOLEAN)
  - answered_at (TIMESTAMP)
```

## API Routes

### Public Routes
- `POST /api/sessions` - Start new survey session with user info
- `GET /api/questions/base` - Get all base questions
- `GET /api/questions/{id}/children` - Get child questions for a parent
- `POST /api/responses` - Submit answer for a question
- `GET /api/sessions/{id}/summary` - Get session results

### Admin Routes (password protected)
- `GET /api/admin/questions` - Get all questions in tree structure
- `POST /api/admin/questions` - Create new question
- `PUT /api/admin/questions/{id}` - Update question (text, parent, order)
- `DELETE /api/admin/questions/{id}` - Delete question and children
- `PUT /api/admin/questions/reorder` - Bulk update order_index
- `GET /api/admin/sessions` - Get all sessions with responses
- `GET /api/admin/analytics` - Get aggregated skills data

## Key Features to Implement

### Phase 1 (MVP)
- [x] Basic backend structure with proper separation of concerns
- [x] Database models and migrations
- [x] Seeder for initial questions
- [x] CRUD operations for questions
- [x] Session and response tracking
- [ ] Basic Vue frontend with survey flow
- [ ] Keyboard navigation
- [ ] Docker Compose setup

### Phase 2 (Enhanced)
- [ ] Drag-and-drop question reordering
- [ ] Question categories
- [ ] Admin dashboard with analytics
- [ ] Export functionality (CSV)
- [ ] Response time tracking
- [ ] Bulk question import

## Configuration

### Backend Environment Variables
- `DATABASE_URL`: SQLite connection string (default: sqlite:///./skill_survey.db)
- `ADMIN_PASSWORD`: Simple password for admin routes
- `CORS_ORIGINS`: Allowed origins for frontend (default: http://localhost:5173)
- `SEED_ON_STARTUP`: Whether to seed database if empty (default: true)

### Frontend Environment Variables
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)
- `VITE_ADMIN_PASSWORD`: Admin password for protected routes

## Development Guidelines

### Code Style
- Use type hints throughout Python code
- Implement proper error handling with meaningful HTTP status codes
- Use Pydantic schemas for all request/response models
- Keep business logic in service layer, not in routes
- Use TypeScript strictly in frontend
- Follow Vue 3 Composition API best practices

### Testing Approach
- Unit tests for service layer
- Integration tests for DAOs
- API tests for routes
- Component tests for Vue components

## Seeder Data Structure

```json
{
  "categories": ["DevOps", "Backend", "Frontend", "Data"],
  "questions": [
    {
      "text": "Have you worked with Kubernetes?",
      "is_base": true,
      "category": "DevOps",
      "children": [
        {
          "text": "Have you deployed production workloads?",
          "children": [
            {
              "text": "Have you managed clusters with 100+ nodes?"
            }
          ]
        }
      ]
    }
  ]
}
```

## Docker Deployment

The application uses Docker Compose with:
- Backend service (FastAPI on port 8000)
- Frontend service (Vite dev server on port 5173)
- SQLite volume for data persistence
- Automatic database initialization and seeding

## Common Commands

```bash
# Start entire application
docker-compose up

# Rebuild after changes
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Reset database
docker-compose down -v
docker-compose up
```

## Notes for Future Development
- Consider adding Redis for session management if scaling
- Implement proper authentication system if needed
- Add WebSocket support for real-time admin updates
- Consider PostgreSQL if concurrent writes become an issue
- Add rate limiting for public endpoints