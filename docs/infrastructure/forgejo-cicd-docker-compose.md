# Forgejo + Forgejo Actions CI/CD with Docker Compose

> **Last updated:** 2026-06-07  
> **Stack:** Forgejo 1.22 + PostgreSQL 18 + act_runner (Forgejo Actions)

## Overview

Deploy a complete self-hosted Git server with built-in CI/CD using Forgejo Actions — compatible with GitHub Actions workflow syntax.

### Architecture

```
┌─────────────────────────────────────────┐
│  Docker Network                          │
│                                         │
│  ┌──────────┐    ┌──────────────┐       │
│  │ Forgejo  │◄───│ PostgreSQL   │       │
│  │ :3000    │    │ :5432        │       │
│  │ :22      │    └──────────────┘       │
│  └────┬─────┘                           │
│       │ gRPC (registration + jobs)      │
│  ┌────▼─────┐                           │
│  │act_runner│                           │
│  │ (runner) │                           │
│  └──────────┘                           │
└─────────────────────────────────────────┘
```

### Stack Components

| Service | Image | Purpose |
|---------|-------|---------|
| Forgejo | `codeberg.org/forgejo/forgejo:1.22` | Git server + Actions engine |
| PostgreSQL | `postgres:18-alpine` | Metadata storage (required for Actions) |
| act_runner | `gitea/act_runner:latest` | CI job executor (compatible with Forgejo) |

**Why PostgreSQL over SQLite:** Forgejo Actions can corrupt SQLite under concurrent job loads. PostgreSQL 18 Alpine uses ~50MB RAM idle — worth it for reliability.

## Docker Compose Setup

### File Structure

```
project/
├── docker-compose.yml      ← main compose file
├── .env                    ← secrets & config (copy from .env.example)
└── .forgejo/workflows/     ← CI workflow YAML files (per repo)
    └── ci-test.yml         ← example workflow
```

### docker-compose.yml

```yaml
# Forgejo + PostgreSQL + act_runner (Forgejo Actions CI/CD)
# Deploy: docker compose up -d
services:
  db:
    image: postgres:18-alpine
    container_name: forgejo-db
    environment:
      POSTGRES_DB: forgejo
      POSTGRES_USER: forgejo
      POSTGRES_PASSWORD: ${FORGEJO_DB_PASSWORD:?DB password required}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U forgejo"]
      interval: 10s
      timeout: 5s
      retries: 5

  forgejo:
    image: codeberg.org/forgejo/forgejo:1.22
    container_name: forgejo
    environment:
      USER_UID: 1000
      USER_GID: 1000
      FORGEJO__database__DB_TYPE: postgres
      FORGEJO__database__HOST: db:5432
      FORGEJO__database__NAME: forgejo
      FORGEJO__database__USER: forgejo
      FORGEJO__database__PASSWD: ${FORGEJO_DB_PASSWORD:?DB password required}
      FORGEJO__server__DOMAIN: ${FORGEJO_DOMAIN}
      FORGEJO__server__ROOT_URL: ${FORGEJO_ROOT_URL}
      FORGEJO__server__SSH_DOMAIN: ${FORGEJO_SSH_DOMAIN:-${FORGEJO_DOMAIN}}
      FORGEJO__server__HTTP_PORT: 3000
      FORGEJO__server__SSH_PORT: 22
      FORGEJO__actions__ENABLED: true             # ⚡ Enable Actions
      FORGEJO__service__DISABLE_REGISTRATION: false
    volumes:
      - forgejo_data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "${FORGEJO_HTTP_PORT:-3000}:3000"
      - "${FORGEJO_SSH_PORT:-22}:22"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  runner:
    image: gitea/act_runner:latest
    container_name: forgejo-runner
    environment:
      GITEA_INSTANCE_URL: http://forgejo:3000
      GITEA_RUNNER_REGISTRATION_TOKEN: ${FORGEJO_RUNNER_TOKEN:-}
      GITEA_RUNNER_NAME: ${FORGEJO_RUNNER_NAME:-runner-1}
    volumes:
      - runner_data:/data
      - /var/run/docker.sock:/var/run/docker.sock   # Docker-in-Docker for job containers
    depends_on:
      forgejo:
        condition: service_started
    restart: unless-stopped

volumes:
  postgres_data:
  forgejo_data:
  runner_data:
```

### .env

```ini
# Domain (change to yours)
FORGEJO_DOMAIN=git.example.com
FORGEJO_ROOT_URL=https://git.example.com
FORGEJO_SSH_DOMAIN=git.example.com

# Ports
FORGEJO_HTTP_PORT=3000
FORGEJO_SSH_PORT=22

# Database
FORGEJO_DB_PASSWORD=change_this_password

# Runner — fill AFTER Forgejo is running
FORGEJO_RUNNER_TOKEN=
FORGEJO_RUNNER_NAME=runner-1
```

## Setup Steps

### Step 1: Start Database + Forgejo

```bash
docker compose up -d db forgejo
# Wait for healthy, check logs:
docker compose logs -f forgejo
```

### Step 2: Create Admin Account

Open `http://YOUR_IP:3000` in browser:
1. Fill the installation form — create admin username + password
2. Click Install

### Step 3: Get Runner Registration Token

**Option A — via Web UI:**  
Admin Panel (⚙️ top right) → **Actions** → **Runners** → **"Create Runner Registration Token"**

**Option B — via CLI (faster):**  
```bash
docker exec forgejo forgejo actions generate-runner-token
```

### Step 4: Start the Runner

```bash
# Set token in .env
echo 'FORGEJO_RUNNER_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxx' >> .env

# Start runner
docker compose up -d runner

# Verify
docker compose logs runner
# Expected: "Runner registered successfully"
```

### Step 5: Verify

Forgejo UI → **Admin Panel** → **Actions** → **Runners**.  
Runner should show **Idle** (green ✅).

## Example Workflow

File: `.forgejo/workflows/ci-test.yml` (per repository)

```yaml
name: CI Test
on:
  push:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Hello World
        run: echo "CI running on Forgejo Actions!"
      - name: System info
        run: |
          uname -a
          echo "CPU: $(nproc) cores"
          echo "RAM: $(free -h | grep Mem | awk '{print $2}')"
```

Compatible with GitHub Actions — `actions/checkout@v4`, `actions/setup-node`, `docker/login-action`, etc. work without modification.

## Key Details

| Aspect | Notes |
|--------|-------|
| Docker socket mount | Required so runner can spawn job containers (Docker-in-Docker) |
| Token is one-time | Runner saves config to `runner_data` volume after first registration |
| Workflow directory | `.forgejo/workflows/` — NOT `.github/workflows/` |
| GitHub Marketplace actions | Compatible — use them directly |

## Troubleshooting

**Runner can't register:**
```bash
# Test connectivity from runner to Forgejo
docker exec forgejo-runner curl -s http://forgejo:3000
```

**Runner registered but shows offline:**
```bash
docker compose restart runner
```

**Workflow triggered but jobs don't start:**
```bash
docker compose logs runner
# Usually: expired token or runner crashed
```

**Want to use GitHub Marketplace actions?**  
Works out of the box — e.g. `actions/checkout@v4`, `actions/setup-node@v4`.

## Related

- [dokploy-basic-auth](dokploy-basic-auth.md) — Adding basic auth to Compose apps on Dokploy
- [zot-registry](zot-registry.md) — Self-hosted OCI registry with RBAC
