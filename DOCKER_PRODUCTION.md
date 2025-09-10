# Docker Production Deployment Guide

## 🚀 Quick Start

Just three commands to get everything running in production:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd skill-tree-survey

# 2. Set up environment (optional - defaults work out of the box)
cp .env.production.example .env.production
# Edit .env.production to set your admin password

# 3. Run everything!
docker-compose -f docker-compose.prod.yml up -d
```

That's it! The application will:
- ✅ Build both frontend and backend
- ✅ Start the services
- ✅ Create the database automatically
- ✅ **Seed the database with all skill tree questions** (on first run)
- ✅ Serve frontend on port 80
- ✅ Serve backend API on port 8000

Access the application at:
- Frontend: `http://your-server-ip`
- Backend API: `http://your-server-ip:8000/docs`
- Admin Panel: `http://your-server-ip/admin` (password: admin123 by default)

## 📁 Files Explained

### Production Files Created:
- `docker-compose.prod.yml` - Production orchestration
- `backend/Dockerfile.prod` - Optimized backend image
- `frontend/Dockerfile.prod` - Nginx-served frontend
- `frontend/nginx.conf` - Production web server config

### Development Files (still available):
- `docker-compose.yml` - Development with hot-reload
- `backend/Dockerfile` - Development backend
- `frontend/Dockerfile` - Development frontend

## 🔧 Configuration

### Essential Environment Variables

```bash
# Create .env.production file
cat > .env.production << EOF
# CHANGE THIS - Admin password for the admin panel
ADMIN_PASSWORD=your-secure-password-here

# API URL - Update with your actual domain
VITE_API_URL=http://your-domain.com:8000

# Database URL (SQLite by default, works out of the box)
DATABASE_URL=sqlite:////app/data/skill_survey.db
EOF
```

### Auto-Seeding Feature

The database **automatically seeds with comprehensive skill tree questions** on first run when `SEED_ON_STARTUP=true` (default). This includes:
- 11 categories (Backend, Frontend, DevOps, Cloud, ML, etc.)
- 1000+ skill assessment questions
- Deep hierarchical structure (up to 6 levels)

**No manual setup required!**

## 🌐 Deployment Scenarios

### Local Server / VPS

```bash
# Deploy with custom env file
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down

# Reset everything (including database)
docker-compose -f docker-compose.prod.yml down -v
```

### Cloud Platforms

#### AWS EC2 / DigitalOcean Droplet / Linode

```bash
# SSH into your server
ssh user@your-server-ip

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Clone and run
git clone <your-repo>
cd skill-tree-survey
docker-compose -f docker-compose.prod.yml up -d
```

#### With HTTPS (Recommended)

Add Caddy or Traefik as reverse proxy:

```yaml
# Add to docker-compose.prod.yml
  caddy:
    image: caddy:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
    networks:
      - skill-survey-network
```

Create `Caddyfile`:
```
your-domain.com {
    reverse_proxy frontend:80
}

api.your-domain.com {
    reverse_proxy backend:8000
}
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build
```

### Backup Database

```bash
# Backup SQLite database
docker run --rm -v skill-tree-survey_sqlite_data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore from backup
docker run --rm -v skill-tree-survey_sqlite_data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/backup-20240101.tar.gz -C /data
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Backend only
docker-compose -f docker-compose.prod.yml logs -f backend

# Frontend only  
docker-compose -f docker-compose.prod.yml logs -f frontend
```

## 🚨 Troubleshooting

### Port Already in Use

```bash
# Check what's using port 80
sudo lsof -i :80

# Use different ports
FRONTEND_PORT=3000 docker-compose -f docker-compose.prod.yml up -d
```

### Database Issues

```bash
# Reset database (will re-seed)
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### Can't Access Application

```bash
# Check if containers are running
docker ps

# Check firewall (Ubuntu/Debian)
sudo ufw allow 80
sudo ufw allow 8000

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs --tail=50
```

## 🔐 Security Checklist

Before going live:

- [ ] **Change admin password** from default 'admin123'
- [ ] **Set up HTTPS** with Let's Encrypt
- [ ] **Configure firewall** to only allow necessary ports
- [ ] **Update CORS origins** in docker-compose.prod.yml
- [ ] **Set up regular backups** of the database
- [ ] **Monitor logs** for suspicious activity

## 🎯 Performance Tips

### Scale Backend Workers

```yaml
# In docker-compose.prod.yml, under backend service
command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

### Add Redis Cache (Optional)

```yaml
  redis:
    image: redis:alpine
    networks:
      - skill-survey-network
    restart: always
```

### Use PostgreSQL for Better Performance

```yaml
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: skill_survey
      POSTGRES_USER: skilluser
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - skill-survey-network
```

Then update `DATABASE_URL` in your environment.

## 📊 Monitoring

### Health Checks

- Backend: `http://your-server:8000/health`
- Frontend: `http://your-server/`
- API Docs: `http://your-server:8000/docs`

### Container Stats

```bash
# Resource usage
docker stats

# Container health
docker-compose -f docker-compose.prod.yml ps
```

## 🎉 Success!

Your Skill Tree Survey is now running in production! 

- Survey URL: `http://your-server/`
- Admin Panel: `http://your-server/admin`
- API Documentation: `http://your-server:8000/docs`

The database is automatically seeded with comprehensive skill assessment questions across all major tech domains. Employees can start taking the survey immediately!