# Dokploy Basic Auth

> How to add basic authentication (username + password) to applications deployed on Dokploy, for both **Application** and **Compose** types.

## Background

Dokploy v0.29.x has built-in basic auth via **Traefik middleware** — but the UI implementation differs by app type:

| Type | Built-in UI? | How |
|------|:---:|-----|
| **Application** | ✅ Yes | Advanced → Security card |
| **Compose** | ❌ No | Manual via full Traefik labels in docker-compose.yml (UI middleware field doesn't apply) |

---

## Method 1: Application Type (Built-in)

If your app was created as **Application** in Dokploy, use the built-in Security feature.

### Steps

1. Open your app in the Dokploy dashboard
2. Click the **Advanced** tab
3. Scroll down to the **Security** card (title: "Add basic auth to your application")
4. Click **Add Security**
5. Fill in **Username** and **Password** (plain text — Dokploy handles bcrypt hashing automatically)
6. Click **Create**

That's it. The basic auth is active immediately after saving.

---

## Method 2: Compose Type (Manual Traefik Middleware)

If your app was created as **Compose**, there's no Security card in the UI. Use Traefik labels directly.

### Step 1 — Generate bcrypt password hash

Traefik requires bcrypt-hashed passwords for basic auth:

```bash
# Using htpasswd (from apache2-utils)
htpasswd -nbB user123 "your-password" | cut -d: -f2

# Or using Docker
docker run --rm xmartlabs/htpasswd user123 "your-password" 2>/dev/null | cut -d: -f2
```

Output example: `$2y$05$Lk0R7NyV8NQj...`

### Step 2 — Add full Traefik labels to docker-compose.yml

For **Compose** type, the Dokploy UI Middlewares field **does not apply labels to services inside compose**. You must define everything inline in `docker-compose.yml`:

```yaml
services:
  your-app:
    image: your-image
    # ports:                          ← HAPUS jika Traefik handle routing
    #   - "5000:5000"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
      - "traefik.http.routers.app.service=app"
      - "traefik.http.routers.app.middlewares=app-auth"
      - "traefik.http.services.app.loadbalancer.server.port=PORT"
      - "traefik.http.middlewares.app-auth.basicauth.users=user123:$$2y$$05$$Lk0R7NyV8NQj..."
```

⚠️ **Critical:** Every `$` in the bcrypt hash — not just the first one — must be doubled to `$$`. Docker Compose treats `$` as variable interpolation, so `$2y$05$hash...` becomes `$$2y$$05$$hash...`.

Also remove the `ports:` mapping — Traefik routes via the internal Docker network, so direct port exposure isn't needed.

### Step 3 — Set domain in Dokploy

1. Go to your Compose app in the Dokploy dashboard
2. Navigate to the **Domains** tab
3. Add your domain (e.g. `your-domain.com`)
4. Let Dokploy handle the HTTPS certificate automatically via Let's Encrypt
5. **Skip the Middlewares field** — it only works for Application type, not Compose

### Step 4 — Redeploy

Deploy or restart your application for the changes to take effect.

---

## How it works (Compose method)

For **Application** type, Dokploy creates a Traefik file provider config, so you reference middleware via `@file`.

For **Compose** type, all labels **must be on the service itself** in `docker-compose.yml`:

```
docker-compose.yml
  └── label: traefik.enable=true
  └── label: traefik.http.routers.app.rule=Host(...)
  └── label: traefik.http.routers.app.service=app
  └── label: traefik.http.routers.app.middlewares=app-auth  ← apply middleware
  └── label: traefik.http.services.app.loadbalancer.server.port=PORT
  └── label: traefik.http.middlewares.app-auth.basicauth.users=...  ← define middleware
                    │
                    ▼
       Traefik reads all labels from the running container
                    │
                    ▼
       Router + middleware + service all defined inline
                    │
                    ▼
       Basic auth applied on every HTTPS request
```

**Why the UI Middlewares field doesn't work for Compose:** Dokploy's domain middleware field generates a Traefik file provider config snippet, but it only applies to the **outer** Compose project router — individual services inside compose files are invisible to it.

### Provider suffixes explained

| Suffix | Source | Example |
|--------|--------|---------|
| `@docker` | Labels on Docker containers | `app-auth@docker` |
| `@file` | Traefik file provider (YAML) | `app-auth@file` |
| `@kubernetes` | Kubernetes ingress | `app-auth@kubernetes` |

## Alternative: File provider (any type)

If you prefer not to edit `docker-compose.yml`, create a Traefik dynamic config file on the server:

```yaml
# /path/to/traefik/dynamic/auth.yml
http:
  middlewares:
    app-auth:
      basicAuth:
        users:
          - "user123:$2y$05$Lk0R7NyV8NQj..."
```

Then in the domain Middlewares field, reference it as `app-auth@file`.

## Limitations

- For Compose type, all Traefik labels must be inline in `docker-compose.yml` — the UI Middlewares field only works for Application type
- Credentials visible in compose file (hashed, but plaintext readable by anyone with file access)
- Each service needs its own full label set when using the compose method
- `ports:` mapping should be removed from compose when Traefik handles routing
