# Zot Registry

> Lightweight (~20MB binary, ~50MB RAM idle), OCI-compliant container registry in Go. A production-ready alternative to Docker Distribution and Harbor for resource-constrained environments.

## Why Zot?

| Aspect | Zot | Docker Distribution | Harbor |
|--------|:---:|:-------------------:|:------:|
| RAM usage | ~50MB | ~30MB | ~2-4GB |
| OCI Artifact | ✅ Yes | ⚠️ Partial | ✅ Yes |
| RBAC | ✅ Yes | ❌ No | ✅ Yes (proper) |
| GC | Auto | Manual | Auto |
| Built-in UI | ✅ Yes | ❌ No | ✅ Yes |
| OIDC | ✅ Yes | ❌ No | ✅ Yes |
| Cosign/Notation | ✅ Built-in | ❌ No | ⚠️ Extension |
| CVE scanning | ✅ Trivy | ❌ No | ✅ Trivy |

**Choose Zot when:** resource-constrained VPS, <10GB storage, need OCI artifacts + RBAC but Harbor is too heavy.

---

## Deploy with Docker Compose

### Basic compose + local storage:

```yaml
services:
  zot:
    image: ghcr.io/project-zot/zot-linux-amd64:latest
    container_name: zot-registry
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./zot-config.json:/etc/zot/config.json:ro
      - ./htpasswd:/etc/zot/htpasswd:ro
      - zot-data:/var/lib/zot
    environment:
      - TZ=Asia/Jakarta
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:5000/v2/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  zot-data:
```

---

## Cloudflare R2 Storage

Zot supports S3-compatible storage — Cloudflare R2 works perfectly with **no egress fees**.

```json
{
  "distSpecVersion": "1.1.0",
  "storage": {
    "storageDriver": {
      "name": "s3",
      "rootDirectory": "/zot",
      "region": "auto",
      "bucket": "YOUR_R2_BUCKET",
      "endpoint": "https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com",
      "accessKey": "YOUR_R2_ACCESS_KEY",
      "secretKey": "YOUR_R2_SECRET_KEY",
      "secure": true,
      "skipVerify": false
    },
    "gc": true,
    "dedupe": true,
    "commit": true
  },
  "http": {
    "address": "0.0.0.0",
    "port": "5000"
  },
  "log": {
    "level": "debug"
  },
  "extensions": {
    "search": {
      "cve": {
        "updateInterval": "2h"
      }
    },
    "ui": {
      "enable": true
    }
  }
}
```

**⚠️ R2 notes:**
- `region` **must** be `"auto"` — AWS region strings (e.g. `us-east-1`) will fail
- Bucket must be created in Cloudflare R2 dashboard first
- No egress fee — cheap for registry

---

## Auth Options

### 1. htpasswd (for docker CLI)

```json
"http": {
  "auth": {
    "htpasswd": {
      "path": "/etc/zot/htpasswd"
    }
  }
}
```

Generate:
```bash
htpasswd -nbB admin securepass > htpasswd
htpasswd -nbB robot-ci token123 >> htpasswd
```

### 2. OIDC (for web browser SSO)

```json
"http": {
  "auth": {
    "oidc": {
      "provider": {
        "name": "authentik",
        "issuer": "https://auth.domain.com/application/o/zot-registry/"
      },
      "clientid": "xxx",
      "clientsecret": "xxx"
    }
  }
}
```

### 3. Dual auth (recommended — htpasswd for CLI + OIDC for web)

```json
"http": {
  "auth": {
    "htpasswd": { "path": "/etc/zot/htpasswd" },
    "oidc": { ... }
  }
}
```

### 4. Traefik Basic Auth (for Dokploy Compose)

Zot runs with no auth, Traefik handles authentication via labels:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.zot.rule=Host(`registry.domain.com`)"
  - "traefik.http.routers.zot.entrypoints=websecure"
  - "traefik.http.routers.zot.tls.certresolver=letsencrypt"
  - "traefik.http.routers.zot.service=zot"
  - "traefik.http.routers.zot.middlewares=zot-auth"
  - "traefik.http.services.zot.loadbalancer.server.port=5000"
  - "traefik.http.middlewares.zot-auth.basicauth.users=admin:$$2y$$05$$HASH..."
