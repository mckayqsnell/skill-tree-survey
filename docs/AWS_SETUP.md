# AWS / Host Setup

The backend runs as Docker containers on a single AWS EC2 instance. There is **no
nginx and no certbot** — [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
handles TLS and routing, so the box only needs Docker and an outbound connection.

## What runs on the box

Three containers, defined in [docker-compose.prod.yml](../docker-compose.prod.yml):

| Container | Image | Role |
|-----------|-------|------|
| `backend` | `ghcr.io/heal-engineering/skill-tree-survey-api:latest` | FastAPI on `:8000` (not published) |
| `cloudflared` | `cloudflare/cloudflared` | Outbound tunnel → routes the public hostname to `backend:8000` |
| `watchtower` | `ghcr.io/nicholas-fedor/watchtower` | Polls GHCR every 5 min, auto-updates `backend` |

SQLite persists on the `sqlite_data` named volume, so image updates don't lose data.

## Instance

- **Type:** `t4g.medium` — AWS Graviton (**arm64**). The CI image is built for
  `linux/arm64` to match, so the instance architecture matters.
- **OS:** Amazon Linux 2023 (arm64).
- **Networking:** an Elastic IP for stable SSH; the app is reached via the tunnel,
  not the IP.
- **Security group:** inbound **SSH (22) only** — the tunnel is outbound, so 80/443
  are never opened. All egress allowed.

## Provisioning (recommended: Terraform)

The instance, Elastic IP, and security group are managed as code in
[infrastructure/terraform/](../infrastructure/terraform/). Terraform's `user_data`
([scripts/user_data.sh](../infrastructure/terraform/scripts/user_data.sh)) installs
Docker + the Compose plugin on first boot. Follow the runbook in
[infrastructure/terraform/README.md](../infrastructure/terraform/README.md):

```bash
cd infrastructure/terraform
terraform init
terraform plan  -var-file=environments/prod.tfvars
terraform apply -var-file=environments/prod.tfvars
terraform output elastic_ip       # point ~/.ssh/config Host skill-tree at this
```

Then ship the stack from your workstation:

```bash
task prod:deploy                   # scp .env.prod + compose, docker compose up -d
```

See [GO_LIVE_CHECKLIST.md](GO_LIVE_CHECKLIST.md) for the full first-time sequence
(Cloudflare Tunnel token, GHCR image, Vercel, DNS).

## Provisioning (manual fallback)

If you're standing the host up by hand instead of Terraform:

```bash
# On a fresh Amazon Linux 2023 (arm64) instance
sudo dnf update -y
sudo dnf install -y docker git
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user        # re-login for this to take effect

# Docker Compose plugin (aarch64)
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-aarch64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
```

The backend image is **public** on GHCR, so no `docker login` is needed to pull it.
Create the app directory `task prod:deploy` ships into:

```bash
mkdir -p ~/skill-tree-survey
```

## SSH access

`task prod:deploy` / `task prod:status` / `task prod:logs` use an SSH alias
(default `skill-tree`). Add it to `~/.ssh/config`:

```sshconfig
Host skill-tree
  HostName <elastic-ip>
  User ec2-user
  IdentityFile ~/.ssh/skill-tree-keypair.pem
```

## Backups

SQLite is a single file on the `sqlite_data` volume. To snapshot it:

```bash
ssh skill-tree 'docker cp skill-tree-survey-backend:/app/data/skill_survey.db -' \
  > skill_survey-$(date +%Y%m%d).db
```

## Notes

- **No inbound 80/443** — if you ever see a request to open them, the tunnel isn't
  wired correctly; fix the tunnel instead.
- The box needs **no AWS API credentials** at runtime (SQLite is local, the image is
  public, secrets arrive via `task prod:deploy`), so it has no IAM instance role.
