#!/bin/bash

# Install certbot and nginx
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx nginx

# Stop any existing nginx
sudo systemctl stop nginx

# Get SSL certificate
sudo certbot certonly --standalone -d skills-survey.heal.engineering --non-interactive --agree-tos --email your-email@example.com

# Copy nginx config
sudo cp nginx-proxy.conf /etc/nginx/sites-available/skills-survey
sudo ln -sf /etc/nginx/sites-available/skills-survey /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Set up auto-renewal
(crontab -l 2>/dev/null; echo "0 2 * * * certbot renew --quiet --nginx") | crontab -

echo "SSL setup complete!"
echo "Don't forget to update your .env files with HTTPS URLs:"
echo "CORS_ORIGINS should include: https://skills-survey.heal.engineering"
echo "VITE_API_URL should be: https://skills-survey.heal.engineering/api"