# Skill Tree Survey

A gamified employee skills assessment tool with branching question logic. Built with Vue 3, TypeScript, FastAPI, and a space-themed UI. Keyboard-driven for speed - complete in 5-10 minutes!

## 🔧 Development

For information on contributing to this project:
- [Contributing Guidelines](./CONTRIBUTING.md) - Development workflow and standards
- [Deployment Documentation](./docs/DEPLOYMENT.md) - CI/CD pipeline and deployment process
- [Workflow Examples](./docs/WORKFLOW_EXAMPLES.md) - Common development scenarios
- [AWS Setup Guide](./docs/AWS_SETUP.md) - Infrastructure setup instructions

### Quick Start for Developers
1. Clone the repository
2. Check out the `develop` branch
3. Create a feature branch
4. Make your changes
5. Submit a PR to `develop`

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed instructions.

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
- **Admin Panel**: Manage questions, view sessions, analytics with radar charts
- **Individual Session Analysis**: Detailed skill breakdowns with spider web visualizations
- **Session Management**: Delete individual sessions or bulk clear all data
- **Real-time Progress**: Visual progress tracking and depth indicators
- **Performance Metrics**: Tooltips explain all metrics, API health monitoring
- **Clean Error Handling**: Comprehensive logging and error recovery

## Tech Stack

- **Frontend**: Vue 3, TypeScript, Vite, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic
- **Deployment**: Docker Compose with hot-reload

## 🌍 Environments

This project supports multiple environments with proper separation:

- **Development**: Local development with hot-reload
- **Test**: Staging environment for testing
- **Production**: Live production environment

### Quick Start by Environment
```bash
# Development
docker-compose up

# Test
docker-compose -f docker-compose.test.yml up -d

# Production  
docker-compose -f docker-compose.prod.yml up -d

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

## Database Management

### Reset Database (Fresh Start)
```bash
# Complete reset - removes all data and re-seeds
docker-compose down -v
docker-compose up -d
```

**Note:** The `-v` flag removes the Docker volume containing the SQLite database. On restart, the seeder will automatically populate fresh data from `backend/app/seeders/initial_questions.json`.

### Normal Restart (Keep Data)
```bash
# Restart services without losing data
docker-compose restart

# Or stop and start
docker-compose down    # No -v flag keeps the volume
docker-compose up -d
```

## Troubleshooting

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# View real-time logs
docker-compose logs -f backend

# Check if services are running
docker-compose ps
```
