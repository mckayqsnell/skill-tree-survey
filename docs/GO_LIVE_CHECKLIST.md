# Go-Live Checklist — manual / web steps

Everything in the modernization that **a human has to do by hand** (cloud
dashboards, AWS, DNS, secrets, publication) — in dependency order, with what to
do, where, and how to verify it. Code/infra is in the repo; this file is the
human runbook that ties it together.

> **How to use:** work top to bottom — each step lists the **gate** ("do this
> when…") so you don't do it too early. Claude will also flag the next pending
> step in chat as each phase lands. Tick the boxes as you go.

---

## Decisions (confirmed)

- ✅ **Backend hostname** (Cloudflare Tunnel): `api.skills-survey.heal.engineering`
- ✅ **Frontend hostname** (Vercel): `skills-survey.heal.engineering`
- ✅ **MIT LICENSE copyright holder**: `HEAL USA Inc.`

---

## Status snapshot

| # | Step | Gate (do it when…) | Status |
|---|------|--------------------|--------|
| 0 | 1Password vaults + Sentry DSN | — | ✅ done |
| 1 | Cloudflare Tunnel + `TUNNEL_TOKEN` + CORS | before first prod deploy | ⬜ |
| 2 | AWS credentials ready | before Terraform | ⬜ |
| 3 | Terraform: provision **fresh** prod EC2 (+EIP, **with Claude**) → update SSH config | after Phase 6 merged | ⬜ |
| 4 | Build image to GHCR + make package **public** | before first prod deploy | ⬜ |
| 5 | First `task prod:deploy` to the new box + verify tunnel | after 1, 3, 4 | ⬜ |
| 6 | Terminate the **OLD** box + arm `prevent_destroy` | after 5 verifies green | ⬜ |
| 7 | Vercel project + domain (frontend) | after backend hostname is live | ⬜ |
| 8 | **Drop the test EC2** + test DNS | after prod confirmed healthy | ⬜ |
| 9 | Make repo public (open-source) | after Phase 7 docs + secret scrub | ⬜ |
| 10 | Final end-to-end verification | last | ⬜ |

---

## Step 1 — Cloudflare Tunnel (backend TLS + routing)

**Gate:** before the first prod deploy — `cloudflared` won't start without `TUNNEL_TOKEN`.
**Where:** Cloudflare dashboard (the `heal.engineering` zone must already be on Cloudflare).

1. [ ] **Zero Trust → Networks → Tunnels → Create a tunnel** → connector **Cloudflared** → name it `skill-tree-survey`.
2. [ ] Copy the tunnel **token** (the long `eyJ…` string in the install command — just the token).
3. [ ] Save it in **1Password → `SKILL-TREE-PROD` → item `TUNNEL_TOKEN`** (value in the password/credential field, tag `backend`).
4. [ ] Add a **Public Hostname** to the tunnel:
   - Subdomain `api.skills-survey`, Domain `heal.engineering`
   - Service: **Type `HTTP`**, **URL `backend:8000`** ← the compose service name + port (cloudflared shares the compose network; **not** `localhost`).
5. [ ] Save — Cloudflare auto-creates the DNS `CNAME` (`api.skills-survey…` → `<id>.cfargotunnel.com`).
6. [ ] Set **1Password → `SKILL-TREE-PROD` → `CORS_ORIGINS`** to include the frontend origin: `["https://skills-survey.heal.engineering"]`.

**Verify:** nothing yet (backend isn't deployed) — verified in Step 5.

---

## Step 2 — AWS credentials

**Gate:** before running Terraform (Step 3).

1. [ ] Have AWS CLI creds for account **`463932052589`**, region **`us-east-2`**, with EC2 + access to the shared `heal-terraform-state` S3 bucket (and its KMS key).
2. [ ] Confirm: `aws sts get-caller-identity` → account `463932052589`.

---

## Step 3 — Terraform: provision a FRESH prod EC2  (do this **with Claude**)

**Gate:** after Phase 6 (Terraform) is merged; can run in parallel with Step 4.
**Where:** `infrastructure/terraform/` — full runbook in [its README](../infrastructure/terraform/README.md).

We stand up a brand-new box (no risky import). `prevent_destroy` is `false` for now.

1. [ ] `terraform init`
2. [ ] `terraform plan -var-file=environments/prod.tfvars` → expect **creates only** (instance, EIP, association, SG). Nothing destroyed.
3. [ ] `terraform apply -var-file=environments/prod.tfvars`
4. [ ] ⚠️ **Grab the new IP and update SSH** — Claude will remind you here:
   - `terraform output elastic_ip`
   - Point `~/.ssh/config` `Host skill-tree` → that IP (this is the alias `task prod:deploy` uses).
5. [ ] Wait for first-boot Docker install: `ssh skill-tree 'cloud-init status --wait'` (~1–3 min).

(The old box keeps running on its old IP until you terminate it in Step 6 — zero downtime cutover.)

---

## Step 4 — Build the backend image to GHCR + make it public

**Gate:** before the first prod deploy (compose pulls `…/skill-tree-survey-api:latest`).
**Where:** GitHub Actions + GitHub org package settings.

1. [ ] Trigger a build:
   - **Recommended:** merge `develop → main` (the finale) — `build-and-push.yml` builds arm64 on push to `main`.
   - **Early test:** GitHub → **Actions → "Build and Push Image" → Run workflow** (`workflow_dispatch`).
2. [ ] Confirm the package appears: GitHub → org **HEAL-Engineering → Packages → `skill-tree-survey-api`**.
3. [ ] ⚠️ **Make the package Public:** Package → **Package settings → Change visibility → Public**. (So Watchtower/compose pull with no auth.)
4. [ ] Verify from a logged-out shell: `docker pull ghcr.io/heal-engineering/skill-tree-survey-api:latest`.

---

## Step 5 — First production deploy (to the new box)

**Gate:** after Steps 1 (token), 3 (new box + EIP + SSH), 4 (image public).
**Where:** your workstation (1Password unlocked + signed in; `task env:setup` if needed).

1. [ ] On `main` (preflight requires it; or `FORCE=1` to test from the branch).
2. [ ] `task prod:deploy:dry-run` → review the plan.
3. [ ] `task prod:deploy` → regenerates `.env.prod` from `SKILL-TREE-PROD`, ships it + `docker-compose.prod.yml`, `compose up -d`, verifies the backend container is healthy.

**Verify:**
- [ ] `curl https://api.skills-survey.heal.engineering/health` → `200` with **valid TLS** (Cloudflare's edge cert — no cert work). Tip: set `PROD_HEALTH_URL=https://api.skills-survey.heal.engineering/health` so `task prod:deploy` checks it for you.
- [ ] `task prod:status` → `cloudflared`, `backend`, `watchtower` all up.
- [ ] `task prod:logs` → cloudflared shows "Registered tunnel connection".

---

## Step 6 — Retire the OLD box + arm the destroy guard

**Gate:** **after** Step 5 verifies the new box is healthy (clean cutover).
**Where:** AWS (us-east-2) + `infrastructure/terraform/`.

1. [ ] ⚠️ **Data:** the new box started with an **empty** SQLite DB. To keep existing survey responses, copy the old DB across **before** terminating (locate it on the old box — old docker volume / `/app/data/skill_survey.db`). A clean slate? Skip.
2. [ ] Terminate the old hand-built instance: `aws ec2 terminate-instances --instance-ids i-0ae247d6ac4fff53a --region us-east-2`.
3. [ ] (Optional) delete its old security group once nothing uses it: `aws ec2 delete-security-group --group-id sg-0522c32dc40fb86e4 --region us-east-2`.
4. [ ] **Arm the guard:** set `prevent_destroy = true` in `infrastructure/terraform/ec2.tf`, then `terraform apply -var-file=environments/prod.tfvars` (no-op apply, just enables the guard). Commit the change.

---

## Step 7 — Vercel (frontend hosting)

**Gate:** after the backend hostname is live (Step 1/5) so `VITE_API_URL` is correct.
**Where:** Vercel dashboard + Cloudflare DNS.

1. [ ] **Add New Project** → import GitHub repo `HEAL-Engineering/skill-tree-survey`.
2. [ ] Settings:
   - **Root Directory: `frontend`**
   - Framework Preset: **Vite** (`vercel.json` already sets the SPA rewrite; pnpm auto-detected via `packageManager`).
   - Build `pnpm build`, Output `dist` (defaults).
   - **Production Branch: `main`**.
3. [ ] **Environment Variables** (Production) — both are `VITE_` = **public/client-exposed, never put secrets here**:
   - [ ] `VITE_API_URL` = `https://api.skills-survey.heal.engineering`
   - [ ] `VITE_CLOUDFRONT_URL` = your icon-asset host. ⚠️ Without it, survey icons fall back to a dead `https://example.cloudfront.net` placeholder. Use the value prod used previously, or host the icons and set it.
4. [ ] Deploy. Then **Settings → Domains → add `skills-survey.heal.engineering`** → Vercel shows a DNS record → add it in **Cloudflare DNS** (follow Vercel's proxy guidance).

**Verify:**
- [ ] `https://skills-survey.heal.engineering` loads; complete a survey end-to-end; admin loads (analytics + drag-drop).
- [ ] Browser Network tab → API calls hit `api.skills-survey…` and succeed (**no CORS errors** — confirms `CORS_ORIGINS` includes the Vercel domain).
- [ ] Survey **icons render** (the `VITE_CLOUDFRONT_URL` check).

---

## Step 8 — Drop the TEST environment

**Gate:** **after** prod is confirmed healthy (Steps 5–7) — don't remove the fallback early.
**Where:** AWS (us-east-2) + Cloudflare DNS + GitHub.

1. [ ] Find the test instance (was `test-skills-survey.heal.engineering`):
   `aws ec2 describe-instances --region us-east-2 --filters "Name=instance-state-name,Values=running" --query 'Reservations[].Instances[].{id:InstanceId,name:Tags[?Key==\`Name\`]|[0].Value,ip:PublicIpAddress}'`
2. [ ] **Terminate** it: `aws ec2 terminate-instances --instance-ids <test-id> --region us-east-2`.
3. [ ] Release any **test Elastic IP** (else it bills): `aws ec2 release-address --allocation-id <alloc-id> --region us-east-2`.
4. [ ] Delete the test-only security group (if dedicated).
5. [ ] **Cloudflare DNS:** remove `test-skills-survey.heal.engineering` (and any stale old-prod `A` record now replaced by the tunnel CNAME).
6. [ ] **GitHub → Settings → Environments:** delete any `test` environment + its secrets. (Test deploy workflows were already removed in Phase 5.)

**Verify:** [ ] nothing resolves/deploys to the test host anymore.

---

## Step 9 — Open-source the repo

**Gate:** after Phase 7 (docs + `LICENSE`) **and** a secret-history scrub.
**Where:** GitHub repo settings.

1. [ ] ⚠️ **Secret scrub — current tree AND git history.** Old compose/docs had placeholder creds (`admin123`); make sure no **real** secret, token, or cert was ever committed. If history has a real secret → **rotate it** and/or rewrite history (`git filter-repo`) before going public. _(Phase 7 verified the current tree: no `.env*`, private keys, tokens, or Sentry DSNs are tracked. History still needs a pass.)_
2. [ ] ⚠️ **Internal infrastructure identifiers** — not secrets, but decide before publishing. The AWS **account ID**, **instance/VPC/subnet/SG IDs**, and **Elastic IP** appear in `infrastructure/terraform/environments/prod.tfvars` (VPC + subnet) and in this checklist. Options: gitignore `*.tfvars` and commit a `prod.tfvars.example` with placeholders, and/or move this checklist to an internal location. Decide with the team.
3. [ ] Confirm `LICENSE` (MIT, `HEAL USA Inc.`) + accurate `README` are present.
4. [ ] GitHub → **Settings → General → Danger Zone → Change visibility → Public**.
5. [ ] Confirm the **GHCR package is Public** (Step 4) and Actions still run on the public repo.

---

## Step 10 — Final end-to-end verification

- [ ] Frontend (Vercel domain) loads; survey + admin fully work in both themes.
- [ ] Backend health via tunnel = `200`, valid TLS.
- [ ] **Auto-deploy loop:** push a trivial backend change to `main` → Actions builds → **Watchtower** updates the container within ~5 min (`task prod:logs`).
- [ ] **Sentry** receives events (check the project after a deploy / handled error).
- [ ] **Data persists:** survey data survives a Watchtower image update (SQLite is on the `sqlite_data` named volume).
- [ ] SSH still works against the EIP; `ssh_allowed_cidrs` tightened from `0.0.0.0/0` if desired.
- [ ] `prevent_destroy = true` is committed (armed in Step 6).

---

### Quick dependency map

```
Decisions (confirmed)
   ├─▶ Step 1 Cloudflare Tunnel (TUNNEL_TOKEN, CORS) ─┐
   └─▶ Step 7 Vercel (VITE_API_URL, CORS) ◀───────────┤ (needs backend hostname)
Step 2 AWS creds ─▶ Step 3 Terraform (fresh box + EIP) ─▶ update SSH ─┐
Step 4 GHCR image (public) ───────────────────────────────────────────┤
                                                                       ▼
                                                   Step 5 prod deploy ─▶ verify
                                                                       │
                                       (new box green) ─▶ Step 6 terminate old + arm prevent_destroy
                                          (prod healthy) ─▶ Step 8 drop test
                              (Phase 7 docs + scrub) ─▶ Step 9 public ─▶ Step 10 verify
```
