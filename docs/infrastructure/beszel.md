---
title: Beszel — Lightweight Server Monitoring
description: - [What is Beszel?](#what-is-beszel)
---

# Beszel — Lightweight Server Monitoring

> Beszel is a lightweight server monitoring platform with historical data, Docker stats, alerts, and OAuth/OIDC support. Built on PocketBase. Agent binary ~15MB, hub ~30MB RAM idle.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Beszel Hub     │     │  Beszel Agent   │
│  (PocketBase)   │◄────│  (per server)   │
│  :8090          │     │  :45876         │
│  Web UI + API   │     │  │              │
└────────┬────────┘     │  ├── Docker     │
         │              │  ├── CPU/Mem    │
    ┌────▼────┐         │  ├── Disk       │
    │  Dex    │         │  └── Network    │
    │ (OIDC)  │         └─────────────────┘
    └─────────┘
```

- **Hub** — Web UI (PocketBase-based), stores metrics, manages users
- **Agent** — Runs on each monitored server, collects & pushes metrics via WebSocket or SSH

## Docker Compose Setup

### Hub

```yaml
services:
  beszel:
    image: henrygd/beszel:latest
    container_name: beszel-hub
    restart: unless-stopped
    ports:
      - "8090:8090"
    volumes:
      - beszel-data:/beszel/data
    environment:
      - TZ=Asia/Jakarta
      # Optional: OIDC / OAuth
      - USER_CREATION=true
      # - DISABLE_PASSWORD_AUTH=true   # OIDC-only

volumes:
  beszel-data:
```

### Hub + Local Agent (combined)

```yaml
services:
  beszel:
    image: henrygd/beszel:latest
    container_name: beszel-hub
    restart: unless-stopped
    ports:
      - "8090:8090"
    volumes:
      - beszel-data:/beszel/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - TZ=Asia/Jakarta

volumes:
  beszel-data:
```

### Traefik Labels (for Dokploy)

```yaml
services:
  beszel:
    # ... container config ...
    expose:
      - "8090"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.beszel.rule=Host(`beszel.dtakah.com`)"
      - "traefik.http.routers.beszel.entrypoints=websecure"
      - "traefik.http.routers.beszel.tls.certresolver=letsencrypt"
      - "traefik.http.services.beszel.loadbalancer.server.port=8090"
```

## Agent Setup

### Docker (recommended for containerized servers)

```yaml
services:
  beszel-agent:
    image: henrygd/beszel-agent:latest
    container_name: beszel-agent
    restart: unless-stopped
    ports:
      - "45876:45876"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
    environment:
      - KEY=<public-key-from-hub>
      - PORT=45876
```

The key is generated in the hub UI when adding a new system.

### Binary (for non-Docker servers)

```bash
# Download
curl -sL https://github.com/henrygd/beszel/releases/latest/download/beszel-agent_Linux_x86_64.tar.gz | tar xz

# Run
KEY=<key> ./beszel-agent
```

## Hub Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_URL` | unset | Hub URL, needed for subpath serving |
| `AUTO_LOGIN` | unset | Email to auto-login (bypasses auth) |
| `DISABLE_PASSWORD_AUTH` | false | Disable password login (OIDC-only mode) |
| `USER_CREATION` | false | Auto-create users on first OIDC login |
| `MFA_OTP` | false | Enable email OTP for MFA |
| `SHARE_ALL_SYSTEMS` | false | All users see all systems |
| `TRUSTED_AUTH_HEADER` | unset | Header for forward auth (e.g. Cloudflare Access) |

## OIDC Authentication

Beszel uses **PocketBase** as its backend. OIDC is configured via the PocketBase admin UI at `/_/`.

### Setup Steps

1. Start the hub and create admin account
2. Visit `https://beszel.example.com/_/` (PocketBase admin)
3. **Settings** → toggle **OFF** "Hide collection create and edit controls"
4. **Collections** → **users** → **Options** tab
5. Under **OAuth2**:
   - Enable OAuth2 ✅
   - **Provider:** `oidc`
   - **Client ID:** `beszel`
   - **Client Secret:** `beszel-client-secret-change-me`
   - **Issuer URL:** `https://auth.dtakah.com` (Dex URL)
6. Save collection
7. Toggle "Hide collection create and edit controls" back **ON**
8. Set env vars:
   ```
   USER_CREATION=true
   DISABLE_PASSWORD_AUTH=true   # optional, for OIDC-only
   ```

### Redirect URI

When registering the OAuth2 app in Dex, use:
```
https://beszel.example.com/api/oauth2-redirect
```

### Supported Providers

**External:** Apple, GitHub, GitLab, Google, Discord, Microsoft, Notion, ZITADEL, and 20+ more.

**Self-hosted / OIDC:** Authelia, Authentik, Gitea, GitLab, Kanidm, Keycloak, **Dex**, Pocket ID, ZITADEL.

## Alerts

Beszel supports configurable alerts for:

- CPU usage (percentage or temperature)
- Memory usage
- Disk usage (percentage)
- Network bandwidth (throughput)
- Load average
- System status (online/offline)

**Notification channels:** Email, Webhook, Discord, Slack, Telegram, Gotify, Ntfy, and more.

## API

Beszel exposes a REST API (via PocketBase). Authentication via PocketBase auth tokens.

```bash
# List systems
curl -H "Authorization: Bearer <token>" https://beszel.example.com/api/collections/systems/records

# Get system metrics
curl -H "Authorization: Bearer <token>" https://beszel.example.com/api/collections/systems/records/<system-id>
```

## Backup

Beszel stores data in `/beszel/data` (SQLite database). To backup:

```bash
# Stop hub, copy data dir
docker compose stop beszel
tar czf beszel-backup-$(date +%Y%m%d).tar.gz ./beszel/data/
docker compose start beszel
```

Or use the built-in backup feature: **Settings → Backups** in the hub UI (supports disk and S3-compatible storage).

## Key Details

| Aspect | Notes |
|--------|-------|
| Storage | SQLite (PocketBase) — single file, easy backup |
| Docker socket | Read-only mount for container stats |
| Agent protocol | WebSocket (default) or SSH |
| Multi-user | Built-in; admins control system visibility |
| OIDC auto-provision | Enable `USER_CREATION=true` |

## Related

- [Dex OIDC](./dex-oidc.md) — Central OIDC identity provider
- [Zot Registry](./zot-registry.md) — Container registry
- [Forgejo CI/CD](./forgejo-cicd-docker-compose.md) — Git + CI/CD