```

**⚠️ CRITICAL:** In docker-compose.yml, every `$` in bcrypt hash must be doubled to `$$` (Docker Compose variable interpolation).

---

## Access Control (RBAC)

Zot has proper per-repo authorization via `http.accessControl`.

### Actions

| Action | Meaning |
|--------|---------|
| `read` | Pull image, list tags, inspect manifest |
| `create` | Push new image / new tag |
| `update` | Overwrite existing tag |
| `delete` | Delete image/tag |

### Permission levels

| Level | Scope |
|-------|-------|
| **adminPolicy** | Full access to ALL repos |
| **policies[]** | Per-user/group + per-repo + specific actions |
| **defaultPolicy** | Default for authenticated users without specific policy |
| **anonymousPolicy** | For unauthenticated (public) access |

### Glob patterns for repos

| Pattern | Matches |
|---------|---------|
| `**` | All repos |
| `infra/**` | Everything under `infra/` (recursive) |
| `infra/*` | Single level under `infra/` |
| `nginx` | Exact repo name |

### Example config

```json
{
  "http": {
    "auth": {
      "htpasswd": { "path": "/etc/zot/htpasswd" }
    },
    "accessControl": {
      "groups": {
        "developers": { "users": ["alice", "bob"] },
        "ops":       { "users": ["charlie"] }
      },
      "repositories": {
        "**": {
          "defaultPolicy": ["read"],
          "policies": [
            {
              "groups": ["developers"],
              "actions": ["read", "create", "update"]
            }
          ]
        },
        "infra/**": {
          "policies": [
            {
              "groups": ["ops"],
              "actions": ["read", "create", "update", "delete"]
            }
          ],
          "defaultPolicy": ["read"]
        },
        "prod/**": {
          "policies": [
            {
              "users": ["charlie"],
              "actions": ["read", "create", "update"],
              "conditions": [
                {
                  "expression": "req.time < timestamp(\"2099-12-31T23:59:59Z\")",
                  "message": "Access expired"
                }
              ]
            }
          ]
        }
      },
      "adminPolicy": {
        "users": ["admin"],
        "actions": ["read", "create", "update", "delete"]
      }
    }
  }
}
```

### Anonymous access (public pull)

```json
"repositories": {
  "public/**": {
    "anonymousPolicy": ["read"]
  }
}
```

### Conditional policies (CEL)

Zot uses CEL (Common Expression Language) for dynamic conditions:

```json
{
  "users": ["alice"],
  "actions": ["create", "update"],
  "conditions": [
    {
      "expression": "req.referenceType == \"digest\"",
      "message": "Must use digest reference, not mutable tags"
    }
  ]
}
```

Available `req` fields:
| Field | Type | Example |
|-------|------|---------|
| `req.time` | timestamp | `timestamp("2026-12-31T23:59:59Z")` |
| `req.method` | string | `"GET"`, `"PUT"`, `"DELETE"` |
| `req.referenceType` | string | `"tag"` or `"digest"` |
| `req.auth.admin` | bool | Admin or not |
| `req.client.ip` | string | Client IP address |
| `req.tls.enabled` | bool | TLS or not |

---

## Artifact Support

Zot is **OCI-native** — based on OCI Image Spec v1.1.0 + OCI Distribution Spec. This means it supports **any** OCI artifact, not just container images.

### Artifact types supported

| Type | How to push |
|------|-------------|
| **Container images** (Docker/OCI) | `docker push`, `podman push` |
| **Helm charts** | `helm push chart.tgz oci://registry.domain.com/repo` |
| **WASM modules** | `wasm-to-oci push` |
| **SBOM** (CycloneDX, SPDX) | ORAS CLI |
| **Cosign signatures** | `cosign sign` (pushes signature as artifact) |
| **Notation signatures** | `notation sign` |
| **Attestations** (SLSA, intoto) | `cosign attest` |
| **Generic files** | `oras push oci://registry.domain.com/repo file.txt` |
| **Any OCI artifact** | ORAS CLI: `oras push` |

### Referrers API

Zot implements the OCI Referrers API — artifacts (SBOMs, signatures, attestations) linked to their parent image are automatically discoverable. No extra config needed.

---

## Extensions

| Extension | Config | What it does |
|-----------|--------|-------------|
| **search** | `extensions.search.cve` | Image search + CVE scanning (Trivy) |
| **ui** | `extensions.ui` | Web UI for browsing |
| **sync** | `extensions.sync` | Mirror/sync from other registries |
| **trust** | `extensions.trust` | Cosign + Notation signature verification |
| **scrub** | `extensions.scrub` | Periodic data integrity check |
| **metrics** | `extensions.metrics` | Prometheus metrics endpoint |
| **lint** | `extensions.lint` | Image linting |
| **events** | `extensions.events` | Event notifications |
| **mgmt** | `extensions.mgmt` | Management API |

**⚠️ UI v2.1.x quirk:** Enabling UI requires `extensions.search.cve` block too, or Zot fails with `"failed to enable ui, search extension must be enabled"`.

---

## Dokploy Compose Deployment

In Dokploy Compose type:

1. **Files tab** → create `docker-compose.yml` + `zot-config.json` + `htpasswd` (optional)
2. Files are in the same directory, so use relative paths in volumes: `./zot-config.json:/etc/zot/config.json:ro`
3. Use `expose` instead of `ports` for services behind Traefik
4. **Domains tab** → add domain → Service: `zot`, Port: `5000`

### Full inline Traefik auth for Compose (alternative to Zot auth)

Since Dokploy's Middlewares field in Domains UI doesn't apply to Compose services:

```yaml
services:
  zot:
    image: ghcr.io/project-zot/zot-linux-amd64:latest
    container_name: zot-registry
    restart: unless-stopped
    expose:
      - "5000"
    volumes:
      - ./zot-config-noauth.json:/etc/zot/config.json:ro
      - zot-data:/var/lib/zot
    environment:
      - TZ=Asia/Jakarta
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.zot.rule=Host(`registry.domain.com`)"
      - "traefik.http.routers.zot.entrypoints=websecure"
      - "traefik.http.routers.zot.tls.certresolver=letsencrypt"
      - "traefik.http.routers.zot.service=zot"
      - "traefik.http.routers.zot.middlewares=zot-auth"
      - "traefik.http.services.zot.loadbalancer.server.port=5000"
      - "traefik.http.middlewares.zot-auth.basicauth.users=admin:$$2y$$05$$HASH..."
```

**⚠️ Remember:** All `$` in bcrypt hash → `$$` in docker-compose labels.

---

## Pitfalls

- **Port exposure:** `127.0.0.1:5000:5000` = localhost only (safe for proxy pattern). `5000:5000` = public (dangerous without auth)
- **UI needs search + CVE:** Zot v2.1.x requires `extensions.search.cve` for UI to work
- **Search extension has no `enable` flag:** Unlike `ui`, search is enabled implicitly by the `cve` sub-block
- **UI uses absolute paths:** If proxied under a sub-path, static assets (JS/CSS) may break. Use subdomain instead
- **No fine-grained RBAC per namespace:** Zot has per-repo policies but no project-level namespace isolation like Harbor
- **R2 region:** Must be `"auto"` — AWS region strings will fail
