#!/bin/bash
# Setup script for nginx on production server

set -e

echo "🔧 Setting up nginx for production environment"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo"
    exit 1
fi

# Install nginx if not already installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing nginx..."
    yum update -y
    yum install -y nginx
else
    echo "✅ nginx already installed"
fi

# Copy production nginx config
echo "📝 Copying production nginx configuration..."
cp /home/ec2-user/skill-tree-survey/infrastructure/nginx/production.conf /etc/nginx/conf.d/skills-survey.conf

# Create SSL certificate with certbot
echo "🔐 Setting up SSL certificate..."
if [ ! -d "/etc/letsencrypt/live/skills-survey.heal.engineering" ]; then
    # Install certbot if not installed
    if ! command -v certbot &> /dev/null; then
        yum install -y certbot python3-certbot-nginx
    fi

    # Get certificate
    certbot certonly --nginx -d skills-survey.heal.engineering --non-interactive --agree-tos --email admin@heal.engineering
else
    echo "✅ SSL certificate already exists"
fi

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
nginx -t

# Enable and start nginx
echo "🚀 Starting nginx..."
systemctl enable nginx
systemctl restart nginx

# Set up auto-renewal for SSL certificate
echo "⏰ Setting up SSL auto-renewal..."
if ! crontab -l 2>/dev/null | grep -q certbot; then
    (crontab -l 2>/dev/null; echo "0 0,12 * * * /usr/bin/certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -
    echo "✅ SSL auto-renewal configured"
else
    echo "✅ SSL auto-renewal already configured"
fi

# Open firewall ports if firewall is active
if systemctl is-active --quiet firewalld; then
    echo "🔥 Configuring firewall..."
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
fi

echo "✅ Nginx setup complete!"
echo ""
echo "📋 Status:"
systemctl status nginx --no-pager | head -10
echo ""
echo "🌐 Your site should now be accessible at:"
echo "   https://skills-survey.heal.engineering"