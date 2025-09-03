# Skill Tree Survey

Employee skills assessment tool using branching question logic. "Yes" answers unlock deeper questions in that skill area.

## Quick Start

```bash
# Using Docker (recommended)
docker-compose up -d

# Verify
curl http://localhost:8000/health

# API docs
http://localhost:8000/docs
```

## Manual Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Vue 3 (not implemented)
- **Deployment**: Docker Compose

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

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite:///./skill_survey.db | Database path |
| ADMIN_PASSWORD | admin123 | Admin API password |
| SEED_ON_STARTUP | true | Auto-seed questions |

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