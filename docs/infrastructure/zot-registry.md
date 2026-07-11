---
title: Zot Registry
description: - [Why Zot?](#why-zot)
---

# Zot Registry

> Lightweight (~20MB binary, ~50MB RAM idle), OCI-compliant container registry in Go. A production-ready alternative to Docker Distribution and Harbor for resource-constrained environments.


## Table of Contents

- [Why Zot?](#why-zot)
- [Deploy with Docker Compose](#deploy-with-docker-compose)
  - [Basic compose + local storage:](#basic-compose-local-storage)
- [Cloudflare R2 Storage](#cloudflare-r2-storage)
- [Auth Options](#auth-options)
  - [1. htpasswd (for docker CLI)](#1-htpasswd-for-docker-cli)
  - [2. OIDC (for web browser SSO)](#2-oidc-for-web-browser-sso)
  - [3. Dual auth (recommended — htpasswd for CLI + OIDC for web)](#3-dual-auth-recommended-htpasswd-for-cli-oidc-for-web)
  - [4. Traefik Basic Auth (for Dokploy Compose)](#4-traefik-basic-auth-for-dokploy-compose)
  - [5. Dex OIDC](#5-dex-oidc)
- [Access Control (RBAC)](#access-control-rbac)
  - [Actions](#actions)
  - [Permission levels](#permission-levels)
  - [Glob patterns for repos](#glob-patterns-for-repos)
  - [Example config](#example-config)
  - [Anonymous access (public pull)](#anonymous-access-public-pull)
  - [Conditional policies (CEL)](#conditional-policies-cel)
- [Artifact Support](#artifact-support)
  - [Artifact types supported](#artifact-types-supported)
  - [Referrers API](#referrers-api)
- [Extensions](#extensions)
- [Dokploy Compose Deployment](#dokploy-compose-deployment)
  - [Full inline Traefik auth for Compose (alternative to Zot auth)](#full-inline-traefik-auth-for-compose-alternative-to-zot-auth)
- [CVE Scanning (Trivy)](#cve-scanning-trivy)
  - [How it works](#how-it-works)
  - [Enable config](#enable-config)
  - [Trivy config options](#trivy-config-options)
  - [What Trivy scans](#what-trivy-scans)
  - [API endpoints](#api-endpoints)
  - [Notes](#notes)
- [Advanced Features](#advanced-features)
  - [📡 Sync / Mirror — Pull-Through Proxy](#sync-mirror-pull-through-proxy)
  - [📦 Retention Policies — Auto-Cleanup](#retention-policies-auto-cleanup)
  - [🚦 Rate Limiting](#rate-limiting)
  - [🔗 Multi-Storage (SubPaths)](#multi-storage-subpaths)
  - [📡 Events (Webhooks)](#events-webhooks)
  - [🔍 Scrub — Data Integrity](#scrub-data-integrity)
  - [⚙️ GC + Dedupe](#gc-dedupe)
  - [🏗️ Clustering](#clustering)
  - [📏 Binary Size](#binary-size)
- [Pitfalls](#pitfalls)

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

### 5. Dex OIDC

Dex as OIDC provider for Zot browser login. Requires API key for `docker login`.

**Zot config (`zot-config.json`):**

```json
{
  "http": {
    "auth": {
      "sessionKeysFile": "/etc/zot/sessionKeys.json",
      "apikey": true,
      "openid": {
        "callbackAllowOrigins": ["https://registry.example.com"],
        "providers": {
          "dex": {
            "name": "Dex",
            "issuer": "https://auth.example.com",
            "credentialsFile": "/etc/zot/dex-credentials.json",
            "scopes": ["openid", "profile", "email"],
            "claimMapping": {
              "username": "preferred_username",
              "groups": "groups"
            }
          }
        }
      }
    }
  }
}
```

**`dex-credentials.json`** (mount at `/etc/zot/`):
```json
{
  "clientid": "zot",
  "clientsecret": "zot-client-secret-change-me"
}
```

**How it works:**
1. User opens `https://registry.example.com` → clicks "Login with Dex"
2. Redirected to Dex → authenticates → redirected back
3. Zot UI now shows authenticated user
4. **For docker CLI** — user generates API key from Zot UI, then:
   ```bash
   docker login -u <username> -p <api_key> registry.example.com
   ```

> See full Dex setup in [dex-oidc.md](./dex-oidc.md).

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

## CVE Scanning (Trivy)

Zot embeds **Trivy as a library** (not a separate binary) — every scan runs inside the Zot process.

### How it works

1. Push image to Zot
2. Zot **automatically triggers** Trivy scan on the new image
3. Results are **cached by digest** — same image (same digest) pushed again won't rescan
4. Shared base image layers are detected — no redundant rescans
5. Trivy vulnerability DB updates periodically based on `updateInterval`
6. Results visible via **Web UI** or **REST API**

### Enable config

```json
{
  "extensions": {
    "search": {
      "cve": {
        "updateInterval": "2h",
        "trivy": {
          "dbRepository": "ghcr.io/aquasecurity/trivy-db",
          "javaDBRepository": "ghcr.io/aquasecurity/trivy-java-db",
          "vulnSeveritySources": ["auto"]
        }
      }
    },
    "ui": {
      "enable": true
    }
  }
}
```

Minimal config (just `updateInterval`):

```json
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
```

### Trivy config options

| Field | Default | Description |
|-------|---------|-------------|
| `updateInterval` | `2h` | How often to update Trivy vulnerability DB |
| `dbRepository` | `ghcr.io/aquasecurity/trivy-db` | Trivy DB container image reference |
| `javaDBRepository` | `ghcr.io/aquasecurity/trivy-java-db` | Java vulnerability DB reference |
| `vulnSeveritySources` | `["auto"]` | Severity source: `auto`, `nvd`, `redhat`, etc. |
| `sbom.enable` | `false` | Generate SBOM during scan |
| `sbom.format` | `"spdx-json"` | SBOM format: `spdx-json` or `cyclonedx` |

### What Trivy scans

- **OS packages** — Alpine, Debian, Ubuntu, CentOS, etc.
- **Language packages** — pip, npm, gem, maven, go modules, cargo
- **Shared base images** — recognizes reused layers across images

**Not scanned:** Dockerfile misconfigurations, IaC scanning, secrets in images.

### API endpoints

Available via REST on `/v2/_zot/ext/search`:

| API | Function |
|-----|----------|
| `GetCVEListForImage` | List CVEs for an image, filterable by `repo`, `tag`, `severity` |
| `GetImageListForCVE` | Find all images affected by a specific CVE |
| `GetImageListWithCVEFixed` | Images where a specific CVE has been fixed |
| `GetCVESummaryForImageMedia` | CVE severity summary for an image |
| `GetCVEDiffListForImages` | CVE comparison between two images (before/after update) |

All APIs are integrated into the **Web UI** — open the registry domain, click an image, see CVE breakdown by severity.

### Notes

- `search` extension does **not** need `"enable": true` — the `cve` sub-block implicitly enables it
- `ui` **does** need `"enable": true` (different from search)
- CVE results are cached efficiently — only new/changed layers trigger a rescan
- The Trivy DB download happens on first scan, then periodically per `updateInterval`

---

## Advanced Features

### 📡 Sync / Mirror — Pull-Through Proxy

Zot can act as a **Docker Hub mirror / pull-through cache**. When an image isn't found locally, it automatically pulls from the upstream registry and caches it.

```json
{
  "extensions": {
    "sync": {
      "enable": true,
      "credentialsFile": "./sync-auth.json",
      "registries": [
        {
          "urls": ["https://index.docker.io"],
          "onDemand": true,
          "pollInterval": "6h",
          "tlsVerify": true,
          "maxRetries": 5,
          "retryDelay": "30s"
        }
      ]
    }
  }
}
```

**Key features:**
- **`onDemand: true`** — pull-through proxy mode (cache on first pull)
- **`pollInterval`** — periodic sync (pre-fetch images every N hours)
- **Tag filters** — regex, semver, exclude patterns
- **Prefix remapping** — strip or rename repo prefixes on sync
- **Only signed** — `onlySigned: true` to sync only cosign-signed images
- **Multiple upstreams** — can sync from different registries simultaneously

Example with tag filtering + prefix remapping:

```json
{
  "urls": ["https://registry.example.com"],
  "onDemand": false,
  "pollInterval": "6h",
  "content": [
    {
      "prefix": "/library/nginx",
      "destination": "/nginx",
      "stripPrefix": true,
      "tags": { "semver": true }
    }
  ]
}
```

### 📦 Retention Policies — Auto-Cleanup

Automatically delete old/stale images based on configurable rules. Essential for CI/CD pipelines that push images on every build.

```json
{
  "storage": {
    "retention": {
      "dryRun": false,
      "delay": "24h",
      "policies": [
        {
          "repositories": ["prod/**"],
          "deleteReferrers": false,
          "keepTags": [
            { "patterns": ["v2.*", ".*-stable"] },
            { "mostRecentlyPushedCount": 10 },
            { "mostRecentlyPulledCount": 5 }
          ]
        },
        {
          "repositories": ["tmp/**"],
          "deleteUntagged": true,
          "deleteReferrers": true,
          "keepTags": [
            { "pushedWithin": "168h" },
            { "pulledWithin": "720h" }
          ]
        },
        {
          "repositories": ["**"],
          "deleteUntagged": true,
          "keepTags": [
            { "mostRecentlyPushedCount": 50 }
          ]
        }
      ]
    }
  }
}
```

**Retention rules:**
| Rule | Description |
|------|-------------|
| `patterns` | Keep tags matching regex (e.g. `v2.*`) |
| `mostRecentlyPushedCount` | Keep last N pushed tags |
| `mostRecentlyPulledCount` | Keep last N pulled tags |
| `pushedWithin` | Keep tags pushed within duration (e.g. `"168h"` = 7 days) |
| `pulledWithin` | Keep tags pulled within duration |
| `deleteUntagged` | Remove orphaned blobs without tags |
| `deleteReferrers` | Remove linked artifacts (signatures, SBOMs) |

**⚠️ Use `dryRun: true` first** to preview what would be deleted.

### 🚦 Rate Limiting

Protect the registry from abuse or CI stampedes:

```json
{
  "http": {
    "ratelimit": {
      "rate": 100,
      "methods": [
        { "method": "GET", "rate": 50 },
        { "method": "PUT", "rate": 20 }
      ]
    }
  }
}
```

Rate is **requests per second**. Per-method overrides the global rate.

### 🔗 Multi-Storage (SubPaths)

One Zot instance can serve multiple storage backends at different repo prefixes:

```json
{
  "storage": {
    "rootDirectory": "/var/lib/zot",
    "dedupe": true,
    "gc": true,
    "subPaths": {
      "/base": {
        "rootDirectory": "/mnt/ssd/base-images",
        "dedupe": true
      },
      "/cache": {
        "rootDirectory": "/mnt/hdd/cache",
        "dedupe": true
      },
      "/scratch": {
        "rootDirectory": "/mnt/tmp/scratch",
        "dedupe": false
      }
    }
  }
}
```

Each sub-path can have:
- Different storage backend (local, S3, R2)
- Independent dedupe setting
- Independent retention policy

### 📡 Events (Webhooks)

Trigger HTTP calls or NATS messages on registry events (push, pull, delete):

```json
{
  "extensions": {
    "events": {
      "enable": true,
      "sinks": [
        {
          "type": "http",
          "address": "https://hooks.example.com/registry",
          "timeout": "10s"
        },
        {
          "type": "nats",
          "address": "nats://127.0.0.1:4222",
          "channel": "registry-events"
        }
      ]
    }
  }
}
```

Useful for:
- Triggering CI/CD pipelines on push
- Audit logging to external systems
- Slack/Telegram notifications

### 🔍 Scrub — Data Integrity

Periodically checks blob integrity in storage:

```json
{
  "extensions": {
    "scrub": {
      "enable": true,
      "interval": "24h"
    }
  }
}
```

Detects corruption, bit rot, or missing blobs — especially useful for R2/S3 storage.

### ⚙️ GC + Dedupe

Built-in garbage collection and cross-repo deduplication — no cron jobs needed:

```json
{
  "storage": {
    "gc": true,
    "gcDelay": "2h",
    "gcInterval": "1h",
    "dedupe": true
  }
}
```

- **GC** removes unused blobs after tag deletion — delay prevents accidental removal
- **Dedupe** shares layers across repositories — saves significant storage
- Works across sub-paths

### 🏗️ Clustering

Zot supports **scale-out clustering** for cloud deployments with shared storage (R2/S3/GCS). Multiple Zot instances can point to the same backend storage. See the [clustering article](https://zotregistry.dev/articles/clustering/) for details.

### 📏 Binary Size

| Build | Size | Use Case |
|-------|------|----------|
| **Full** (`zot-linux-amd64`) | ~20MB | All extensions included |
| **Minimal** (`zot-linux-amd64-minimal`) | ~15MB | Embedded / minimal attack surface |

The minimal build strips all extensions (no sync, search, UI, etc.) — just a bare OCI distribution-spec registry.

---

## Pitfalls

- **Port exposure:** `127.0.0.1:5000:5000` = localhost only (safe for proxy pattern). `5000:5000` = public (dangerous without auth)
- **UI needs search + CVE:** Zot v2.1.x requires `extensions.search.cve` for UI to work
- **Search extension has no `enable` flag:** Unlike `ui`, search is enabled implicitly by the `cve` sub-block
- **UI uses absolute paths:** If proxied under a sub-path, static assets (JS/CSS) may break. Use subdomain instead
- **No fine-grained RBAC per namespace:** Zot has per-repo policies but no project-level namespace isolation like Harbor
- **R2 region:** Must be `"auto"` — AWS region strings will fail
