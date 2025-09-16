# Workflow Examples

Practical examples for common development scenarios with actual commands.

## Example 1: Creating a New Feature

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch (format: <username>/<ticket-id>/<feature-name>)
git checkout -b nate/HEA-123/add-user-dashboard

# Make changes
code .  # Open your editor
# ... edit files ...

# Stage and commit changes
git add .
git commit -m "feat: add user dashboard with statistics"

# Push to GitHub
git push -u origin nate/HEA-123/add-user-dashboard

# Create PR via GitHub UI or CLI
gh pr create --base develop --title "feat: add user dashboard" --body "Added dashboard showing user statistics and activity"

# After PR approval, it auto-deploys to test environment
```

## Example 2: Fixing a Bug

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create bugfix branch
git checkout -b nate/HEA-456/fix-login-timeout

# Fix the bug
# ... make fixes ...

# Commit and push
git add .
git commit -m "fix: increase login session timeout to 30 minutes"
git push -u origin nate/HEA-456/fix-login-timeout

# Create PR to develop
gh pr create --base develop --title "fix: login timeout issue"
```

## Example 3: Emergency Production Hotfix

```bash
# IMPORTANT: Hotfix branches from main, not develop
git checkout main
git pull origin main

# Create hotfix branch
git checkout -b nate/HOTFIX/critical-auth-bug

# Make minimal fix
# ... fix the critical bug ...

# Commit and push
git add .
git commit -m "fix: resolve authentication bypass vulnerability"
git push -u origin nate/HOTFIX/critical-auth-bug

# Create PR directly to main
gh pr create --base main --title "HOTFIX: critical auth vulnerability" --body "URGENT: Fixes authentication bypass"

# After merge and deploy, cherry-pick to develop
git checkout develop
git pull origin develop
git cherry-pick <commit-hash>
git push origin develop
```

## Example 4: Keeping Your Branch Updated

```bash
# You're working on a feature and develop has new changes
git checkout develop
git pull origin develop

# Go back to your feature branch
git checkout nate/HEA-789/new-feature

# Option 1: Merge (preserves history)
git merge develop

# Option 2: Rebase (cleaner history)
git rebase develop

# If conflicts occur during rebase
git status  # See conflicted files
# ... resolve conflicts ...
git add .
git rebase --continue

# Force push after rebase (only if you've already pushed)
git push --force-with-lease origin nate/HEA-789/new-feature
```

## Example 5: Deploying to Production

```bash
# First, create PR from develop to main
gh pr create --base main --head develop --title "Release: Deploy latest features to production"

# After PR approval and merge:
# 1. Go to GitHub → Actions tab
# 2. Click "Deploy to Production" workflow
# 3. Click "Run workflow"
# 4. Enter deployment message
# 5. Click "Run workflow" button

# Monitor deployment in Actions tab
```

## Example 6: Checking Deployment Status

```bash
# Check test environment
curl https://test-skills-survey.heal.engineering/health

# Check production environment
curl https://skills-survey.heal.engineering/health

# SSH to server to check logs
ssh ec2-user@test-skills-survey.heal.engineering
cd /opt/skill-tree-survey
docker-compose -f docker-compose.test.yml logs --tail=50
docker-compose -f docker-compose.test.yml ps
```

## Example 7: Rollback Deployment

```bash
# SSH to server (test or production)
ssh ec2-user@skills-survey.heal.engineering

# Navigate to project
cd /opt/skill-tree-survey

# Check current status
docker-compose -f docker-compose.prod.yml ps

# Stop current deployment
docker-compose -f docker-compose.prod.yml down

# Find and restore previous .env backup
ls -la .env.backup.*
cp .env.backup.20240115_143022 .env  # Use appropriate backup

# Restart with previous configuration
docker-compose -f docker-compose.prod.yml up -d

# Verify rollback
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health
```

## Example 8: Running Local Development

```bash
# Clone and setup
git clone https://github.com/HEAL-Engineering/skill-tree-survey.git
cd skill-tree-survey
git checkout develop

# Docker setup (recommended)
cp environments/.env.development.example .env
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Stop when done
docker-compose down
```

## Example 9: Cleaning Up Old Branches

```bash
# Delete local branches that have been merged
git branch --merged develop | grep -v develop | xargs -n 1 git branch -d

# Prune remote tracking branches
git remote prune origin

# See all your remote branches
git branch -r | grep nate/

# Delete remote branch (after PR merged)
git push origin --delete nate/HEA-123/old-feature
```

## Common Git Aliases (Optional)

Add these to your `~/.gitconfig`:

```bash
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

## Tips

1. **Always test locally** before pushing
2. **Keep PRs small** - easier to review
3. **Write clear commit messages** - future you will thank you
4. **Pull develop frequently** - avoid merge conflicts
5. **Use draft PRs** for work in progress
6. **Don't force push to develop or main** - ever
7. **Ask for help** if you're stuck

## Getting Help

- Check existing PRs for examples
- Ask in team Slack channel
- Review the [Contributing Guidelines](../CONTRIBUTING.md)
- Check [Deployment Documentation](./DEPLOYMENT.md)