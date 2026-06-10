# skill-tree-survey — Terraform Infrastructure

Infrastructure as Code for the single production EC2 instance that runs
skill-tree-survey. Modeled on heal-api's Terraform, but **deliberately
minimal** — this app is a FastAPI + SQLite backend fronted by a Cloudflare
Tunnel, so most of heal-api's moving parts don't apply here.

## Architecture

```
                  ┌──────────────────── Cloudflare edge (TLS) ───────────────┐
   Browser  ──────▶  api.<domain>  ──▶  Cloudflare Tunnel  (outbound-only)    │
                  └───────────────────────────────┬──────────────────────────┘
                                                   │  (tunnel established FROM the box)
        ┌──────────────────────────────────────────▼───────────────────────┐
        │  EC2  t4g.medium (arm64, AL2023)   us-east-2 / default VPC         │
        │                                                                    │
        │   cloudflared ──┐                                                  │
        │   backend  ◀────┘  FastAPI + SQLite (named docker volume)          │
        │   watchtower ──▶ polls GHCR :latest, auto-updates backend          │
        │                                                                    │
        │   Inbound SG: 22 (SSH) only        Outbound: all                   │
        └────────────────────────────────────────────────────────────────────┘

   Frontend (Vue) is hosted separately on Vercel — not managed here.
```

## What this manages

| Resource | Notes |
|----------|-------|
| `aws_instance.api` | The prod box. **Created fresh**, then we cut over to it. |
| _(no Elastic IP)_ | Account EIP quota is full — SSH uses the auto-assigned public IP (`terraform output public_ip`); it changes on stop/start. |
| `aws_security_group.ec2` | SSH-in + all-out. No 80/443 (tunnel is outbound). |

## What it deliberately does NOT manage (unlike heal-api)

- **No Aurora / RDS / SSM lookups** — data is SQLite on a named Docker volume.
- **No nginx / certbot / htpasswd** — Cloudflare Tunnel terminates TLS.
- **No IAM role / instance profile** — the box needs no AWS API access at
  runtime (image is public on GHCR; secrets arrive via scp; DB is local).
- **No Cognito, KMS, Lambda, CloudWatch alarms, SNS/Slack.**
- **No S3 bucket / lock-table resources** — the shared `heal-terraform-state`
  bucket is owned by heal-api; we only consume it under our own state key.

## Prerequisites

1. **Terraform** ≥ 1.14
2. **AWS credentials** for the HEAL AWS account (1Password → `SKILL-TREE-INFRA`
   → `AWS_ACCOUNT_ID`), region `us-east-2`, with access to EC2 + the shared
   `heal-terraform-state` S3 bucket (and its KMS key).
3. **1Password CLI signed in** — the tfvars are generated from it (below).
   There are no *secret* Terraform variables (secrets live in `.env.prod`,
   shipped by `task prod:deploy`), but the internal infra IDs are kept out of
   the public repo.

## Variables (tfvars from 1Password)

`environments/prod.tfvars` is **gitignored** — the real values (VPC + subnet
IDs) live in the 1Password vault **`SKILL-TREE-INFRA`** (items tagged `tfvar`,
titles lowercased into keys). Generate the file locally:

```bash
task tf:gen        # writes environments/prod.tfvars (from the repo root)
```

Only inputs **without defaults** in `variables.tf` are needed; everything else
(instance type, key pair, volume size, SSH CIDRs) uses its default — override
by adding a tagged item to the vault. A placeholder
`environments/prod.tfvars.example` is committed for shape reference. The vault
also holds reference-only records (no `tfvar` tag): `AWS_ACCOUNT_ID`,
`OLD_INSTANCE_ID`, `OLD_SG_ID`.

## State

```
s3://heal-terraform-state/skill-tree-survey/terraform.tfstate   (default workspace)
```

S3 native locking (`use_lockfile = true`) — the bucket is shared with heal-api
but this project has its **own key**, so the two never collide. Single prod
environment ⇒ no workspaces; run plain `terraform` with the tfvars.

---

## Provision the production instance (fresh) + cutover

We **stand up a brand-new instance** and cut over to it, rather than importing
the old hand-built box. The new box auto-installs Docker via `user_data`, then
`task prod:deploy` ships the app onto it. The old instance (1Password →
`SKILL-TREE-INFRA` → `OLD_INSTANCE_ID`) is terminated **manually** afterward —
it's not in Terraform state.

