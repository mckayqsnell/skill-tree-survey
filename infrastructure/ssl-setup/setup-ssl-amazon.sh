#!/bin/bash

# Install nginx and certbot for Amazon Linux
sudo yum update -y
sudo yum install -y nginx

# Install certbot
sudo yum install -y python3 python3-pip
sudo pip3 install certbot certbot-nginx

# Alternative for Amazon Linux 2023:
# sudo dnf install -y nginx python3-certbot-nginx

# Stop any existing nginx
sudo systemctl stop nginx 2>/dev/null || true

# Get SSL certificate
sudo certbot certonly --standalone -d skills-survey.heal.engineering --non-interactive --agree-tos --email your-email@example.com

# Create nginx sites directories (Amazon Linux doesn't have these by default)
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Copy nginx config
sudo cp nginx-proxy.conf /etc/nginx/sites-available/skills-survey
sudo ln -sf /etc/nginx/sites-available/skills-survey /etc/nginx/sites-enabled/

# Update main nginx.conf to include sites-enabled
sudo sed -i '/http {/a\    include /etc/nginx/sites-enabled/*;' /etc/nginx/nginx.conf

# Remove default server block from main nginx.conf if it exists
sudo sed -i '/server {/,/^    }/d' /etc/nginx/nginx.conf

# Test nginx config
sudo nginx -t

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Set up auto-renewal with cron
echo "0 2 * * * /usr/local/bin/certbot renew --quiet --nginx" | sudo crontab -

echo "SSL setup complete!"
echo "Don't forget to update your .env files with HTTPS URLs:"
echo "CORS_ORIGINS should include: https://skills-survey.heal.engineering"
echo "VITE_API_URL should be: https://skills-survey.heal.engineering/api"