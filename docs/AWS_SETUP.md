# Deployment Guide

## Prerequisites

### Server Requirements
- Amazon Linux 2 or Ubuntu 20.04+
- Docker 20.10+
- Docker Compose 2.0+
- Git
- 2GB RAM minimum
- 10GB disk space

### Domain Setup
- DNS A record pointing to server IP
- Ports 80, 443, 8000, 8080 available

## Server Setup

### 1. Install Dependencies (Amazon Linux 2)

```bash
# Update packages
sudo yum update -y

# Install Docker
sudo yum install docker -y
sudo service docker start
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install Git
sudo yum install git -y

# Verify installations
docker --version
docker-compose --version
git --version

# Log out and back in for docker permissions
exit
```

### 1. Install Dependencies (Ubuntu)

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install git -y

# Verify installations
docker --version
docker-compose --version
git --version

# Log out and back in for docker permissions
exit
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/HEAL-Engineering/skill-tree-survey.git
sudo chown -R ec2-user:ec2-user skill-tree-survey  # For Amazon Linux
# sudo chown -R $USER:$USER skill-tree-survey       # For Ubuntu
cd skill-tree-survey
```

## Environment Deployment

### Development Environment

```bash
# Copy environment template
cp environments/.env.development.example .env

# Start services
docker-compose up -d --build

# Verify
curl http://localhost:8000/health
# Access frontend at http://localhost:5173
```

### Test Environment

```bash
# Copy environment template
cp environments/.env.test.example .env

# Edit environment variables
nano .env
# Update:
# - ADMIN_PASSWORD=your-secure-password
# - VITE_API_URL=https://test-skills-survey.heal.engineering

# Build and start
docker-compose -f docker-compose.test.yml up -d --build

# Verify services
docker-compose -f docker-compose.test.yml ps
docker-compose -f docker-compose.test.yml logs -f --tail=50

# Check health
curl http://localhost:8000/health
```

### Production Environment

```bash
# Create production env file
cat > .env << EOF
ADMIN_PASSWORD=your-secure-admin-password
CORS_ORIGINS=["https://skills-survey.heal.engineering"]
VITE_API_URL=https://skills-survey.heal.engineering
ENVIRONMENT=production
SEED_ON_STARTUP=true
DEBUG=false
EOF

# Build and start
docker-compose -f docker-compose.prod.yml up -d --build

# Verify
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health
```

## Nginx Reverse Proxy Setup

### 1. Install Nginx (Amazon Linux 2)

```bash
# Install nginx
sudo amazon-linux-extras install nginx1 -y
sudo systemctl stop nginx
```

### 1. Install Nginx (Ubuntu)

```bash
sudo apt install nginx -y
sudo systemctl stop nginx
```

### 2. Configure Nginx

#### For Test Environment
```bash
sudo cp infrastructure/nginx/test.conf /etc/nginx/conf.d/skill-survey.conf
# Remove default configs
sudo rm -f /etc/nginx/conf.d/default.conf
sudo rm -f /etc/nginx/sites-enabled/default
```

#### For Production Environment
```bash
sudo cp infrastructure/nginx/production.conf /etc/nginx/conf.d/skill-survey.conf
# Remove default configs
sudo rm -f /etc/nginx/conf.d/default.conf
sudo rm -f /etc/nginx/sites-enabled/default
```

### 3. SSL Certificate Setup (Amazon Linux 2)

```bash
# Install certbot via EPEL
sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum install certbot python-certbot-nginx -y

# Stop nginx temporarily
sudo systemctl stop nginx

# Get certificate (replace domain and email)
sudo certbot certonly --standalone \
  -d skills-survey.heal.engineering \
  --non-interactive \
  --agree-tos \
  --email admin@heal.engineering

# Test nginx configuration
sudo nginx -t

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Setup auto-renewal
sudo crontab -e
# Add line: 0 2 * * * certbot renew --quiet --nginx
```

### 3. SSL Certificate Setup (Ubuntu)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Stop nginx temporarily
sudo systemctl stop nginx

# Get certificate (replace domain and email)
sudo certbot certonly --standalone \
  -d skills-survey.heal.engineering \
  --non-interactive \
  --agree-tos \
  --email admin@heal.engineering

# Test nginx configuration
sudo nginx -t

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Setup auto-renewal
sudo crontab -e
# Add line: 0 2 * * * certbot renew --quiet --nginx
```

## AWS EC2 Security Group Configuration

Configure your EC2 security group with these inbound rules:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | Your IP |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

## Deployment Commands

### Deploy New Version

```bash
cd /opt/skill-tree-survey

# Pull latest code
git pull origin main

# For test environment
docker-compose -f docker-compose.test.yml down
docker-compose -f docker-compose.test.yml up -d --build

# For production
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

# Verify deployment
docker-compose -f docker-compose.[env].yml ps
docker-compose -f docker-compose.[env].yml logs --tail=50
```

### Container Management

