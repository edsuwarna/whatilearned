---
title: Warpgate — Smart SSH, HTTPS & Database Bastion Host
description: - [Overview](#overview) - [How It Works](#how-it-works) - [vs Jump Host / VPN / Teleport](#how-is-warpgate-different) - [Installation](#installation) - [Quick Start](#quick-start) - [SSH Proxy](#ssh-proxy) - [Database Proxy](#database-proxy) - [HTTPS Proxy](#https-proxy) - [Kubernetes Proxy](#kubernetes-proxy) - [Admin UI](#admin-ui) - [Authentication](#authentication) - [Use Cases](#use-cases) - [Docker](#docker) - [Comparison](#comparison)
---

# Warpgate — Smart SSH, HTTPS & Database Bastion Host

> **Last updated:** 2026-07-04
> **Version:** v0.26.0
> **Repo:** [warp-tech/warpgate](https://github.com/warp-tech/warpgate) ⭐ 7.3k
> **Language:** Rust (100% safe) — single binary
> **License:** Apache 2.0
> **Docs:** https://warpgate.null.page

**Warpgate** is a smart & fully transparent SSH, HTTPS, Kubernetes, MySQL, and PostgreSQL bastion host that doesn't require a client app or an SSH wrapper. It replaces traditional jump hosts with a secure, auditable, and user-friendly access gateway.

## Table of Contents

- [Overview](#overview)
  - [Is This a Tunnel Tool?](#is-this-a-tunnel-tool)
  - [Key Features](#key-features)
- [How Is Warpgate Different](#how-is-warpgate-different)
- [How It Works](#how-it-works)
- [Installation](#installation)
  - [Quick Install](#quick-install)
  - [From Source](#from-source)
- [Quick Start](#quick-start)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Run](#run)
- [SSH Proxy](#ssh-proxy)
  - [Standard SSH Access](#standard-ssh-access)
  - [SSH with 2FA](#ssh-with-2fa)
  - [SSH Key Authentication](#ssh-key-authentication)
- [Database Proxy](#database-proxy)
  - [MySQL Proxy](#mysql-proxy)
  - [PostgreSQL Proxy](#postgresql-proxy)
  - [Database Backup Through Warpgate](#database-backup-through-warpgate)
- [HTTPS Proxy](#https-proxy)
- [Kubernetes Proxy](#kubernetes-proxy)
- [Admin UI](#admin-ui)
  - [Session Recording](#session-recording)
  - [Live Session View](#live-session-view)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [2FA (TOTP)](#2fa-totp)
  - [SSO (OpenID Connect)](#sso-openid-connect)
  - [Tickets (Temporary Access)](#tickets-temporary-access)
- [Use Cases](#use-cases)
  - [Infrastructure Access Gateway](#infrastructure-access-gateway)
  - [Database Access with Audit](#database-access-with-audit)
  - [Multi-Team Access Control](#multi-team-access-control)
  - [Compliance & Session Recording](#compliance--session-recording)
- [Docker](#docker)
  - [Docker Compose](#docker-compose)
- [Comparison](#comparison)
  - [Chisel vs frp vs Warpgate](#chisel-vs-frp-vs-warpgate)
  - [Warpgate vs Teleport](#warpgate-vs-teleport)
- [Tips & Pitfalls](#tips--pitfalls)

---

## Overview

Warpgate sits in your DMZ and acts as a **bastion gateway** for all infrastructure access. Instead of giving users direct SSH/DB access to servers, they go through Warpgate which handles authentication, authorization, session recording, and proxying — all transparently.

### Is This a Tunnel Tool?

**No.** Warpgate is not a tunnel tool like Chisel or frp. It's a **bastion / PAM** (Privileged Access Management) system. Instead of creating tunnels, it **replaces direct access** with a managed gateway:

- Chisel/frp: "I need to tunnel port 3306 through a firewall"
- Warpgate: "I need to give developers secure, audited access to production databases"

### Key Features

| Feature | Description |
|---------|-------------|
| **SSH Proxy** | Transparent jump host — standard SSH client, no wrapper |
| **MySQL Proxy** | `mysql -h warpgate -P 33060` → internal MySQL |
| **PostgreSQL Proxy** | `psql -h warpgate -p 54320` → internal PG |
| **HTTPS Proxy** | Web-based target selection with session proxy |
| **K8s Proxy** | Kubernetes API access through bastion |
| **Session Recording** | Full session capture — replay via web UI |
| **Live Session View** | Watch active sessions in real-time |
| **2FA (TOTP)** | Built-in, no external plugins |
| **SSO (OIDC)** | Authentik, Google, GitHub, any OIDC provider |
| **Brute-Force Protection** | IP blocking + user lockout built-in |
| **Temporary Tickets** | Time-limited access without creating users |
| **User Management** | Web UI for managing users, roles, targets |
| **No Client Software** | Uses standard SSH/MySQL/psql/kubectl clients |
| **Single Binary** | Rust — no dependencies, ~15MB |

---

## How Is Warpgate Different

| Warpgate | SSH Jump Host | VPN | Teleport |
|----------|:-------------:|:---:|:--------:|
| ✅ Precise 1:1 user ↔ service assignment | ⚠️ Full network access usually | ⚠️ Full network access usually | ✅ Precise 1:1 assignment |
| ✅ No custom client needed | ❌ Jump host config needed | ✅ No custom client needed | ❌ Custom client required |
| ✅ 2FA out of the box | ⚠️ Needs PAM plugins | ⚠️ Depends on provider | ✅ 2FA out of the box |
| ✅ SSO out of the box | ⚠️ Needs PAM plugins | ⚠️ Depends on provider | ❌ Paid feature |
| ✅ Command-level audit | ⚠️ Connection-level only | ⚠️ No audit on target | ✅ Command-level audit |
| ✅ Full session recording | ❌ No secure recording | ❌ No secure recording | ✅ Full session recording |
| ✅ Non-interactive connects | ⚠️ Depends on client support | ✅ Non-interactive | ❌ Needs client wrapper |
| ✅ Self-hosted, own data | ✅ Self-hosted | ⚠️ Depends on provider | ❌ SaaS |

---

## How It Works

```
User (SSH/MySQL/psql/kubectl)
        │
        ▼
┌─────────────────────────────────┐
│        Warpgate (DMZ)           │
│                                 │
│  ┌─────────┐   ┌─────────────┐  │
│  │ Auth    │   │ Target       │  │
│  │ (2FA/   │──▶│ Router      │  │
│  │  SSO)   │   │             │  │
│  └─────────┘   └──────┬──────┘  │
│                       │         │
│  ┌─────────┐         │         │
│  │ Session │         │         │
│  │ Recorder│◀────────┘         │
│  └─────────┘                   │
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│  Target Server / DB / K8s       │
│  (Private Network)              │
└─────────────────────────────────┘
```

1. User connects to Warpgate using a standard client (SSH, MySQL, psql, kubectl)
2. Warpgate authenticates the user (password + 2FA, SSH key, or SSO)
3. Warpgate looks up which targets the user is allowed to access
4. Connection is proxied to the target transparently
5. Session is optionally recorded for audit

---

## Installation

### Quick Install

Download from [releases](https://github.com/warp-tech/warpgate/releases):

```bash
# Linux amd64
wget https://github.com/warp-tech/warpgate/releases/download/v0.26.0/warpgate-v0.26.0-x86_64-unknown-linux-musl.tar.gz
tar xzf warpgate-v0.26.0-x86_64-unknown-linux-musl.tar.gz
sudo cp warpgate /usr/local/bin/
```

### From Source

Requires Rust + NodeJS + NPM:

```bash
git clone https://github.com/warp-tech/warpgate.git
cd warpgate
cargo install just
just npm install
just npm run build
cargo build --release
# Binary at target/release/warpgate
```

---

## Quick Start

### Setup

```bash
warpgate setup
```

Interactive wizard generates config at `/etc/warpgate/config.yaml` (or `./warpgate.yaml`).

### Configuration

Minimal `warpgate.yaml`:

```yaml
bind:
  ssh:
    port: 2222
  http:
    port: 443
    external_host: warpgate.example.com
database:
  path: /var/lib/warpgate/warpgate.db
targets:
  - name: production-web
    ssh:
      host: 10.0.0.10
      port: 22
  - name: production-db
    mysql:
      host: 10.0.0.20
      port: 3306
  - name: analytics-db
    postgres:
      host: 10.0.0.30
      port: 5432
users:
  - name: admin
    credentials:
      - password: "$2y$05$..."   # bcrypt hash
    roles:
      - admin
```

### Run

```bash
warpgate run
# Or as systemd service
warpgate run --service
```

---

## SSH Proxy

### Standard SSH Access

User connects directly to target without knowing its address:

```bash
# Warpgate resolves the target from the username format
ssh user@target-name@warpgate.example.com -p 2222

# Example: SSH to production-web as user "deploy"
ssh deploy@production-web@warpgate.example.com -p 2222
```

Or via `~/.ssh/config`:

```
Host *.wg
  HostName warpgate.example.com
  Port 2222
  ProxyJump none
```

Then: `ssh deploy@production-web.wg`

### SSH with 2FA

When 2FA is enabled, Warpgate prompts for TOTP code after password:

```bash
ssh deploy@production-web@warpgate.example.com -p 2222
# Password: ********
# TOTP code: 123456
# → connected to production-web as deploy
```

### SSH Key Authentication

Upload public key via admin UI, then:

```bash
ssh -i ~/.ssh/id_ed25519 deploy@production-web@warpgate.example.com -p 2222
```

---

## Database Proxy

### MySQL Proxy

Connect to internal MySQL through Warpgate:

```bash
mysql -h warpgate.example.com -P 33060 \
  -u "user@target-name" -p
# Password: your-warpgate-password
# → connected to internal MySQL
```

Or using `mysql_config_editor`:

```bash
mysql_config_editor set \
  --host=warpgate.example.com --port=33060 \
  --user=analyst@production-db --password
mysql --login-path=warpgate
```

### PostgreSQL Proxy

```bash
psql -h warpgate.example.com -p 54320 \
  -U "analyst@analytics-db" -d mydb
# Password: your-warpgate-password
# → connected to internal PostgreSQL
```

### Database Backup Through Warpgate

Backup internal databases through the bastion — with full audit trail:

```bash
# MySQL — Warpgate records every query
mysqldump -h warpgate.example.com -P 33060 \
  -u "backup@production-db" -p'warpgate-pass' \
  --all-databases | gzip > backup-$(date +%F).sql.gz

# PostgreSQL
PGPASSWORD="warpgate-pass" pg_dump \
  -h warpgate.example.com -p 54320 \
  -U "backup@analytics-db" mydb | gzip > backup-$(date +%F).sql.gz
```

**Advantage over Chisel/frp:** Every query/command is **recorded and replayable**. You can see exactly what the backup script did.

---

## HTTPS Proxy

Users access the HTTPS port in a browser, see a list of assigned targets, click one, and get proxied through:

```bash
# Open https://warpgate.example.com
# Login with credentials + 2FA
# Select target → proxied automatically
```

Supports switching between targets during a session.

---

## Kubernetes Proxy

```bash
# Set kubectl to use Warpgate as proxy
kubectl config set-cluster wg-cluster \
  --server=https://warpgate.example.com:443 \
  --certificate-authority=ca.crt

kubectl config set-credentials wg-user \
  --username="dev@k8s-cluster" \
  --password="warpgate-pass"

kubectl config set-context wg --cluster=wg-cluster --user=wg-user
kubectl config use-context wg

kubectl get pods  # → proxied through Warpgate with audit
```

---

## Admin UI

Accessible at `https://warpgate.example.com` (admin role required):

**Features:**
- User management (create, edit, delete, assign roles)
- Target management (SSH, MySQL, PostgreSQL, HTTPS, Kubernetes)
- Role-based access control (assign users to targets via roles)
- Session list (current active sessions)
- Session recordings (view and replay)
- SSH key management
- 2FA enrollment
- System configuration
- Audit log

### Session Recording

Every SSH session can be recorded as a **cast** file — replayable directly in the browser:

```
Admin UI → Sessions → Click recording → Replay
```

Shows exact commands typed, output, timing — like watching a video of the terminal.

### Live Session View

Admin can watch active sessions in real-time:

```
Admin UI → Active Sessions → Click session → Live View
```

---

## Authentication

### Local Users

Users defined in config or managed via admin UI:

```yaml
users:
  - name: alice
    credentials:
      - password: "$2y$05$bcrypt-hash"
    roles:
      - developer
```

### 2FA (TOTP)

Built-in TOTP (Time-based One-Time Password):

```yaml
users:
  - name: alice
    credentials:
      - password: "$2y$05$..."
      - totp:
          secret: "BASE32SECRET..."
    roles:
      - developer
```

Users scan QR code from admin UI → Google Authenticator/ Authy.

### SSO (OpenID Connect)

Integrate with any OIDC provider (Authentik, Keycloak, Google, GitHub, Azure AD):

```yaml
sso:
  oidc:
    provider_url: https://auth.example.com/application/o/warpgate/
    client_id: "your-client-id"
    client_secret: "your-client-secret"
    scopes:
      - openid
      - profile
      - email
    # Map OIDC claims to Warpgate roles
    role_claim: "groups"
    role_mappings:
      - oidc_value: "warpgate-admin"
        warpgate_role: "admin"
      - oidc_value: "warpgate-dev"
        warpgate_role: "developer"
```

### Tickets (Temporary Access)

Generate time-limited access credentials without creating user accounts:

```yaml
tickets:
  - name: emergency-db-access
    target: production-db
    roles:
      - db-readonly
    expires: 2026-07-05T12:00:00Z
    max_uses: 3
```

Users redeem via CLI or web:

```bash
warpgate ticket redeem emergency-db-access
# Temporary credentials printed
```

---

## Use Cases

### Infrastructure Access Gateway

Replace SSH jump hosts with Warpgate:

```
Before:
  User → SSH jump host → SSH config → Target server
  (No audit, no 2FA, no access control)

After:
  User → ssh user@target@warpgate -p 2222
         ↓
  Warpgate: 2FA/OIDC → Check role → Proxy → Record
```

### Database Access with Audit

Give developers access to production DBs with full query recording:

```yaml
targets:
  - name: prod-db
    mysql:
      host: 10.0.0.50
      port: 3306
      user: readonly
      password: "${MYSQL_READONLY_PASS}"

roles:
  - name: db-analyst
    targets:
      - prod-db
```

Developers connect: `mysql -h warpgate -P 33060 -u "alice@prod-db" -p`
Every query is recorded and replayable.

### Multi-Team Access Control

```yaml
roles:
  - name: devops
    targets:
      - production-web
      - staging-db
      - k8s-cluster
  - name: backend-dev
    targets:
      - staging-web
      - staging-db
  - name: dba
    targets:
      - production-db
```

### Compliance & Session Recording

For SOC2, ISO27001, PCI-DSS compliance:

- Every SSH session recorded and replayable
- Database queries logged
- User access revocable in real-time
- Brute-force protection logs
- Audit trail of admin actions

---

## Docker

```bash
docker run -d --name warpgate \
  --restart unless-stopped \
  -p 2222:2222 \
  -p 443:443 \
  -p 33060:33060 \
  -p 54320:54320 \
  -v warpgate-data:/var/lib/warpgate \
  -v $(pwd)/warpgate.yaml:/etc/warpgate/config.yaml:ro \
  ghcr.io/warp-tech/warpgate:latest
```

### Docker Compose

```yaml
services:
  warpgate:
    image: ghcr.io/warp-tech/warpgate:latest
    container_name: warpgate
    restart: unless-stopped
    ports:
      - "2222:2222"       # SSH bastion
      - "443:443"         # HTTPS admin + proxy
      - "33060:33060"     # MySQL proxy
      - "54320:54320"     # PostgreSQL proxy
    volumes:
      - ./warpgate.yaml:/etc/warpgate/config.yaml:ro
      - warpgate-data:/var/lib/warpgate
    environment:
      - TZ=Asia/Jakarta
      - RUST_LOG=info

volumes:
  warpgate-data:
```

### Kubernetes (Helm)

```bash
helm repo add warpgate https://warp-tech.github.io/warpgate
helm install warpgate warpgate/warpgate
```

---

## Comparison

### Chisel vs frp vs Warpgate

| Aspect | Chisel | frp | Warpgate |
|--------|:------:|:---:|:--------:|
| **Category** | Tunnel | Reverse Proxy | **Bastion / PAM** |
| **Language** | Go | Go | Rust |
| **Stars** | 16.2k | 108k | 7.3k |
| **Binary** | Single | frps + frpc | Single |
| **Primary use** | Tunnel through firewall | Expose ports to public | **Secure access gateway** |
| **SSH proxy** | Via tunnel port | Via tunnel port | ✅ **Transparent bastion** |
| **MySQL proxy** | ❌ (generic TCP) | ❌ (generic TCP) | ✅ **Native MySQL protocol** |
| **PostgreSQL proxy** | ❌ (generic TCP) | ❌ (generic TCP) | ✅ **Native PG protocol** |
| **K8s proxy** | ❌ | ❌ | ✅ |
| **Session recording** | ❌ | ❌ | ✅ |
| **Live session viewing** | ❌ | ❌ | ✅ |
| **2FA** | ❌ | ❌ | ✅ **TOTP built-in** |
| **SSO (OIDC)** | ❌ | ✅ (client auth only) | ✅ **Full SSO** |
| **Web Admin UI** | ❌ | ✅ (dashboard) | ✅ **Full management UI** |
| **Brute-force protection** | ❌ | ❌ | ✅ |
| **Temporary tickets** | ❌ | ❌ | ✅ |
| **User management** | users.json | Config file | **Web UI** |
| **Setup complexity** | Simple (CLI flags) | Simple (config files) | Medium (config + UI setup) |
| **Best for** | Quick tunnels | Port exposing | **Infra access management** |

### Warpgate vs Teleport

| Aspect | Warpgate | Teleport |
|--------|:--------:|:--------:|
| **Pricing** | **Free** (open source) | Paid (SaaS) |
| **Client needed** | No (standard clients) | **Yes** (tsh client) |
| **Self-hosted** | ✅ | SaaS |
| **SSH** | ✅ | ✅ |
| **K8s** | ✅ | ✅ |
| **Database** | MySQL, PostgreSQL | MySQL, PostgreSQL, MongoDB, Redis |
| **Session recording** | ✅ | ✅ |
| **2FA/SSO** | ✅ | ✅ |
| **Setup** | Simple (single binary) | Complex (cluster mode) |
| **Windows support** | ❌ (via SSH) | ✅ RDP support |

---

## Tips & Pitfalls

### ✅ Start with `warpgate setup`

The interactive wizard generates a working config with sensible defaults. Don't write config from scratch.

### ✅ Use environment variables for secrets

```yaml
targets:
  - name: prod-db
    mysql:
      password: "${MYSQL_PASSWORD}"
```

### ✅ Enable 2FA for production

Always require TOTP for users accessing production targets.

### ✅ Use roles for access control

Don't assign targets directly to users — create roles and assign users to roles for easier management.

### ⚠️ Port conflicts

Default ports (2222, 443, 33060, 54320) may conflict with existing services. Change them in config:

```yaml
bind:
  ssh:
    port: 2222
  mysql:
    port: 33060
  postgres:
    port: 54320
```

### ⚠️ SQLite database location

Default: `/var/lib/warpgate/warpgate.db`. Back this up regularly — it contains user config and session recordings.

### ✅ TLS certificate

Use `--tls-letsencrypt` or provide cert via config:

```yaml
tls:
  certificate: /etc/letsencrypt/live/warpgate/fullchain.pem
  private_key: /etc/letsencrypt/live/warpgate/privkey.pem
```

### ❌ Not a replacement for Chisel/frp

Warpgate is for **managed access**, not for tunneling through restrictive firewalls. If you need to:
- Tunnel through a corporate firewall → use **Chisel**
- Expose a local dev server to the internet → use **frp** or **cloudflared**
- Give your team secure, audited access to infrastructure → use **Warpgate**
