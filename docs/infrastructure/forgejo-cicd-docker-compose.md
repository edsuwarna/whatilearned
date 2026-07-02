---
title: Forgejo + Forgejo Actions CI/CD with Docker Compose
description: - [Overview](#overview)
---

# Forgejo + Forgejo Actions CI/CD with Docker Compose

> **Last updated:** 2026-06-07  
> **Stack:** Forgejo 15 + PostgreSQL 18 + Forgejo Runner (Forgejo Actions)


## Table of Contents

- [Overview](#overview)
  - [Architecture](#architecture)
  - [Stack Components](#stack-components)
- [Docker Compose Setup](#docker-compose-setup)
  - [File Structure](#file-structure)
  - [docker-compose.yml](#docker-composeyml)
  - [.env](#env)
- [Setup Steps](#setup-steps)
  - [Step 1: Start Database + Forgejo](#step-1-start-database-forgejo)
  - [Step 2: Create Admin Account](#step-2-create-admin-account)
  - [Step 3: Get Runner Registration Token](#step-3-get-runner-registration-token)
  - [Step 4: Start the Runner](#step-4-start-the-runner)
  - [Step 5: Verify](#step-5-verify)
- [Example Workflow](#example-workflow)
- [Key Details](#key-details)
- [Reverse Proxy Setup](#reverse-proxy-setup)
  - [Option A: Nginx](#option-a-nginx)
  - [Option B: Traefik (Docker)](#option-b-traefik-docker)
- [SSH Setup for Git Operations](#ssh-setup-for-git-operations)
  - [Understanding SSH Port Mapping](#understanding-ssh-port-mapping)
  - [Adding SSH Keys to Forgejo](#adding-ssh-keys-to-forgejo)
  - [Clone, Push, Pull](#clone-push-pull)
  - [Simplify with ~/.ssh/config](#simplify-with-sshconfig)
  - [Verify SSH Connection](#verify-ssh-connection)
  - [Common SSH Issues](#common-ssh-issues)
- [Object Storage (S3-Compatible)](#object-storage-s3-compatible)
  - [Which Data Can Use Object Storage?](#which-data-can-use-object-storage)
  - [Generic S3 Pattern](#generic-s3-pattern)
  - [Provider Examples](#provider-examples)
  - [Recommendation for MiniPC (4c/8GB/512GB)](#recommendation-for-minipc-4c8gb512gb)
  - [Migrating Existing Data](#migrating-existing-data)
- [Troubleshooting](#troubleshooting)
- [Related](#related)

## Overview

Deploy a complete self-hosted Git server with built-in CI/CD using Forgejo Actions — compatible with GitHub Actions workflow syntax.

### Architecture

```text
┌─────────────────────────────────────────────────┐
│  Docker Network                                  │
│                                                  │
│  ┌──────────┐    ┌──────────────┐                │
│  │ Forgejo  │◄───│ PostgreSQL   │                │
│  │ :3000    │    │ :5432        │                │
│  │ :22      │    └──────────────┘                │
│  └────┬─────┘                                    │
│       │ HTTP polling (register → job fetch)      │
│  ┌────▼──────────────────────┐                   │
│  │  Forgejo Runner          │                   │
│  │  (data.forgejo/runner:12) │                   │
│  │                          │                   │
│  │  ┌──────────────────┐    │                   │
│  │  │ docker-in-docker │    │                   │
│  │  │ (dind)           │    │                   │
│  │  └──────────────────┘    │                   │
│  └──────────────────────────┘                   │
└─────────────────────────────────────────────────┘
```

### Stack Components

| Service | Image | Purpose |
|---------|-------|---------|
| Forgejo | `codeberg.org/forgejo/forgejo:15` | Git server + Actions engine |
| PostgreSQL | `postgres:18-alpine` | Metadata storage (required for Actions) |
| Forgejo Runner | `data.forgejo.org/forgejo/runner:12` | CI job executor |

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
# Forgejo + PostgreSQL + Forgejo Runner (Forgejo Actions CI/CD)
# Deploy: docker compose up -d
#
# IMPORTANT: Forgejo 15.x uses OFFLINE REGISTRATION for runners
# See Step 3-4 below for runner UUID+Token setup

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
    image: codeberg.org/forgejo/forgejo:15
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

  # ⚠️ Runner requires manual setup BEFORE first start:
  # 1. Create runner in Forgejo UI → get UUID + Token
  # 2. Generate config: docker run --rm data.forgejo.org/forgejo/runner:12 forgejo-runner generate-config > ./data/runner-config.yml
  # 3. Edit config: add server.connections.forgejo with url, uuid, token
  docker-in-docker:
    image: docker:dind
    container_name: 'forgejo-dind'
    privileged: true
    command: ['dockerd', '-H', 'tcp://0.0.0.0:2375', '--tls=false']
    restart: 'unless-stopped'

  runner:
    image: 'data.forgejo.org/forgejo/runner:12'
    depends_on:
      docker-in-docker:
        condition: service_started
    container_name: 'forgejo-runner'
    environment:
      DOCKER_HOST: tcp://docker-in-docker:2375
    user: 1001:1001
    volumes:
      - ./data:/data
    restart: 'unless-stopped'
    command: 'forgejo-runner daemon --config /data/runner-config.yml'

volumes:
  postgres_data:
  forgejo_data:
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
```

> **No runner token in .env:** Forgejo 15.x uses offline registration via config file (UUID + Token), not env vars.

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

### Step 3: Get Runner UUID + Token (Offline Registration)

Forgejo 15.x uses **offline registration** — you create the runner in the UI and get a UUID+Token pair, then configure the runner with those values.

1. In Forgejo UI, go to **Settings** (⚙️ top right) → **Actions** → **Runners**
2. Click **"Create new runner"**
3. Enter a name (e.g., `runner-1`) → click **Create**
4. **Copy the UUID and Token** shown — they appear only once!

> ⚠️ This is **not** a "registration token" — it's a permanent UUID + Token pair for the runner's config file.

### Step 4: Configure and Start the Runner

First, prepare the data directory with proper permissions:

```bash
# Create data directory for runner config
mkdir -p ./data/.cache
sudo chown -R 1001:1001 ./data
sudo chmod 775 ./data/.cache
sudo chmod g+s ./data/.cache
```

Generate the default config file:

```bash
docker run --rm data.forgejo.org/forgejo/runner:12 forgejo-runner generate-config > ./data/runner-config.yml
```

Edit `./data/runner-config.yml` and add the runner credentials under the `server` section:

```yaml
# ./data/runner-config.yml
server:
  connections:
    forgejo:
      url: http://forgejo:3000
      uuid: <UUID_FROM_UI>
      token: <TOKEN_FROM_UI>
```

Now start all services:

```bash
# Start everything (db + forgejo + dind + runner)
docker compose up -d

# Check runner logs
docker compose logs -f runner
# Expected: Runner daemon started successfully
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
| Docker socket | Not mounted — runner uses docker-in-docker (dind) sidecar for isolation |
| Registration | Offline: create runner in UI → get UUID+Token → put in `runner-config.yml` |
| Config file | `./data/runner-config.yml` with `server.connections.forgejo` section |
| Workflow directory | `.forgejo/workflows/` — NOT `.github/workflows/` |
| GitHub Marketplace actions | Compatible — use them directly |

## Reverse Proxy Setup

Forgejo needs HTTP and SSH exposed. Both Nginx and Traefik can proxy HTTP (port 3000), but **SSH must still be directly mapped** on the host since reverse proxies don't natively proxy SSH (it's not HTTP).

### Option A: Nginx

Nginx reverse proxy for HTTPS termination + WebSocket support (needed for Git operations over HTTP).

**`/etc/nginx/sites-available/forgejo`:**

```nginx
server {
    listen 80;
    server_name git.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name git.example.com;

    ssl_certificate /etc/letsencrypt/live/git.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/git.example.com/privkey.pem;

    # Max upload size for large repos
    client_max_body_size 512m;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (required for Git operations)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable and reload:
```bash
sudo ln -s /etc/nginx/sites-available/forgejo /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

**SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d git.example.com
```

### Option B: Traefik (Docker)

If using Traefik (via Dokploy or standalone), add labels to the Forgejo service directly in `docker-compose.yml`:

```yaml
  forgejo:
    # ... existing config ...
    ports:
      - "${FORGEJO_HTTP_PORT:-3000}:3000"
      - "${FORGEJO_SSH_PORT:-22}:22"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.forgejo.rule=Host(`${FORGEJO_DOMAIN}`)"
      - "traefik.http.routers.forgejo.entrypoints=websecure"
      - "traefik.http.routers.forgejo.tls=true"
      - "traefik.http.routers.forgejo.tls.certresolver=letsencrypt"
      - "traefik.http.services.forgejo.loadbalancer.server.port=3000"
```

If deploying on **Dokploy**, go to Forgejo app → **Networking** tab:
- **Port:** `3000` (HTTP)
- **Domain:** `git.example.com`
- Traefik handles SSL automatically via Dokploy's ACME config

**Important for Traefik:** HTTP port mapping (`3000:3000`) is still needed for Forgejo to properly detect its own URL. The Traefik labels route external traffic to the container's port 3000.

## SSH Setup for Git Operations

### Understanding SSH Port Mapping

Forgejo container exposes SSH on port 22 internally. On the host, you have two options:

| Approach | Host Port | Command |
|----------|-----------|---------|
| **Direct (if host SSH on alt port)** | `22:22` | `ssh://git@git.example.com/user/repo.git` |
| **Custom port (recommended)** | `2222:22` | `ssh://git@git.example.com:2222/user/repo.git` |

**If host already uses port 22** (default SSH server), map Forgejo SSH to a different host port:

```yaml
# docker-compose.yml
services:
  forgejo:
    ports:
      - "2222:22"    # Host:2222 → Container:22
```

```ini
# .env
FORGEJO_SSH_PORT=2222
FORGEJO_SSH_DOMAIN=git.example.com
```

Forgejo automatically uses these values to display the correct clone URL in the UI.

### Adding SSH Keys to Forgejo

1. Generate a key pair if you don't have one:
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```

2. Copy the public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. Add to Forgejo:
   - Profile (top right avatar) → **Settings** → **SSH / GPG Keys** → **Add Key**
   - Paste your public key → **Add Key**

### Clone, Push, Pull

**With custom port (2222):**

```bash
# Clone
git clone ssh://git@git.example.com:2222/username/repo-name.git

# Or if already cloned, set remote
git remote add origin ssh://git@git.example.com:2222/username/repo-name.git

# Push/pull work normally after that
git push origin main
git pull origin main
```

**With default port (22):**

```bash
git clone git@git.example.com:username/repo-name.git
```

### Simplify with ~/.ssh/config

Create `~/.ssh/config` to avoid typing the port every time:

```
Host forgejo
    HostName git.example.com
    Port 2222
    User git
    IdentityFile ~/.ssh/id_ed25519
```

Then clone with a simple alias:

```bash
git clone forgejo:username/repo-name.git
```

**For Windows users (if applicable):** Same `~/.ssh/config` format works with Windows OpenSSH client at `%USERPROFILE%\.ssh\config`.

### Verify SSH Connection

```bash
# Test connection to Forgejo
ssh -T -p 2222 git@git.example.com

# Expected output (if using ssh config alias):
ssh -T forgejo
# → "Hi there, username! You've successfully authenticated..."
```

### Common SSH Issues

**Permission denied (publickey):**
```bash
# Make sure your key is added to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Verify the key is registered in Forgejo UI
# Profile → Settings → SSH / GPG Keys
```

**Port 22 already in use on host:**
```bash
# Check what's using port 22
sudo lsof -i :22
# Usually the host's SSH server. Move it to a different port instead:
# /etc/ssh/sshd_config → change Port to 2222, then restart sshd
# This frees up host port 22 for Forgejo

# OR just use the custom port approach (2222 → 22) as shown above
```

**Clone URL shows wrong port in UI:**
Make sure `.env` has:
```ini
FORGEJO_SSH_PORT=2222       # Must match the HOST port
FORGEJO_SSH_DOMAIN=git.example.com
FORGEJO_ROOT_URL=https://git.example.com
```

Then restart Forgejo:
```bash
docker compose up -d forgejo
```

## Object Storage (S3-Compatible)

Forgejo supports S3-compatible object storage for separating file storage from the main data volume. You can configure each storage type independently.

### Which Data Can Use Object Storage?

| Storage Type | Env Var Prefix | What It Stores | Default |
|-------------|---------------|----------------|---------|
| `attachments` | `FORGEJO__attachment__` | Issue/PR file attachments | Local |
| `avatars` | `FORGEJO__avatar__` | User & org avatars | Local |
| `repo-avatars` | `FORGEJO__picture__` | Repository avatars | Local |
| `lfs` | `FORGEJO__lfs__` | Git LFS objects | Local |
| `actions-artifacts` | `FORGEJO__actions__` | CI/CD job artifacts | Local |
| `packages` | `FORGEJO__packages__` | Package registry (npm, Docker, etc.) | Local |

### Generic S3 Pattern

All S3-compatible providers use the same config pattern with `STORAGE_TYPE: minio` (Forgejo uses "minio" as the generic S3 label):

```yaml
FORGEJO__{type}__STORAGE_TYPE: minio
FORGEJO__{type}__MINIO_ENDPOINT: s3.amazonaws.com
FORGEJO__{type}__MINIO_ACCESS_KEY_ID: ${S3_ACCESS_KEY}
FORGEJO__{type}__MINIO_SECRET_ACCESS_KEY: ${S3_SECRET_KEY}
FORGEJO__{type}__MINIO_BUCKET: forgejo-{type}
FORGEJO__{type}__MINIO_LOCATION: auto
FORGEJO__{type}__MINIO_USE_SSL: true
# Optional: custom path style (required for some providers)
FORGEJO__{type}__MINIO_PATH_STYLE: true   # Garages, MinIO
```

### Provider Examples

#### ☁️ AWS S3

Best for: production, global accessibility, existing AWS setup.

```yaml
forgejo:
  environment:
    # Actions Artifacts
    FORGEJO__actions__ARTIFACT_STORAGE_TYPE: minio
    FORGEJO__actions__MINIO_ENDPOINT: s3.amazonaws.com
    FORGEJO__actions__MINIO_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
    FORGEJO__actions__MINIO_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
    FORGEJO__actions__MINIO_BUCKET: forgejo-actions
    FORGEJO__actions__MINIO_LOCATION: ap-southeast-1
    FORGEJO__actions__MINIO_USE_SSL: true

    # Git LFS
    FORGEJO__lfs__STORAGE_TYPE: minio
    FORGEJO__lfs__MINIO_ENDPOINT: s3.amazonaws.com
    FORGEJO__lfs__MINIO_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
    FORGEJO__lfs__MINIO_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
    FORGEJO__lfs__MINIO_BUCKET: forgejo-lfs
    FORGEJO__lfs__MINIO_LOCATION: ap-southeast-1
    FORGEJO__lfs__MINIO_USE_SSL: true
```

Create S3 buckets first:
```bash
aws s3 mb s3://forgejo-actions --region ap-southeast-1
aws s3 mb s3://forgejo-lfs --region ap-southeast-1
```

Pricing: ~$0.023/GB/month (S3 Standard) + $0.005/1k PUT + egress fees.

#### ☁️ Cloudflare R2

Best for: zero egress fees, global edge, low cost.

```yaml
forgejo:
  environment:
    FORGEJO__actions__ARTIFACT_STORAGE_TYPE: minio
    FORGEJO__actions__MINIO_ENDPOINT: ${R2_ACCOUNT_ID}.r2.cloudflarestorage.com
    FORGEJO__actions__MINIO_ACCESS_KEY_ID: ${R2_ACCESS_KEY_ID}
    FORGEJO__actions__MINIO_SECRET_ACCESS_KEY: ${R2_SECRET_ACCESS_KEY}
    FORGEJO__actions__MINIO_BUCKET: forgejo-actions
    FORGEJO__actions__MINIO_LOCATION: auto
    FORGEJO__actions__MINIO_USE_SSL: true

    FORGEJO__lfs__STORAGE_TYPE: minio
    FORGEJO__lfs__MINIO_ENDPOINT: ${R2_ACCOUNT_ID}.r2.cloudflarestorage.com
    FORGEJO__lfs__MINIO_ACCESS_KEY_ID: ${R2_ACCESS_KEY_ID}
    FORGEJO__lfs__MINIO_SECRET_ACCESS_KEY: ${R2_SECRET_ACCESS_KEY}
    FORGEJO__lfs__MINIO_BUCKET: forgejo-lfs
    FORGEJO__lfs__MINIO_LOCATION: auto
    FORGEJO__lfs__MINIO_USE_SSL: true
```

**Setup:**
1. Go to Cloudflare Dashboard → R2 → Create bucket (`forgejo-actions`, `forgejo-lfs`)
2. Go to **Manage R2 API Tokens** → Create API token with `Object Read & Write` permission
3. Copy `Access Key ID` and `Secret Access Key` to `.env`
4. Account ID is found in R2 dashboard URL or Workers & Pages → right sidebar

```ini
# .env
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
```

**Why R2 for personal use:** Zero egress fees — clone/push/pull traffic is free. 10GB storage free tier. No data transfer cost when developers pull from different locations.

#### ☁️ Google Cloud Storage (GCS)

GCS supports S3-compatible HMAC keys via the XML API.

```yaml
forgejo:
  environment:
    FORGEJO__actions__ARTIFACT_STORAGE_TYPE: minio
    FORGEJO__actions__MINIO_ENDPOINT: storage.googleapis.com
    FORGEJO__actions__MINIO_ACCESS_KEY_ID: ${GCS_HMAC_ACCESS_KEY}
    FORGEJO__actions__MINIO_SECRET_ACCESS_KEY: ${GCS_HMAC_SECRET_KEY}
    FORGEJO__actions__MINIO_BUCKET: forgejo-actions
    FORGEJO__actions__MINIO_LOCATION: auto
    FORGEJO__actions__MINIO_USE_SSL: true
```

**Setup:**
1. Go to GCP Console → Cloud Storage → Create bucket (must be globally unique name)
2. Go to **Settings** → **Interoperability** → **Create HMAC key** for your service account
3. The HMAC key gives you an Access Key + Secret compatible with S3

**Pricing:** ~$0.020/GB/month, $0.005/1k operations, but egress is expensive ($0.12/GB). Best if most access is from GCP.

#### 🏠 Garage (Self-Hosted S3)

[Garage](https://garagehq.deuxfleurs.fr/) is an open-source, lightweight S3-compatible object store designed for geo-distributed deployments. Much lighter than MinIO (~30MB RAM vs MinIO's ~100-200MB).

```yaml
  garage:
    image: dxflrs/garage:latest
    container_name: forgejo-garage
    environment:
      GARAGE_ADMIN_TOKEN: ${GARAGE_ADMIN_TOKEN}
      GARAGE_METRICS_TOKEN: ${GARAGE_METRICS_TOKEN}
      GARAGE_RPC_SECRET: ${GARAGE_RPC_SECRET}
    volumes:
      - garage_data:/data
    ports:
      - "${GARAGE_S3_PORT:-3900}:3900"   # S3-compatible API
      - "3901:3901"                       # Admin API
    restart: unless-stopped

  forgejo:
    environment:
      FORGEJO__actions__ARTIFACT_STORAGE_TYPE: minio
      FORGEJO__actions__MINIO_ENDPOINT: garage:3900
      FORGEJO__actions__MINIO_ACCESS_KEY_ID: ${GARAGE_ACCESS_KEY_ID}
      FORGEJO__actions__MINIO_SECRET_ACCESS_KEY: ${GARAGE_SECRET_ACCESS_KEY}
      FORGEJO__actions__MINIO_BUCKET: forgejo-actions
      FORGEJO__actions__MINIO_LOCATION: auto
      FORGEJO__actions__MINIO_USE_SSL: false
      FORGEJO__actions__MINIO_PATH_STYLE: true    # Required for Garage & MinIO
```

**Garage setup after first deploy:**
```bash
# Configure Garage (one-time)
docker exec forgejo-garage garage layout assign -z dc1 -c 1 $(docker exec forgejo-garage garage node id)
docker exec forgejo-garage garage layout apply

# Create bucket and access keys
docker exec forgejo-garage garage bucket create forgejo-actions
docker exec forgejo-garage garage bucket create forgejo-lfs
docker exec forgejo-garage garage key create forgejo-user
docker exec forgejo-garage garage bucket allow forgejo-actions --key forgejo-user --read --write --owner
docker exec forgejo-garage garage bucket allow forgejo-lfs --key forgejo-user --read --write --owner

# Get access key & secret
docker exec forgejo-garage garage key info forgejo-user
```

**Why Garage over MinIO on a MiniPC:**
- ~30MB RAM vs MinIO's ~100-200MB
- Designed for edge/small deployments
- Built-in geo-replication if you ever add more nodes
- Simpler resource footprint

### Recommendation for MiniPC (4c/8GB/512GB)

| Approach | RAM Usage | Complexity | Best For |
|----------|-----------|------------|----------|
| **Local storage** (default) | 0MB extra | None | Starting out, single user |
| **Garage** (self-hosted) | ~30MB | Medium | Lightweight S3, low RAM |
| **Cloudflare R2** | 0MB extra | Low | Zero egress, free tier |
| **AWS S3** | 0MB extra | Low | Production, team access |
| **MinIO** (self-hosted) | ~100-200MB | Medium | Feature-rich S3 |
| **GCS** | 0MB extra | Low | If already on GCP |

**Gw recommend:** Mulai dengan **local** dulu. Kalo butuh object storage, pilih:

1. **Cloudflare R2** — kalo lo pengen storage di cloud tanpa biaya egress dan free tier 10GB. Cocok buat LFS kalo lo sering push binary/assets.
2. **Garage** — kalo lo pengen self-hosted tapi RAM miniPC-nya terbatas. Jauh lebih ringan dari MinIO.
3. **Jangan MinIO** di MiniPC — kebanyakan makan RAM buat single-user setup.

### Migrating Existing Data

If you switch from local to object storage mid-way, local files **don't auto-migrate**. Forgejo will start writing new data to S3 but old data stays local. To migrate:

```bash
# Stop Forgejo
docker compose stop forgejo

# Copy local attachments to S3 (example)
docker run --rm -v forgejo_data:/data amazon/aws-cli s3 sync \
  /data/forgejo/attachments/ s3://forgejo-attachments/

# Or for Garage:
docker run --rm -v forgejo_data:/data \
  -e AWS_ACCESS_KEY_ID=... -e AWS_SECRET_ACCESS_KEY=... \
  amazon/aws-cli --endpoint-url http://garage:3900 s3 sync \
  /data/forgejo/attachments/ s3://forgejo-attachments/

# Restart Forgejo
docker compose up -d forgejo
```

## Troubleshooting

**Runner can't connect to Forgejo:**
```bash
# Check runner logs
docker compose logs runner
# If "cannot register new runner" — you're using the wrong image (should be data.forgejo.org/forgejo/runner:12)
# If it can't reach forgejo — check docker-in-docker: docker compose logs docker-in-docker
```

**Runner registered but shows offline:**
```bash
docker compose restart runner
```

**Token error (invalid_argument):**
Forgejo 15.x does NOT use `GITEA_RUNNER_REGISTRATION_TOKEN` env var. You must:
- Create runner in UI → get UUID + Token
- Put them in `runner-config.yml` under `server.connections.forgejo`
- See [Forgejo Runner Registration docs](https://forgejo.org/docs/latest/admin/actions/registration/)

**Workflow triggered but jobs don't start:**
```bash
docker compose logs runner
# Usually: config file missing UUID/Token, or runner can't reach dind
# Check DOCKER_HOST env var in runner container
docker exec forgejo-runner env | grep DOCKER
```

**Want to use GitHub Marketplace actions?**  
Works out of the box — e.g. `actions/checkout@v4`, `actions/setup-node@v4`.

## Related

- [dokploy-basic-auth](dokploy-basic-auth.md) — Adding basic auth to Compose apps on Dokploy
- [zot-registry](zot-registry.md) — Self-hosted OCI registry with RBAC
