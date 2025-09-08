# Skill Tree Survey

A gamified employee skills assessment tool with branching question logic. Built with Vue 3, TypeScript, FastAPI, and a space-themed UI. Keyboard-driven for speed - complete in 5-10 minutes!

## Quick Start

```bash
# Start both frontend and backend with Docker
docker-compose up

# Access the application
http://localhost:5173      # Frontend (Vue app)
http://localhost:8000/docs  # Backend API docs
```

## Features

- **Gamified Experience**: Space-themed UI with smooth animations
- **Keyboard Navigation**: 
  - `Space`/`Enter` = YES (go deeper)
  - `N` = NO (next skill)
- **Branching Logic**: "Yes" answers unlock deeper questions in that skill area
- **Admin Panel**: Manage questions, view sessions, analytics
- **Real-time Progress**: Visual progress tracking and depth indicators
- **Clean Error Handling**: Comprehensive logging and error recovery

## Tech Stack

- **Frontend**: Vue 3, TypeScript, Vite, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic
- **Deployment**: Docker Compose with hot-reload

## Project Structure

```
backend/
├── app/
│   ├── config/       # Settings
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── dao/          # Data access layer
│   ├── services/     # Business logic
│   ├── routes/       # API endpoints
│   └── seeders/      # Initial data (60+ questions)
└── requirements.txt
```

## API Examples

### Start Session
```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"John Doe","user_email":"john@example.com","company":"TechCorp"}'
```

### Get Base Questions
```bash
curl http://localhost:8000/api/questions/base
```

### Get Child Questions
```bash
curl http://localhost:8000/api/questions/1/children
```

### Submit Response
```bash
curl -X POST http://localhost:8000/api/responses/session/1 \
  -H "Content-Type: application/json" \
  -d '{"question_id":1,"answer":true}'
```

## Admin Endpoints

Require header: `X-Admin-Password: admin123`

- `GET /api/admin/sessions` - All sessions
- `GET /api/admin/analytics` - Analytics data
- `POST /api/admin/questions` - Create question
- `PUT /api/admin/questions/{id}` - Update question
- `DELETE /api/admin/questions/{id}` - Delete question

## Usage Guide

### Taking the Survey
1. Navigate to http://localhost:5173
2. Enter your information (name, email, company)
3. Answer questions using keyboard:
   - Press `Space` or `Enter` for YES
   - Press `N` for NO
4. View your results on completion

### Admin Panel
1. Navigate to http://localhost:5173/admin
2. Enter password: `admin123`
3. Manage questions, view sessions, analytics

## Environment Variables

### Backend
| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite:///./skill_survey.db | Database path |
| ADMIN_PASSWORD | admin123 | Admin API password |
| SEED_ON_STARTUP | true | Auto-seed questions |

### Frontend
| Variable | Default | Description |
|----------|---------|-------------|
| VITE_API_URL | http://localhost:8000 | Backend API URL |
| VITE_ADMIN_PASSWORD | admin123 | Admin password |

## Database Schema

- **questions**: id, parent_id, text, is_base, category, order_index
- **survey_sessions**: id, user_name, user_email, company, started_at, completed_at  
- **responses**: id, session_id, question_id, answer, answered_at

## Notes

- POST endpoints require trailing slash (e.g., `/api/sessions/`)
- Database auto-seeds with questions across DevOps, Backend, Frontend, Data, Cloud, ML
- SQLite database persists in Docker volume

## Troubleshooting

```bash
# View logs
docker-compose logs backend

# Reset database
docker-compose down -v
docker-compose up -d
```