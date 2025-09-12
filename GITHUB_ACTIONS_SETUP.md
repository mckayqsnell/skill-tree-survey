# GitHub Actions CI/CD Setup Guide

## Overview

This repository uses GitHub Actions for continuous integration and deployment. There are two main workflows:

1. **PR Validation** (`pr-validation.yml`) - Automatically runs on pull requests
2. **Production Deployment** (`deploy-production.yml`) - Manual deployment to production

## Required GitHub Secrets

Before the workflows can run successfully, you need to configure the following secrets in your GitHub repository:

### Navigation to Secrets
1. Go to your GitHub repository
2. Click on **Settings** (in the repository, not your profile)
3. In the left sidebar, expand **Secrets and variables**
4. Click on **Actions**
5. Click **New repository secret** for each secret below

### Required Secrets for Production Deployment

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `EC2_HOST` | Your EC2 instance public IP or hostname | `54.123.45.67` or `ec2-54-123-45-67.compute-1.amazonaws.com` |
| `EC2_USERNAME` | SSH username for EC2 instance | `ec2-user` (Amazon Linux) or `ubuntu` (Ubuntu) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access | Copy entire private key including `-----BEGIN RSA PRIVATE KEY-----` |
| `EC2_PORT` | SSH port (optional, defaults to 22) | `22` |
| `ADMIN_PASSWORD` | Admin password for the application | `your-secure-password-here` |
| `VITE_API_URL` | Production API URL | `https://skills-survey.heal.engineering` |
| `CORS_ORIGINS` | Allowed origins for CORS | `["https://skills-survey.heal.engineering","http://skills-survey.heal.engineering"]` |

### Optional AWS ECR Configuration (if using AWS ECR instead of Docker Hub)

| Secret Name | Description |
|------------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key for ECR |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for ECR |

Also set these repository variables:
- `USE_AWS_ECR`: Set to `true` to use AWS ECR
- `AWS_REGION`: Your AWS region (e.g., `us-east-1`)

## Setting Up SSH Key

### Generate SSH Key Pair (if you don't have one)
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/skill-survey-deploy -C "github-actions"
```

### Add Public Key to EC2 Instance
```bash
# Copy the public key
cat ~/.ssh/skill-survey-deploy.pub

# SSH into your EC2 instance
ssh ec2-user@your-ec2-ip

# Add the public key to authorized_keys
echo "paste-public-key-here" >> ~/.ssh/authorized_keys
```

### Add Private Key to GitHub Secrets
```bash
# Copy the private key
cat ~/.ssh/skill-survey-deploy

# Paste entire contents into EC2_SSH_KEY secret in GitHub
```

## Workflow Usage

### PR Validation Workflow

This workflow runs automatically when:
- A pull request is opened to the `main` branch
- Changes are pushed to an open pull request
- The changes affect backend, frontend, or Docker files

The workflow:
1. Builds both Docker images
2. Validates docker-compose configuration
3. Starts services and runs health checks
4. Tests API endpoints
5. Comments on the PR with results

### Production Deployment Workflow

This workflow must be triggered manually:

1. Go to the **Actions** tab in your repository
2. Select **Deploy to Production** workflow
3. Click **Run workflow**
4. Optionally enter a deployment message
5. Click **Run workflow** (green button)

The workflow:
1. Builds production Docker images
2. Transfers images to EC2
3. Updates environment variables
4. Performs zero-downtime deployment
5. Runs health checks
6. Creates deployment summary

### Manual Deployment Options

When running the production deployment, you have these options:

- **Deployment message**: Add a note about why you're deploying
- **Skip health checks**: Use with caution - bypasses health validation

## Monitoring Deployments

### View Deployment Status
1. Go to **Actions** tab
2. Click on the running/completed workflow
3. View real-time logs and status

### Deployment Summary
After each deployment, check the summary by:
1. Click on the completed workflow
2. Scroll down to see the **Deployment Summary** section

## Troubleshooting

### Common Issues

#### SSH Connection Failed
- Verify `EC2_HOST` is correct
- Check security group allows SSH (port 22) from GitHub Actions IPs
- Ensure SSH key is properly formatted (include full key with headers)

#### Docker Commands Not Found
- Ensure Docker is installed on EC2 instance
- Verify docker-compose is installed
- Check user has docker permissions: `sudo usermod -aG docker $USER`

#### Health Checks Failing
- Check application logs: `docker-compose -f docker-compose.prod.yml logs`
- Verify environment variables are set correctly
- Ensure database is initialized

#### CORS Errors
- Update `CORS_ORIGINS` secret to include all frontend URLs
- Include both HTTP and HTTPS variants if needed

### Manual Rollback

If deployment fails and you need to rollback:

```bash
# SSH into EC2
ssh ec2-user@your-ec2-ip

# Navigate to project directory
cd ~/skill-tree-survey

# Stop current containers
docker-compose -f docker-compose.prod.yml down

# Restore backup environment file (if exists)
cp .env.production.backup.* .env.production

# Start previous version
docker-compose -f docker-compose.prod.yml up -d

# Or pull specific version
docker-compose -f docker-compose.prod.yml up -d
```

## Setting Up Test Environment

To create a test/staging environment, duplicate the production workflow and:

1. Copy `deploy-production.yml` to `deploy-test.yml`
2. Update environment name from `production` to `test`
3. Create new secrets with `TEST_` prefix:
   - `TEST_EC2_HOST`
   - `TEST_EC2_USERNAME`
   - `TEST_EC2_SSH_KEY`
   - `TEST_VITE_API_URL`
   - etc.
4. Update the workflow to use test secrets
5. Change the deployment URL to your test domain

## Security Best Practices

1. **Rotate SSH Keys Regularly**: Generate new SSH keys every 3-6 months
2. **Use Strong Passwords**: Admin password should be complex
3. **Limit GitHub Secrets Access**: Only give repository admin access to those who need it
4. **Review Logs**: Regularly check deployment logs for any issues
5. **Environment Separation**: Keep test and production environments completely separate
6. **Backup Before Deploy**: The workflow automatically backs up `.env.production`

## Advanced Configuration

### Using AWS ECR

If you want to use AWS ECR instead of local Docker images:

1. Create an ECR repository
2. Add AWS credentials to secrets
3. Set repository variable `USE_AWS_ECR` to `true`
4. The workflow will automatically push/pull from ECR

### Custom Health Checks

Modify the health check logic in the deployment workflow:

```yaml
# In deploy-production.yml, modify the health check section
if curl -f http://localhost:8000/your-custom-endpoint; then
  echo "✅ Custom health check passed"
fi
```

### Notifications

Add Slack or email notifications by adding a step:

```yaml
- name: Send Slack notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Support

For issues or questions:
1. Check the workflow logs in the Actions tab
2. Review this documentation
3. Check the error messages in deployment summaries
4. SSH into the server and check Docker logs if needed