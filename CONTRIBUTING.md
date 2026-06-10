# Contributing to Skill Tree Survey

Thanks for contributing! This guide covers local setup, conventions, and the PR
process. For architecture and deeper conventions, see [CLAUDE.md](CLAUDE.md).

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Compose v2
- [Task](https://taskfile.dev/installation/) — the task runner (`task --list` shows everything)
- [uv](https://docs.astral.sh/uv/) — Python package/venv manager (backend)
- [Node 22.13+](https://nodejs.org/) + [pnpm 11](https://pnpm.io/) (`corepack enable`) — frontend
- _(optional)_ [1Password CLI](https://developer.1password.com/docs/cli/) — for real secrets; the app runs on safe defaults without it.

## Local setup

```bash
git clone https://github.com/HEAL-Engineering/skill-tree-survey.git
cd skill-tree-survey

task dev        # backend (Docker) + frontend (Vite) together
# — or —
task start      # backend only (Docker)
task fe         # frontend dev server (Vite, proxies /api → :8000)
```

The backend works with **no `.env` file** thanks to defaults in
[backend/app/core/config.py](backend/app/core/config.py). To use real secrets,
run `task env:setup` once, then `task env:generate` to write `.env.local` from the
`SKILL-TREE-LOCAL` 1Password vault. See the README's
[Configuration & secrets](README.md#configuration--secrets) section.

Running the backend outside Docker:

```bash
cd backend && uv sync && uv run uvicorn app.main:app --reload
```

## Branching & workflow

Trunk-based — one protected branch:

```
feature branch ──PR──▶ main ──▶ build + auto-deploy
                                 ├─ backend: GHCR image → Watchtower (~5 min)
                                 └─ frontend: Cloudflare Workers
```

- **`main`** — the only long-lived branch, protected. Merging a PR here *is* the
  deploy: the GHCR image build kicks off, Watchtower rolls it onto the EC2, and
  Workers Builds ships the frontend.
- **Feature branches** — `<username>/<ticket-id>/<short-description>`,
  e.g. `nate/HEA-123/add-user-dashboard`. (External contributors: fork and open a
  PR against `main`; the branch name convention is optional.)

```bash
git checkout main && git pull
git checkout -b <username>/<ticket-id>/<short-description>
# …work…
git push -u origin <branch>
gh pr create
```

Keep a long-running branch fresh by rebasing on `main`:

```bash
git fetch origin && git rebase origin/main
git push --force-with-lease
```

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | For |
|--------|-----|
| `feat:` | a new feature |
| `fix:` | a bug fix |
| `docs:` | documentation only |
| `refactor:` | code change that neither fixes a bug nor adds a feature |
| `test:` | adding or fixing tests |
| `chore:` | tooling, deps, config |

## Code style & checks

Run these before opening a PR — CI runs the same checks
([.github/workflows/ci.yml](.github/workflows/ci.yml)):

```bash
# Backend
cd backend
uv run ruff check .          # lint
uv run ruff format .         # auto-format (CI checks --check)
uv run pytest                # tests  (or: task test)

# Frontend
cd frontend
pnpm lint
pnpm typecheck
pnpm build
```

- **Backend:** type hints everywhere; follow the DAO → Service → Route layering;
  log through `settings.logger` (the shared Sentry struct logger), not `print`.
- **Frontend:** TypeScript with no `any` in new code; Composition API (`<script setup>`);
  componentize rather than growing monoliths; verify both the terminal and stiff themes.

## Pull requests

1. Pull/rebase the latest `main` and make sure CI checks pass locally.
2. Keep the PR to a **single clear purpose** (no drive-by refactors).
3. Fill out the [PR template](.github/pull_request_template.md); add tests for new behavior.
4. **Never commit secrets** — no `.env*`, tokens, keys, or real passwords. Secrets
   live in 1Password (`.gitignore` already blocks `.env*`, `*.pem`, `*.key`, `*.crt`).
5. Request review; address Copilot/Claude comments; squash-merge once approved.

## Reporting issues

Open a [GitHub issue](https://github.com/HEAL-Engineering/skill-tree-survey/issues)
with steps to reproduce, expected vs. actual behavior, and environment details.
