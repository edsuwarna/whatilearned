# Dokploy Basic Auth

> How to add basic authentication (username + password) to applications deployed on Dokploy, for both **Application** and **Compose** types.

## Background

Dokploy v0.29.x has built-in basic auth via **Traefik middleware** — but the UI implementation differs by app type:

| Type | Built-in UI? | How |
|------|:---:|-----|
| **Application** | ✅ Yes | Advanced → Security card |
| **Compose** | ❌ No | Manual via Traefik labels + domain middleware field |

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

### Step 2 — Add middleware label to docker-compose.yml

Add a Traefik label to the service you want to protect:

```yaml
services:
  your-app:
    image: your-image
    labels:
      - "traefik.http.middlewares.app-auth.basicauth.users=user123:$$2y$$05$$Lk0R7NyV8NQj..."
```

⚠️ **Important:** Each `$` in the bcrypt hash must be doubled to `$$` in docker-compose YAML, otherwise Docker Compose interprets it as a variable interpolation.

### Step 3 — Reference middleware in domain settings

1. Go to your Compose app in the Dokploy dashboard
2. Navigate to the **Domains** tab
3. Click **Edit** (pencil icon) on the domain you want to protect
4. Scroll down to the **Middlewares** field
5. Add: `app-auth@docker`
6. Click **Add**, then **Save**

### Step 4 — Redeploy

Deploy or restart your application for the changes to take effect.

---

## How it works (Compose method)

```
docker-compose.yml
  └── label: traefik.http.middlewares.app-auth.basicauth.users=...
                    │
                    ▼
       Traefik stores middleware as "app-auth@docker"
                    │
                    ▼
       Domain middleware reference: "app-auth@docker"
                    │
                    ▼
       Router applies basic auth on every request
```

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

- Each domain needs its own middleware reference
- For the Compose method, credentials in the Dokploy dashboard show the raw label value (hashed in Traefik config)
- Each service needs its own middleware label when using the compose method
