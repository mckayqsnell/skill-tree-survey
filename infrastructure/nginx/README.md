# Nginx Configuration

This directory contains nginx configurations for the Skill Tree Survey application.

## Architecture

The application uses a two-layer nginx setup:

1. **Host Nginx** (on EC2 instance) - Handles SSL termination and reverse proxy
2. **Container Nginx** (in Docker) - Serves the Vue.js frontend static files

## Files

- `test.conf` - Configuration for test environment (test-skills-survey.heal.engineering)
- `production.conf` - Configuration for production environment (skills-survey.heal.engineering)
- `setup-production-nginx.sh` - Script to configure nginx on production server
- `nginx-main.conf` - Main nginx config (deprecated, kept for reference)

## Setup Instructions

### Test Environment
The test environment already has nginx configured. The configuration:
- Listens on ports 80 (redirect to HTTPS) and 443 (SSL)
- Proxies `/api` and `/health` to backend container (port 8000)
- Proxies `/` to frontend container (port 8080)
- SSL certificates managed by Let's Encrypt

### Production Environment
To set up nginx on the production server:

1. SSH into the production EC2 instance
2. Run the setup script:
   ```bash
   cd ~/skill-tree-survey
   sudo ./infrastructure/nginx/setup-production-nginx.sh
   ```

The script will:
- Install nginx (if not installed)
- Copy the production configuration
- Set up SSL certificates with Let's Encrypt
- Configure auto-renewal for certificates
- Start and enable nginx service

## How It Works

```
Internet Traffic
       ↓
   Port 443 (HTTPS)
       ↓
Host Nginx (SSL termination)
       ↓
   Reverse Proxy
    ├─ /api → Backend Container (port 8000)
    └─ /    → Frontend Container (port 8080)
               ↓
         Container Nginx
               ↓
         Vue.js Static Files
```

## Container Ports

- **Backend**: 8000 (FastAPI)
- **Frontend**: 8080 (nginx serving Vue.js)

## Troubleshooting

### Check nginx status on host
```bash
sudo systemctl status nginx
```

### Test nginx configuration
```bash
sudo nginx -t
```

### View nginx logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Reload nginx after config changes
```bash
sudo systemctl reload nginx
```

### SSL Certificate Issues
```bash
# Test certificate renewal
sudo certbot renew --dry-run

# Force renewal
sudo certbot renew --force-renewal

# View certificate details
sudo certbot certificates
```

## Security Notes

- SSL certificates are auto-renewed via cron job
- Security headers are configured (CSP, X-Frame-Options, etc.)
- TLS 1.2 and 1.3 only
- High-strength ciphers only