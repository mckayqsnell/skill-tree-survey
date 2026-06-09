#!/bin/bash
# =============================================================================
# EC2 user-data — runs once on FIRST boot of a fresh instance.
#
# Installs just enough to run the stack: Docker + the Docker Compose plugin.
# There is deliberately NO nginx, certbot, or htpasswd here — TLS and routing
# are handled by the Cloudflare Tunnel (the `cloudflared` container), and the
# only inbound port on the box is SSH.
#
# It does NOT pull or start the app. The compose file and secrets arrive later
# via `task prod:deploy` (scp), and Watchtower keeps the image up to date from
# GHCR after that.
#
# This runs on the fresh production box's first boot (and on any future
# replacement). It does not run again on reboots — first boot only.
# =============================================================================
set -euo pipefail

PROJECT_NAME="${project_name}"
ENVIRONMENT="${environment}"

# Log to a file + the console (visible via SSH or EC2 → Get system log).
exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1
echo "=== skill-tree-survey user-data start ($(date)) — env=$${ENVIRONMENT} ==="

echo "Updating system packages..."
dnf update -y

echo "Installing Docker..."
dnf install -y docker git
systemctl enable --now docker
usermod -aG docker ec2-user

# Docker Compose v2 as a CLI plugin (aarch64 build for Graviton).
# Pinned for reproducibility — see https://github.com/docker/compose/releases
COMPOSE_VERSION="v2.40.2"
echo "Installing Docker Compose $${COMPOSE_VERSION}..."
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL "https://github.com/docker/compose/releases/download/$${COMPOSE_VERSION}/docker-compose-linux-aarch64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version

# App directory that `task prod:deploy` scps the compose file + .env.prod into.
echo "Preparing app directory..."
mkdir -p "/home/ec2-user/$${PROJECT_NAME}"
chown -R ec2-user:ec2-user "/home/ec2-user/$${PROJECT_NAME}"

echo ""
echo "============================================"
echo "  skill-tree-survey bootstrap complete"
echo "============================================"
echo "Next: from a workstation, run  task prod:deploy"
echo "  → ships docker-compose.prod.yml + .env.prod here and starts the stack"
echo "  → cloudflared opens the tunnel; watchtower auto-updates from GHCR"
echo "Logs: /var/log/user-data.log  /var/log/cloud-init-output.log"
echo "============================================"
