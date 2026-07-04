---
title: Chisel — Fast TCP/UDP Tunnel over HTTP
description: - [Overview](#overview) - [Installation](#installation) - [Quick Start](#quick-start) - [Tunnel Examples](#tunnel-examples) - [Reverse Tunneling](#reverse-tunneling) - [SOCKS5 Guide](#socks5-guide) - [Auth & Security](#auth--security) - [Docker](#docker) - [Use Cases](#use-cases) - [Pitfalls](#pitfalls)
---

# Chisel — Fast TCP/UDP Tunnel over HTTP

> **Last updated:** 2026-07-04
> **Repo:** [jpillora/chisel](https://github.com/jpillora/chisel) ⭐ 16.2k
> **Language:** Go — single binary, client + server in one
> **License:** MIT

**Chisel** is a fast TCP/UDP tunnel transported over HTTP, secured via SSH. Single executable including both client and server. Perfect for passing through firewalls, exposing services behind NAT, and creating secure endpoints into your network.

## Table of Contents

- [Overview](#overview)
  - [How It Works](#how-it-works)
  - [Key Features](#key-features)
- [Installation](#installation)
  - [Quick Install](#quick-install)
  - [Docker](#docker)
  - [From Source](#from-source)
- [Quick Start](#quick-start)
  - [Server](#server)
  - [Client](#client)
- [Tunnel Examples](#tunnel-examples)
  - [Basic Port Forwarding](#basic-port-forwarding)
  - [Custom Local Host](#custom-local-host)
  - [UDP Tunneling](#udp-tunneling)
  - [Multiple Remotes](#multiple-remotes)
  - [Stdio Tunnel (SSH ProxyCommand)](#stdio-tunnel-ssh-proxycommand)
- [Reverse Tunneling](#reverse-tunneling)
  - [Basic Reverse](#basic-reverse)
  - [Reverse SOCKS5](#reverse-socks5)
- [SOCKS5 Guide](#socks5-guide)
  - [Standard SOCKS5](#standard-socks5)
  - [Reverse SOCKS5](#reverse-socks5-1)
- [Auth & Security](#auth--security)
  - [Server Auth File](#server-auth-file)
  - [Fingerprint Verification](#fingerprint-verification)
  - [Mutual TLS](#mutual-tls)
- [Docker](#docker)
  - [Docker Compose](#docker-compose)
- [Use Cases](#use-cases)
  - [Database Backup Through Tunnel](#database-backup-through-tunnel)
  - [Expose Dev Server](#expose-dev-server)
  - [Multi-VPS Mesh](#multi-vps-mesh)
- [Pitfalls](#pitfalls)

---

## Overview

Chisel creates an **SSH-encrypted tunnel** over **HTTP** (or HTTPS/WebSocket). All traffic looks like normal HTTP requests to firewalls/proxies, making it extremely effective at bypassing network restrictions.

```
┌─────────┐     HTTP/HTTPS      ┌─────────┐
│  Client  │ ──────────────────→ │  Server │
│ (NAT/FW) │   SSH-encrypted    │ (Public)│
└─────────┘     tunnel          └─────────┘
     │                                │
     │ localhost:3306                 │ localhost:3000
     ▼                                ▼
  MySQL DB                        Web App
```

### Key Features

| Feature | Description |
|---------|-------------|
| **SSH encryption** | All traffic encrypted via `crypto/ssh` (ECDSA) |
| **Single binary** | Client + server in one ~10MB executable |
| **Reverse tunnels** | Server listens → client serves |
| **SOCKS5 proxy** | Route browser traffic through tunnel |
| **UDP support** | Tunnel UDP over TCP/HTTP |
| **Auto-reconnect** | Exponential backoff on disconnect |
| **Auth + ACL** | Per-user authentication with address regex |
| **Fingerprint verification** | MITM protection via key fingerprint |
| **Mutual TLS** | Certificate-based client authentication |
| **LetsEncrypt** | Auto HTTPS via `--tls-domain` |

---

## Installation

### Quick Install

```bash
curl https://i.jpillora.com/chisel! | bash
```

### Package Managers

| Manager | Command |
|---------|---------|
| **Homebrew** | `brew install chisel` |
| **Fedora** | `sudo dnf install chisel` |
| **Docker** | `docker pull jpillora/chisel` |

### From Source

```bash
go install github.com/jpillora/chisel@latest
```

### Verify

```bash
chisel --help
# Usage: chisel [command] [--help]
# Commands:
#   server - runs chisel in server mode
#   client - runs chisel in client mode
```

---

## Quick Start

### Server

```bash
chisel server -p 9312 --reverse
```

This starts a chisel server on port 9312 with reverse tunnel support enabled.

```
2026/07/04 10:00:00 server: Fingerprint 3c:2a:...:e7
2026/07/04 10:00:00 server: Listening on http://0.0.0.0:9312
```

> **⚠️ Save the fingerprint!** You'll need it on the client for secure connections.

### Client

```bash
chisel client <server-address>:9312 3000
```

Tunnels the server's `localhost:3000` → client's `localhost:3000` (forward tunnel).

---

## Tunnel Examples

### Basic Port Forwarding

Tunnel a remote service to your local machine:

```bash
# Syntax: <local-port>:<remote-host>:<remote-port>
chisel client server.com:9312 8080:internal-web:80
```

Forward in 4 forms:

| Remote | Meaning |
|--------|---------|
| `3000` | `0.0.0.0:3000` → `server:3000` (default local/remote match) |
| `example.com:3000` | `0.0.0.0:3000` → `example.com:3000` |
| `3000:google.com:80` | `0.0.0.0:3000` → `google.com:80` |
| `192.168.0.5:3000:google.com:80` | `192.168.0.5:3000` → `google.com:80` |

### Custom Local Host

```bash
chisel client server.com:9312 127.0.0.1:5432:db.internal:5432
# Client listens on localhost:5432 → server connects to db.internal:5432
```

### UDP Tunneling

Add `/udp` suffix:

```bash
chisel client server.com:9312 1.1.1.1:53/udp
# Tunnel DNS queries through chisel
```

### Multiple Remotes

```bash
chisel client server.com:9312 \
  3306:localhost:3306 \     # MySQL
  5432:localhost:5432 \     # PostgreSQL
  3000:localhost:3000       # Web App
```

All three tunnels share **one TCP connection** — efficient.

### Stdio Tunnel (SSH ProxyCommand)

```bash
# Tunnel SSH through chisel
ssh -o ProxyCommand='chisel client chisel-server.com stdio:%h:%p' \
    user@internal-server.com
```

---

## Reverse Tunneling

> Requires server started with `--reverse`

### Basic Reverse

Expose a **local** service to the **server** (useful for NAT/firewall traversal):

```bash
# Syntax: R:<server-port>:<local-host>:<local-port>
chisel client server.com:9312 R:3000:localhost:3000
```

Now `server.com:3000` → your local `localhost:3000`.

| Reverse Remote | Meaning |
|----------------|---------|
| `R:2222:localhost:22` | Server's `localhost:2222` → client's SSH |
| `R:8080:localhost:80` | Server's `localhost:8080` → client's web app |
| `R:80:192.168.1.10:3000` | Server's `localhost:80` → client's LAN service |

### Reverse SOCKS5

```bash
chisel client server.com:9312 R:socks
# Server listens on port 1080 (default SOCKS port)
# All SOCKS traffic forwarded → client
```

---

## SOCKS5 Guide

### Standard SOCKS5

1. Start server with `--socks5`:

```bash
chisel server -p 9312 --socks5 --keyfile /path/to/key
```

2. Connect client:

```bash
chisel client server.com:9312 socks
```

3. Configure browser/OS to use `localhost:1080` as SOCKS5 proxy.

### Reverse SOCKS5

With `--reverse` on server:

```bash
chisel client server.com:9312 R:socks
# Server opens SOCKS5 proxy on port 1080
# Connections route through the client
```

---

## Auth & Security

### Server Auth File

Create `users.json`:

```json
{
  "admin:StrongPass1": [""],
  "backup:BackupPass123": ["db.internal:3306", "db.internal:5432"],
  "dev:DevPass456": ["dev-server:3000"]
}
```

- `""` = full access (all addresses)
- Address regexes restrict which remotes a user can create
- File auto-reloads on change

> **⚠️ CRITICAL:** Auth file matches the **exact string** `user:pass` — make sure the colon is between username and password, not a typo in file format.

Run server with auth:

```bash
chisel server -p 9312 --reverse --authfile users.json
```

Or single user via env:

```bash
AUTH=admin:StrongPass1 chisel server -p 9312 --reverse
```

### Fingerprint Verification

Client verifies server's key (MITM protection):

```bash
chisel client \
  --fingerprint '3c:2a:...:e7' \
  server.com:9312 3000
```

Generate a persistent key for consistent fingerprint:

```bash
chisel server --keygen /path/to/chisel-key
# Then use it:
chisel server -p 9312 --keyfile /path/to/chisel-key
```

### Mutual TLS

Server-side CA verification:

```bash
chisel server -p 443 \
  --tls-domain yourdomain.com \
  --tls-ca /path/to/ca-bundle.pem
```

Client-side cert auth:

```bash
chisel client https://server.com:443 \
  --tls-key /path/to/client-key.pem \
  --tls-cert /path/to/client-cert.pem \
  3000
```

---

## Docker

```bash
# Run server
docker run --rm -p 9312:9312 jpillora/chisel server -p 9312 --reverse

# Run client
docker run --rm jpillora/chisel client server.com:9312 3000
```

### Docker Compose

```yaml
services:
  chisel-server:
    image: jpillora/chisel:latest
    container_name: chisel
    restart: unless-stopped
    command: server -p 9312 --reverse --authfile /etc/chisel/users.json
    ports:
      - "9312:9312"
    volumes:
      - ./chisel-key:/etc/chisel/key
      - ./users.json:/etc/chisel/users.json
    environment:
      - TZ=Asia/Jakarta
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:9312/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Use Cases

### Database Backup Through Tunnel

Backup DBs on a server without public ports — just outbound HTTP:

```bash
# On backup-server (has access to all DBs)
chisel client -v \
  --auth "backup:BackupPass123" \
  --fingerprint '3c:2a:...' \
  public-server.com:9312 \
  3307:db1.internal:3306 \
  5433:db2.internal:5432

# On public-server (chisel server)
chisel server -p 9312 --reverse --authfile users.json
```

Then backup from public-server (or even another client):

```bash
# Tunnel back to access the DBs
chisel client public-server.com:9312 \
  3306:localhost:3307 \
  5432:localhost:5433

# Now backup from local
mysqldump -h localhost -P 3306 -u backup -p'pass' --all-databases > backup.sql
pg_dump -h localhost -p 5432 -U backup dbname > backup.sql
```

Or better — use reverse tunnel to let a centralized backup server pull:

```bash
# On each VPS with DB (client behind NAT)
chisel client backup-center.com:9312 \
  R:3306:localhost:3306     # expose local MySQL to backup-center

# On backup-center (chisel server + runs backup scripts)
chisel server -p 9312 --reverse
# Now backup-center:3306 → VPS's MySQL
```

### Expose Dev Server

```bash
# Developer laptop (behind NAT/cafe WiFi)
chisel client public-server.com:9312 \
  R:3000:localhost:3000   # expose local dev server

# Client/manager accesses:
# → public-server.com:3000 → your laptop's localhost:3000
```

### Multi-VPS Mesh

For your multi-provider setup (DO, Hetzner, BiznetGIO):

```bash
# Hub server (public)
chisel server -p 9312 --reverse --authfile users.json

# Each VPS connects as client
chisel client --auth "vps1:pass1" hub.com:9312 \
  R:9100:localhost:9100   # node_exporter metrics

chisel client --auth "vps2:pass2" hub.com:9312 \
  R:9101:localhost:9100
```

Now hub can scrape all metrics from `localhost:9100`, `localhost:9101`, etc.

---

## Pitfalls

### ❌ Fingerprint mismatch on reconnect
When server restarts with a new random key, clients with `--fingerprint` will fail.
**Fix:** Generate persistent key with `chisel server --keygen` and always use `--keyfile`.

### ❌ WebSocket required
Since chisel uses WebSocket transport under the hood, it won't work behind proxies that block WebSocket upgrade headers. Most cloud providers work, but some restrictive corporate proxies may block it.

### ❌ Keepalive needed through proxies
Proxies often close idle connections. Use `--keepalive 25s` (default) or increase it:
```bash
chisel client --keepalive 10s server.com:9312 3000
```

### ❌ Auth file colon confusion
The auth file format is `"user:pass": [...]` — the colon separates username AND password. If your password contains a colon, it breaks.
**Fix:** Avoid colons in passwords, or handle encoding on the server side.

### ❌ Reverse tunnel port conflicts
If two clients try to open the same reverse port, the second one fails silently.
**Fix:** Assign unique ports per client, or use a coordinator script.

### ❌ UDP limitations
UDP is tunneled over TCP — packet loss on the TCP layer causes head-of-line blocking for UDP streams.
**Fix:** For real-time UDP (VoIP, gaming), consider WireGuard instead.

### ❌ Big file transfers
Chisel isn't optimized for bulk data — SSH encryption + HTTP framing adds overhead.
**Fix:** For large database dumps, compress first (`gzip`), or use rsync over the tunnel.
