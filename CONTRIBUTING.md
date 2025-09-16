# Contributing to Skill Tree Survey

## 📋 Table of Contents
- [Branching Strategy](#branching-strategy)
- [Development Workflow](#development-workflow)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Getting Started](#getting-started)

## 🌳 Branching Strategy

```
feature branches     develop          main
       |               |               |
       ├────PR────────>├──────PR──────>|
       |               |               |
       |          Auto-deploy      Manual
       |           to Test        Deploy
       |               ↓          to Prod
            test-skills-      skills-survey.
            survey.heal.      heal.engineering
            engineering
```

### Branch Types
- `main` - Production branch (protected)
- `develop` - Integration branch (protected, auto-deploys to test)
- Feature branches follow: `<username>/<ticket-id>/<feature-name>`

### Branch Naming Convention
Format: `<username>/<ticket-id>/<feature-name>`

Examples:
- `nate/HEA-123/add-user-dashboard`
- `nate/HEA-45/fix-login-timeout`
- `nate/HEA-789/update-survey-logic`

## 💻 Development Workflow

### 1. Start from develop
```bash
git checkout develop
git pull origin develop
```

### 2. Create feature branch
```bash
# Format: <username>/<ticket-id>/<feature-name>
git checkout -b nate/HEA-123/add-user-dashboard
```

### 3. Make changes and commit
```bash
git add .
git commit -m "feat: describe your changes"
```

### 4. Push and create PR
```bash
git push -u origin nate/HEA-123/add-user-dashboard
# Create PR on GitHub: base=develop, compare=your-branch
```

### 5. After PR approval and merge
- Branch auto-deploys to test environment
- Feature branch is deleted automatically

## 📝 Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting, no code change
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance

Examples:
```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve database timeout issue"
git commit -m "docs: update API documentation"
```

## 🔀 Pull Request Process

1. **Before creating PR:**
   - Pull latest `develop`
   - Test your changes locally
   - Remove any debug code/console.logs

2. **PR Requirements:**
   - Clear title following commit convention
   - Fill out PR template
   - Request review from team member
   - Ensure CI checks pass

3. **After approval:**
   - Squash and merge to `develop`
   - Changes auto-deploy to test environment

## 🚀 Getting Started

### Quick Setup with Docker
```bash
# Clone repo
git clone https://github.com/HEAL-Engineering/skill-tree-survey.git
cd skill-tree-survey

# Switch to develop
git checkout develop

# Start local environment
cp environments/.env.development.example .env
docker-compose up -d --build

# Access at:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

### Without Docker
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## 🚨 Hotfix Process

For critical production issues:
```bash
# Create from main
git checkout main
git pull origin main
git checkout -b <username>/HOTFIX/<fix-description>

# Fix, commit, push
git push -u origin <username>/HOTFIX/<fix-description>

# PR directly to main, then cherry-pick to develop
```

## 📚 Additional Resources
- [Deployment Pipeline](./docs/DEPLOYMENT.md)
- [Workflow Examples](./docs/WORKFLOW_EXAMPLES.md)
- [AWS Infrastructure Setup](./docs/AWS_SETUP.md)