`prevent_destroy` is **false** during stand-up (see `ec2.tf`) so the first apply
runs cleanly and can be re-run freely. You flip it to `true` once prod is live.

> ⚠️ **Data:** the new box starts with an **empty** SQLite database. If you want
> to keep the existing survey responses, copy the old DB across before you
> terminate the old box (see step 6). If a clean slate is fine, skip it.

### Runbook (run with AWS creds present)

```bash
# 0. From the repo root: write the gitignored tfvars from 1Password.
task tf:gen

cd infrastructure/terraform

# 1. Initialize the S3 backend (creates the state object under our key).
terraform init

# 2. Review the plan — expect 2 creates: instance + security group (no EIP —
#    account quota is full). NOTHING destroyed (the old box isn't in state).
terraform plan -var-file=environments/prod.tfvars

# 3. Create the instance.
terraform apply -var-file=environments/prod.tfvars

# 4. Grab the new public IP and update your SSH config.
terraform output public_ip           # e.g. 3.x.x.x
terraform output ssh_command         # ready-made ssh line
```

(`task tf:plan` / `task tf:apply` from the repo root wrap steps 2–3 and
auto-generate the tfvars if missing.)

Point the **`skill-tree`** SSH host (used by `task prod:deploy`) at that IP:

```sshconfig
# ~/.ssh/config
Host skill-tree
  HostName <public_ip from above>
  User ec2-user
  IdentityFile ~/.ssh/skill-tree-keypair.pem
```

```bash
# 5. Wait for first-boot provisioning to finish (Docker install), then deploy.
ssh skill-tree 'cloud-init status --wait'   # ~1-3 min on first boot
#   ...from the repo root:
task prod:deploy                            # ships compose + .env.prod, starts the stack
#   verify: curl https://skills-survey-api.heal.engineering/health  → 200
```

```bash
# 6. (Optional) migrate existing survey data from the OLD box, THEN terminate it.
#    The old box still answers at its old public IP until you change DNS/SSH.
#      - copy the old SQLite file into the new box's sqlite_data volume, or skip.
#    IDs: 1Password → SKILL-TREE-INFRA → OLD_INSTANCE_ID / OLD_SG_ID
aws ec2 terminate-instances --region us-east-2 \
  --instance-ids "$(op read 'op://SKILL-TREE-INFRA/OLD_INSTANCE_ID/password')"
#    (optional) delete the old security group once nothing else uses it:
aws ec2 delete-security-group --region us-east-2 \
  --group-id "$(op read 'op://SKILL-TREE-INFRA/OLD_SG_ID/password')"

# 7. Lock prod down: set `prevent_destroy = true` in ec2.tf, then:
terraform apply -var-file=environments/prod.tfvars   # no-op change, just arms the guard
```

---

## Day-to-day

```bash
task tf:plan       # from the repo root — review first (generates tfvars if missing)
task tf:apply
terraform -chdir=infrastructure/terraform output     # IPs, instance id, etc.
```

(`prod.tfvars` is local-only; on a fresh clone run `task tf:gen` once.)

## Bootstrap (user_data)

`scripts/user_data.sh` runs on first boot and installs Docker + the Compose
plugin and preps the app dir. It does **not** start the app — that's
`task prod:deploy` (ships `docker-compose.prod.yml` + `.env.prod`), after which
Watchtower keeps the backend image current from GHCR. (Changing `user_data`
later forces a replacement; that's expected for a managed box — see "rebuild".)

## Rebuilding / replacing the box later

Once `prevent_destroy = true`, Terraform will refuse to replace the instance —
a good guard. To intentionally rebuild (OS upgrade, changed `user_data`, etc.):

1. Set `prevent_destroy = false` in `ec2.tf`.
2. ⚠️ **Back up first** — the SQLite volume lives on the instance. Snapshot/copy
   `/app/data` (the `sqlite_data` Docker volume) or you lose survey data.
3. `terraform apply` (or `terraform taint aws_instance.api` then apply).
4. Re-`task prod:deploy`, restore data, re-verify, then set `prevent_destroy = true`.

## Relationship to the rest of the repo

Terraform owns the **machine**. The **application** lifecycle is separate:

- `task prod:deploy` → ships compose + secrets to the box.
- GitHub Actions (`build-and-push.yml`) → builds the arm64 image to GHCR on
  merge to `main`.
- Watchtower (in `docker-compose.prod.yml`) → pulls new images automatically.
