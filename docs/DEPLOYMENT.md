# Deployment Pipeline

## 🔄 Pipeline Overview

```
Feature Branch          Develop               Main
     |                     |                    |
     ├──PR + Review───────>├──PR + Approval────>|
     |                     |                    |
     |                Auto Deploy           Manual Deploy
     |                     ↓                    ↓
                   TEST Environment      PRODUCTION Environment
              test-skills-survey.heal.   skills-survey.heal.
                   engineering              engineering
```

## 🌍 Environments

### Local Development
- **URL**: http://localhost:5173 (frontend), http://localhost:8000 (backend)
- **Purpose**: Individual developer testing
- **Database**: Local SQLite
- **Deployment**: `docker-compose up`

### Test Environment
- **URL**: https://test-skills-survey.heal.engineering
- **Purpose**: Integration testing, QA
- **Deployment**: **Automatic** on merge to `develop`
- **Database**: Test SQLite database
- **Container Names**: `test-skill-survey-backend`, `test-skill-survey-frontend`

### Production Environment
- **URL**: https://skills-survey.heal.engineering
- **Purpose**: Live application
- **Deployment**: **Manual** trigger after merge to `main`
- **Database**: Production SQLite database
- **Container Names**: `skill-survey-backend`, `skill-survey-frontend`

## 📦 Deployment Process

### To Test (Automatic)

1. **Create PR** from feature branch to `develop`
2. **PR Validation** workflow automatically runs:
   - Builds Docker images
   - Runs health checks
   - Posts results to PR
3. **After approval and merge**:
   - Test deployment automatically triggered
   - Docker images built and deployed
   - Available at test URL within ~5 minutes
4. **Monitor** in GitHub Actions tab

### To Production (Manual)

1. **Create PR** from `develop` to `main`
2. **Requires** senior team member approval
3. **After merge**:
   ```
   Go to GitHub → Actions tab → Deploy to Production
   Click "Run workflow" → Add deployment message → Run
   ```
4. **Deployment steps**:
   - Builds production Docker images
   - Transfers to EC2
   - Deploys with docker-compose.prod.yml
   - Runs health checks
5. **Verify** at production URL

## 🔧 GitHub Actions Workflows

### PR Validation (`pr-validation.yml`)
- **Triggers**: PR to `main` or `develop`
- **Actions**: Build, test, health check
- **Duration**: ~3-5 minutes

### Test Deployment (`deploy-test.yml`)
- **Triggers**: Push to `develop` or manual
- **Actions**: Build, deploy to test environment
- **Duration**: ~5-7 minutes

### Production Deployment (`deploy-production.yml`)
- **Triggers**: Manual only
- **Actions**: Build, deploy to production
- **Duration**: ~5-7 minutes

## 🔄 Rollback Procedures

### Test Environment Rollback
```bash
# SSH to test server
ssh ec2-user@test-skills-survey.heal.engineering

# Navigate to project
cd /opt/skill-tree-survey

# Stop current deployment
docker-compose -f docker-compose.test.yml down

# Restore previous .env
ls -la .env.backup.*
cp .env.backup.YYYYMMDD_HHMMSS .env

# Redeploy
docker-compose -f docker-compose.test.yml up -d
```

### Production Rollback
Same as test but use `docker-compose.prod.yml` and production server.

### Emergency Hotfix
```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b <username>/HOTFIX/<description>

# Make fix and push
git push -u origin <username>/HOTFIX/<description>

# PR directly to main
# After deploy, cherry-pick to develop
```

## 📊 Monitoring

### Health Check Endpoints
- Backend: `/health`
- Full URL Test: `https://test-skills-survey.heal.engineering/health`
- Full URL Prod: `https://skills-survey.heal.engineering/health`

### Viewing Logs
```bash
# On server
docker-compose -f docker-compose.[env].yml logs -f backend
docker-compose -f docker-compose.[env].yml logs -f frontend

# View all logs
docker-compose -f docker-compose.[env].yml logs --tail=100
```

### GitHub Actions
- Go to repository → Actions tab
- View workflow runs
- Click on run for detailed logs
- Check deployment summaries

## 🔑 Environment Variables

### Test Environment
Configured via GitHub Secrets (TEST_ prefix):
- `TEST_EC2_HOST`
- `TEST_EC2_USERNAME`
- `TEST_EC2_SSH_KEY`
- `TEST_ADMIN_PASSWORD`
- `TEST_VITE_API_URL`
- `TEST_CORS_ORIGINS`

### Production Environment
Configured via GitHub Secrets:
- `EC2_HOST`
- `EC2_USERNAME`
- `EC2_SSH_KEY`
- `ADMIN_PASSWORD`
- `VITE_API_URL`
- `CORS_ORIGINS`

## 🚨 Troubleshooting

### Deployment Failed
1. Check GitHub Actions logs
2. SSH to server and check Docker logs
3. Verify environment variables
4. Check disk space: `df -h`
5. Check Docker status: `docker ps`

### Health Checks Failing
```bash
# Check if containers are running
docker ps

# Check container logs
docker logs skill-survey-backend
docker logs skill-survey-frontend

# Test endpoints directly
curl http://localhost:8000/health
curl http://localhost:8080
```

### Common Issues
- **Port conflicts**: Check with `sudo lsof -i :8000`
- **Docker space**: Run `docker system prune -a`
- **Environment variables**: Verify `.env` file exists and is correct

## 📚 Related Documentation
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Workflow Examples](./WORKFLOW_EXAMPLES.md)
- [AWS Infrastructure Setup](./AWS_SETUP.md)