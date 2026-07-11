---
title: Dex OIDC — Federated Identity Provider
description: - [What is Dex?](#what-is-dex)
---

# Dex OIDC — Federated Identity Provider

> **Dex** is a CNCF sandbox project that acts as a federated OpenID Connect (OIDC) identity provider. It sits between your apps and your user store (LDAP, GitHub, static users, etc.), providing a single OIDC endpoint for all your self-hosted services.

**Use case:** Centralize authentication for apps like Zot Registry, Forgejo, and Beszel — users log in via Dex instead of each app having its own auth.

## Architecture

```
User Browser
  │
  ├── Zot Registry  ────┐
  ├── Forgejo       ────┤  OIDC (Authorization Code Flow)
  └── Beszel        ────┤
                        ▼
                  ┌──────────┐
                  │   Dex    │  ← federated OIDC provider
                  │  :5556   │
                  └────┬─────┘
                       │
            ┌──────────┼──────────┐
            │          │          │
       ┌────▼───┐ ┌───▼────┐ ┌───▼────┐
       │ Static │ │ GitHub │ │  LDAP   │  ← connectors (backends)
       │ Users  │ │ OAuth  │ │        │
       └────────┘ └────────┘ └────────┘
```

Each app redirects to Dex for login. Dex authenticates against the configured connector, then issues an ID token back to the app.

## Docker Compose Setup

```yaml
services:
  dex:
    image: ghcr.io/dexidp/dex:v2.42.0
    container_name: dtakah-dex
    restart: unless-stopped
    ports:
      - "5556:5556"
    volumes:
      - ./dex/config.yaml:/etc/dex/config.yaml:ro
      - dex-data:/var/dex

volumes:
  dex-data:
```

### Traefik Labels (Dokploy)

```yaml
services:
  dex:
    # ... container config ...
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dtakah-dex.rule=Host(`auth.dtakah.com`)"
      - "traefik.http.routers.dtakah-dex.entrypoints=websecure"
      - "traefik.http.routers.dtakah-dex.tls.certresolver=letsencrypt"
      - "traefik.http.services.dtakah-dex.loadbalancer.server.port=5556"
```

## Configuration

### `dex/config.yaml`

```yaml
issuer: https://auth.dtakah.com

storage:
  type: sqlite3
  config:
    file: /var/dex/dex.db

web:
  http: 0.0.0.0:5556

oauth2:
  skipApprovalScreen: true  # skip "App would like to..." screen

# === CONNECTORS (user store backends) ===
connectors:
  # Option A: Static users (simple, for testing)
  - type: static
    id: static
    name: Static Users
    config:
      users:
        - email: admin@dtakah.com
          hash: "$2a$10$..."  # bcrypt hash
          username: admin
        - email: user@dtakah.com
          hash: "$2a$10$..."
          username: user

  # Option B: LDAP (for production)
  # - type: ldap
  #   id: ldap
  #   name: LDAP
  #   config:
  #     host: ldap.example.com:389
  #     bindDN: cn=admin,dc=example,dc=com
  #     bindPW: password
  #     userSearch:
  #       baseDN: ou=users,dc=example,dc=com
  #       filter: "(uid=%s)"
  #       username: uid
  #       idAttr: uid
  #       emailAttr: mail
  #       nameAttr: displayName

# === OAuth2 CLIENTS (apps allowed to use Dex) ===
staticClients:
  - id: zot
    name: Zot Registry
    secret: zot-client-secret-change-me
    redirectURIs:
      - "https://registry.dtakah.com/auth/callback/oidc"

  - id: forgejo
    name: Forgejo
    secret: forgejo-client-secret-change-me
    redirectURIs:
      - "https://git.dtakah.com/user/oauth2/dex/callback"

  - id: beszel
    name: Beszel
    secret: beszel-client-secret-change-me
    redirectURIs:
      - "https://beszel.dtakah.com/api/oauth2-redirect"
```

### Generate bcrypt Password

```bash
# Using Dex itself
docker run --rm ghcr.io/dexidp/dex:v2.42.0 dex hash-password password

# Or using htpasswd
htpasswd -bnBC 10 "" password | tr -d ':\n'
```

## App Integration

### Zot Registry

See full Zot OIDC config in [zot-registry.md](./zot-registry.md#5-dex-oidc).

Key points:
- Dex OIDC works via `http.auth.openid.providers` in Zot config
- OIDC is **browser-only** — for `docker login`, users must generate API keys from the Zot UI after logging in
- Credentials JSON file must be mounted with client ID + secret

### Forgejo

See [forgejo-cicd-docker-compose.md](./forgejo-cicd-docker-compose.md#oauth2-authentication) for setup.

Key points:
- Add Dex as an OAuth2 authentication source via Forgejo Admin UI
- Use OpenID Connect provider type with Dex's discovery URL
- Forgejo auto-generates the callback URL

### Beszel

See [beszel.md](./beszel.md#oidc-authentication).

Key points:
- Beszel uses PocketBase under the hood
- OAuth/OIDC is configured via PocketBase admin UI at `/_/`
- Redirect URI: `https://beszel.example.com/api/oauth2-redirect`
- Enable `USER_CREATION=true` for auto-provisioning

## Verification

1. Open Dex discovery URL: `https://auth.dtakah.com/.well-known/openid-configuration`
   - Should return JSON with `issuer`, `authorization_endpoint`, `token_endpoint`, etc.
2. Test auth flow: open any app → click "Login with Dex" → should redirect to Dex login page
3. After login, should redirect back to the app authenticated

## Related

- [Zot Registry](./zot-registry.md) — OCI container registry with Dex OIDC
- [Forgejo CI/CD](./forgejo-cicd-docker-compose.md) — Git server with Dex OAuth
- [Beszel](./beszel.md) — Server monitoring with Dex OIDC
- [Dex Documentation](https://dexidp.io/docs/) — Official Dex docs
