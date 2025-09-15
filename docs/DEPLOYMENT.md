# Deployment Guide

## Environments

### Development
- **URL**: http://localhost:5173
- **Compose**: `docker-compose.yml`
- **Environment**: `environments/.env.development.example`

### Test
- **URL**: https://test-skills-survey.heal.engineering
- **Compose**: `docker-compose.test.yml`
- **Environment**: `environments/.env.test.example`
- **Setup**: `infrastructure/scripts/setup-test-environment.sh`

### Production
- **URL**: https://skills-survey.heal.engineering
- **Compose**: `docker-compose.prod.yml`
- **Environment**: `environments/.env.production.example`

## Quick Deployment

### Test Environment
```bash
# On test server
git pull origin main
cp environments/.env.test.example .env.test
# Edit .env.test with your values
docker-compose -f docker-compose.test.yml up -d --build
