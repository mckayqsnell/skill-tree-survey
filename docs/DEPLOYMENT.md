# Deployment

How Skill Tree Survey ships to production. The design goal is **no manual deploy
step for code**: merge to `main` and the running container updates itself.

> First-time setup (provisioning, Cloudflare, Vercel, DNS) is a separate, ordered
> runbook — see [GO_LIVE_CHECKLIST.md](GO_LIVE_CHECKLIST.md). This document covers
> the steady-state pipeline once that's done.

## Pipeline

```
        ┌────────────────────────── Frontend ──────────────────────────┐
push ──▶ Vercel Git integration ──▶ build (pnpm) ──▶ https://skills-survey.<domain>
  │
  │     ┌────────────────────────── Backend ───────────────────────────┐
  └──▶ GitHub Actions (build-and-push.yml)
            └─ build linux/arm64 image ──▶ GHCR :latest + :prod-<sha>
                                              │
                            Watchtower on EC2 polls GHCR every 5 min
                                              │
                                   recreates the backend container
                                              │
                       Cloudflare Tunnel ──▶ https://skills-survey-api.<domain>
```

- **Backend code** → push to `main` (paths `backend/**`) builds an arm64 image and
  pushes it to `ghcr.io/heal-engineering/skill-tree-survey-api` (`:latest` +
  `:prod-<sha>`). [Watchtower](https://github.com/nicholas-fedor/watchtower) on the
  EC2 pulls `:latest` within ~5 minutes and recreates the container (rolling, waits
  for healthy). The SQLite DB lives on a named volume, so it survives the swap.
- **Frontend code** → Vercel's Git integration builds and deploys automatically on
  push to `main` (and gives every PR a preview URL).
- **TLS / routing** → [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
  (`cloudflared` container) terminates TLS at Cloudflare's edge and forwards the
  public hostname to `backend:8000`. It's outbound-only: **no ports are published on
  the box and no certs live on it**.

## Environments

| Environment | Frontend | Backend | Deploy trigger |
|-------------|----------|---------|----------------|
| Local | Vite dev server (`task fe`) | Docker (`task start`) | manual |
| Production | Vercel | EC2 (Graviton) via GHCR + Watchtower | push to `main` |

There is no separate test/staging environment. Vercel preview deployments cover
frontend review; backend changes are validated by CI on the PR.

## Deploying configuration / secrets

Code updates are automatic; **config and secrets are not**. When you change
`docker-compose.prod.yml` or a value in the `SKILL-TREE-PROD` 1Password vault
(e.g. `ADMIN_PASSWORD`, `CORS_ORIGINS`, `SENTRY_DSN`, `TUNNEL_TOKEN`), push it to
the box with:

```bash
task prod:deploy:dry-run   # preview what will happen
task prod:deploy           # regenerate .env.prod from 1Password, scp it +
                           # the compose file to the EC2, recreate the stack
```

`prod:deploy` preflights that you're on `main`, the compose file is committed, the
EC2 is reachable over SSH, and 1Password is signed in. It requires an SSH alias in
`~/.ssh/config` (default `skill-tree`) — see [tasks/prod.yml](../tasks/prod.yml).

```bash
task prod:status   # docker compose ps on the EC2
task prod:logs     # tail backend logs on the EC2
```

## Rollback

Watchtower follows `:latest`, so to pin a known-good build, point the backend image
at a specific SHA tag and redeploy:

```yaml
# docker-compose.prod.yml
backend:
  image: ghcr.io/heal-engineering/skill-tree-survey-api:prod-<good-sha>
```

```bash
task prod:deploy   # ships the pinned compose + restarts
```

While pinned, remove the backend's `com.centurylinklabs.watchtower.enable=true`
label (or stop the `watchtower` container) so it doesn't pull `:latest` back over
your pin. To resume auto-updates, set the image back to `:latest`, restore the
label, and `task prod:deploy`. Past images are retained in GHCR (the
[cleanup workflow](../.github/workflows/cleanup-images.yml) keeps the last 5 `prod-*`).

## Monitoring & verification

- **Health:** `curl https://skills-survey-api.<domain>/health` → `200` with valid
  Cloudflare TLS. Set `PROD_HEALTH_URL` so `task prod:deploy` checks it for you.
- **Containers:** `task prod:status` — `cloudflared`, `backend`, `watchtower` up.
- **Tunnel:** `task prod:logs` (or the cloudflared logs) show "Registered tunnel connection".
- **Errors:** Sentry receives events when `SENTRY_DSN` is set in `SKILL-TREE-PROD`.
- **Data:** survey responses persist across image updates (SQLite on the
  `sqlite_data` named volume).

## Troubleshooting

| Symptom | Check |
|---------|-------|
| New code not live | Actions build green? `task prod:logs` for Watchtower pull; it polls every 5 min |
| 502 / site down | `task prod:status`; is `backend` healthy and `cloudflared` connected? |
| CORS errors in browser | `CORS_ORIGINS` in `SKILL-TREE-PROD` includes the Vercel origin → `task prod:deploy` |
| Tunnel won't start | `TUNNEL_TOKEN` present in `.env.prod` (from 1Password)? |
| Frontend can't reach API | `VITE_API_URL` in Vercel = `https://skills-survey-api.<domain>` |

## Related

- [GO_LIVE_CHECKLIST.md](GO_LIVE_CHECKLIST.md) — one-time go-live steps (Cloudflare, Vercel, DNS, AWS)
- [AWS_SETUP.md](AWS_SETUP.md) — EC2 + Docker + Cloudflare Tunnel host setup
- [infrastructure/terraform/README.md](../infrastructure/terraform/README.md) — provisioning the EC2 with Terraform
