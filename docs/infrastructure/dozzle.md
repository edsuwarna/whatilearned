---
title: Dozzle — Real-time Docker Log Viewer
description: - [What is Dozzle?](#what-is-dozzle)
---

# Dozzle — Real-time Docker Log Viewer

> Dozzle is a real-time Docker log viewer with a web UI. Lightweight (~7MB binary), no database, no storage — streams logs directly from the Docker API. Supports multi-host via agent mode, container actions, shell access, and forward-proxy authentication for OIDC integration with Dex.

## Architecture

```
User Browser
  │
  ├── Zot Registry  ────┐
  ├── Forgejo       ────┤
  ├── Beszel        ────┤  OIDC (direct with Dex)
  └── Dozzle        ────┤
                        │
                  ┌─────▼──────────┐
                  │  oauth2-proxy  │  ← OIDC client → Dex
                  │    :4180       │
                  └─────┬──────────┘
                        │  Remote-User / Remote-Email headers
                  ┌─────▼──────────┐
                  │     Dozzle     │  ← --auth-provider=forward-proxy
                  │    :8080       │
                  └────────────────┘
```

**Why forward-proxy?** Dozzle does not speak OIDC natively. It reads user identity from HTTP headers set by a reverse proxy. `oauth2-proxy` handles the Dex OIDC flow, then passes `Remote-User`, `Remote-Email`, and `Remote-Name` headers to Dozzle.

## Docker Compose Setup

Create `docker-compose.yml`:

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    container_name: dozzle
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      DOZZLE_AUTH_PROVIDER: forward-proxy
      DOZZLE_AUTH_LOGOUT_URL: https://auth.example.com/dex/logout
      DOZZLE_HOSTNAME: my-server
    networks:
      - dokploy-network

  oauth2-proxy:
    image: quay.io/oauth2-proxy/oauth2-proxy:latest
    container_name: dozzle-oauth2-proxy
    restart: unless-stopped
    ports:
      - "4180:4180"
    environment:
      OAUTH2_PROXY_PROVIDER: oidc
      OAUTH2_PROXY_OIDC_ISSUER_URL: https://auth.example.com/dex
      OAUTH2_PROXY_CLIENT_ID: dozzle
      OAUTH2_PROXY_CLIENT_SECRET: dozzle-client-secret-change-me
      OAUTH2_PROXY_REDIRECT_URL: https://dozzle.example.com/oauth2/callback
      OAUTH2_PROXY_UPSTREAMS: http://dozzle:8080
      OAUTH2_PROXY_EMAIL_DOMAINS: "*"
      OAUTH2_PROXY_COOKIE_SECRET: $(openssl rand -base64 32)
      OAUTH2_PROXY_COOKIE_SECURE: "true"
      OAUTH2_PROXY_SKIP_PROVIDER_BUTTON: "true"
      OAUTH2_PROXY_SET_XAUTHREQUEST: "true"
      OAUTH2_PROXY_PASS_USER_HEADERS: "true"
    depends_on:
      - dozzle
    networks:
      - dokploy-network

networks:
  dokploy-network:
    external: true
```

### Traefik Labels (Dokploy)

Add to the oauth2-proxy service (not Dozzle directly — oauth2-proxy is the entry point):

```yaml
services:
  oauth2-proxy:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dozzle.rule=Host(`dozzle.example.com`)"
      - "traefik.http.routers.dozzle.entrypoints=websecure"
      - "traefik.http.routers.dozzle.tls.certresolver=letsencrypt"
      - "traefik.http.services.dozzle.loadbalancer.server.port=4180"
```

> **Note:** Traefik routes to oauth2-proxy on port 4180, which forwards authenticated requests to Dozzle on port 8080 internally. The router and service are named `dozzle` for clarity.

## Dex Client Configuration

Add this client to your Dex `staticClients` in `dex/config.yaml`:

```yaml
staticClients:
  # ... existing clients (zot, forgejo, beszel) ...
  - id: dozzle
    name: Dozzle
    secret: dozzle-client-secret-change-me
    redirectURIs:
      - "https://dozzle.example.com/oauth2/callback"
```

## How It Works

1. User visits `https://dozzle.example.com`
2. Traefik routes to oauth2-proxy (port 4180)
3. oauth2-proxy detects no session → redirects to Dex login
4. User authenticates with Dex (password, LDAP, etc.)
5. Dex redirects back to oauth2-proxy with auth code
6. oauth2-proxy exchanges code for ID token, creates session
7. oauth2-proxy forwards request to Dozzle with headers:
   - `Remote-User: admin`
   - `Remote-Email: admin@example.com`
   - `Remote-Name: Admin`
8. Dozzle reads headers and creates an authenticated session

## Header Reference

| Header | Claim Source | Description |
|--------|-------------|-------------|
| `Remote-User` | `preferred_username` or `email` | Username in Dozzle UI |
| `Remote-Email` | `email` | Used for Gravatar avatar |
| `Remote-Name` | `name` | Display name |
| `Remote-Roles` | `groups` (optional) | Comma-separated roles |
| `Remote-Filter` | custom (optional) | Comma-separated container filters |

## Logout

Configure logout URL so users can sign out of both Dozzle and Dex:

```yaml
environment:
  DOZZLE_AUTH_LOGOUT_URL: https://auth.example.com/dex/logout
  OAUTH2_PROXY_LOGOUT_URL: https://auth.example.com/dex/logout
```

## Alternative: Simple File-Based Auth (no Dex)

If you don't need SSO with Dex, Dozzle supports a simple file-based provider:

```bash
docker run -d \
  --name dozzle \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ./data:/data \
  -p 8080:8080 \
  amir20/dozzle:latest \
  --auth-provider=simple
```

Generate `users.yml` in the mounted `/data` directory:

```bash
# Generate password hash
docker run --rm amir20/dozzle:latest generate-password mypassword
```

```yaml
# /data/users.yml
users:
  admin:
    password: "$2y$10$..."   # bcrypt hash
    email: admin@example.com
    name: Admin
  user:
    password: "$2y$10$..."
    email: user@example.com
    name: User
```

## Security Notes

- Dozzle has access to `docker.sock` — equivalent to **root on the host**
- Always keep Dozzle behind authentication (forward-proxy or simple)
- Disable [actions](https://dozzle.dev/guide/actions) and [shell access](https://dozzle.dev/guide/shell-access) if not needed:
  ```yaml
  environment:
    DOZZLE_ENABLE_ACTIONS: "false"
    DOZZLE_ENABLE_SHELL: "false"
  ```
- Use [roles](https://dozzle.dev/guide/authentication#roles) and [filters](https://dozzle.dev/guide/authentication#filters) in `users.yml` to restrict container access per user
- Read-only `docker.sock` mount (`:ro`) blocks container create/delete/update but still exposes most of the API

## Related

- [Dex OIDC](./dex-oidc.md) — Central OIDC provider
- [Dozzle Authentication Docs](https://dozzle.dev/guide/authentication) — Official docs
- [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) — Reverse proxy with OIDC support