```bash
# View running containers
docker ps

# View logs
docker-compose -f docker-compose.[env].yml logs -f backend
docker-compose -f docker-compose.[env].yml logs -f frontend

# Restart services
docker-compose -f docker-compose.[env].yml restart

# Stop services
docker-compose -f docker-compose.[env].yml down

# Remove volumes (WARNING: deletes data)
docker-compose -f docker-compose.[env].yml down -v
```

## Verification

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Via nginx (after SSL setup)
curl https://skills-survey.heal.engineering/health

# API endpoints
curl https://skills-survey.heal.engineering/api/questions/base
```

### Database Verification

```bash
# Access backend container
docker exec -it skill-survey-backend bash

# Check database
ls -la /app/data/
sqlite3 /app/data/skill_survey.db "SELECT COUNT(*) FROM questions;"
```

## Troubleshooting

### Container Issues

```bash
# Check container status
docker-compose -f docker-compose.[env].yml ps

# View detailed logs
docker-compose -f docker-compose.[env].yml logs --tail=100 backend
docker-compose -f docker-compose.[env].yml logs --tail=100 frontend

# Restart containers
docker-compose -f docker-compose.[env].yml restart

# Rebuild without cache
docker-compose -f docker-compose.[env].yml build --no-cache
docker-compose -f docker-compose.[env].yml up -d
```

### Port Conflicts

```bash
# Check port usage
sudo lsof -i :8000
sudo lsof -i :8080
sudo lsof -i :80
sudo lsof -i :443

# Kill process using port
sudo kill -9 $(sudo lsof -t -i:8000)
```

### Database Issues

```bash
# Reset database (WARNING: data loss)
docker-compose -f docker-compose.[env].yml down -v
docker-compose -f docker-compose.[env].yml up -d

# Backup database
docker exec skill-survey-backend cp /app/data/skill_survey.db /app/data/backup_$(date +%Y%m%d).db

# Restore database
docker exec skill-survey-backend cp /app/data/backup_20240101.db /app/data/skill_survey.db
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# View error logs
sudo tail -f /var/log/nginx/error.log

# Reload configuration
sudo systemctl reload nginx

# Full restart
sudo systemctl restart nginx
```

### SSL Certificate Issues

```bash
# Test renewal
sudo certbot renew --dry-run

# Force renewal
sudo certbot renew --force-renewal

# Check certificate
sudo certbot certificates
```

### Amazon Linux 2 Specific Issues

```bash
# If docker won't start
sudo yum reinstall docker
sudo service docker restart

# If nginx isn't available
sudo amazon-linux-extras list | grep nginx
sudo amazon-linux-extras enable nginx1

# SELinux issues (if enabled)
sudo setsebool -P httpd_can_network_connect 1
```

## Monitoring

### System Resources

```bash
# Container stats
docker stats

# Disk usage
df -h
docker system df

# Clean up unused resources
docker system prune -a --volumes
```

### Application Logs

```bash
# Follow all logs
docker-compose -f docker-compose.[env].yml logs -f

# Export logs
docker-compose -f docker-compose.[env].yml logs > deployment_$(date +%Y%m%d).log
```

### AWS CloudWatch Integration (Optional)

```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
sudo rpm -U ./amazon-cloudwatch-agent.rpm
```

## Backup & Recovery

### Backup

```bash
# Create backup directory
mkdir -p /opt/backups

# Backup database
docker exec skill-survey-backend tar czf /tmp/backup.tar.gz /app/data/
docker cp skill-survey-backend:/tmp/backup.tar.gz /opt/backups/backup_$(date +%Y%m%d_%H%M%S).tar.gz

# Backup environment
cp .env /opt/backups/.env.backup_$(date +%Y%m%d)

# Sync to S3 (if using AWS)
aws s3 sync /opt/backups s3://your-backup-bucket/skill-survey-backups/
```

### Restore

```bash
# Stop services
docker-compose -f docker-compose.[env].yml down

# Restore database
docker-compose -f docker-compose.[env].yml up -d backend
docker cp /opt/backups/backup_20240101_120000.tar.gz skill-survey-backend:/tmp/
docker exec skill-survey-backend tar xzf /tmp/backup.tar.gz -C /

# Restart all services
docker-compose -f docker-compose.[env].yml up -d
```

## Security Notes

1. **Change default passwords** in production
2. **Restrict ports** - only expose 80/443 through security groups
3. **Regular updates** - keep Docker, OS packages updated
4. **Backup regularly** - automate daily backups to S3
5. **Monitor logs** - use CloudWatch for centralized logging
6. **Use secrets management** - AWS Secrets Manager for sensitive data
7. **Enable MFA** for AWS console access
8. **Use IAM roles** for EC2 instances instead of access keys

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| ADMIN_PASSWORD | Admin panel password | secure-password-123 |
| CORS_ORIGINS | Allowed frontend origins | ["https://domain.com"] |
| VITE_API_URL | Frontend API URL | https://domain.com |
| DATABASE_URL | Database connection | sqlite:////app/data/db.db |
| SEED_ON_STARTUP | Auto-seed database | true |
| ENVIRONMENT | Environment name | production |
| DEBUG | Debug mode | false |