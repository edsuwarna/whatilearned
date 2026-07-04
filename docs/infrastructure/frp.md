---
title: frp — Fast Reverse Proxy for NAT Traversal
description: - [Overview](#overview) - [Installation](#installation) - [Quick Start](#quick-start) - [Proxy Types](#proxy-types) - [Use Cases](#use-cases) - [frp vs Chisel](#frp-vs-chisel) - [Dashboard & Monitoring](#dashboard--monitoring) - [Auth](#authentication) - [Security](#security) - [Docker](#docker) - [Tips & Pitfalls](#tips--pitfalls)
---

# frp — Fast Reverse Proxy for NAT Traversal

> **Last updated:** 2026-07-04
> **Version:** v0.69.1
> **Repo:** [fatedier/frp](https://github.com/fatedier/frp) ⭐ 108k
> **Language:** Go — single binary, client (frpc) + server (frps)
> **License:** Apache 2.0

**frp** is a fast reverse proxy that exposes local servers behind NAT/firewall to the internet. Supports **TCP**, **UDP**, **HTTP**, **HTTPS**, and **P2P** modes.

## Table of Contents

- [Overview](#overview)
  - [Architecture](#architecture)
  - [Key Features](#key-features)
- [Installation](#installation)
  - [Quick Install](#quick-install)
  - [From Source](#from-source)
- [Quick Start](#quick-start)
  - [Server (frps)](#server-frps)
  - [Client (frpc)](#client-frpc)
  - [Config Format](#config-format)
- [Proxy Types](#proxy-types)
  - [TCP](#tcp)
  - [UDP](#udp)
  - [HTTP/HTTPS](#httphttps)
  - [STCP (Secret TCP)](#stcp-secret-tcp)
  - [XTCP (P2P)](#xtcp-p2p)
  - [TCPMUX](#tcpmux)
- [Use Cases](#use-cases)
  - [Database Backup Tunnel](#database-backup-tunnel)
  - [Multi-VPS Mesh](#multi-vps-mesh)
  - [Expose Web App with Domain](#expose-web-app-with-domain)
  - [Load Balancing](#load-balancing)
  - [SSH Gateway](#ssh-gateway)
  - [Virtual Network (TUN)](#virtual-network-tun)
- [frp vs Chisel](#frp-vs-chisel)
- [Dashboard & Monitoring](#dashboard--monitoring)
  - [Server Dashboard](#server-dashboard)
  - [Client Admin UI](#client-admin-ui)
  - [Prometheus](#prometheus)
- [Authentication](#authentication)
  - [Token Auth](#token-auth)
  - [OIDC Auth](#oidc-auth)
  - [Per-Proxy Auth](#per-proxy-auth)
- [Security](#security)
  - [TLS](#tls)
  - [Encryption & Compression](#encryption--compression)
  - [Port Whitelist](#port-whitelist)
- [Docker](#docker)
  - [Docker Compose](#docker-compose-frps)
- [Advanced Features](#advanced-features)
  - [Hot Reload](#hot-reload)
  - [Health Check](#health-check)
  - [Bandwidth Limit](#bandwidth-limit)
  - [KCP/QUIC Transport](#kcpquic-transport)
  - [Connection Pooling](#connection-pooling)
  - [Plugin System](#plugin-system)
- [Tips & Pitfalls](#tips--pitfalls)

---

## Overview

frp lets you expose services behind NAT/firewall through a public server. It supports **TCP**, **UDP**, **HTTP**, and **HTTPS** protocols with features like load balancing, health checks, authentication, and a built-in web dashboard.

### Architecture

```
┌──────────┐    control conn     ┌──────────┐
│  frpc    │ ◄─────────────────► │  frps    │ ◄──── User
│ (NAT)    │                     │ (Public) │       (HTTP/TCP/UDP)
│          │    proxy conn       │          │
│ local:80 ├─────────────────────►  :8080   │
└──────────┘                     └──────────┘
```

- **frps** — server on public VPS
- **frpc** — client behind NAT, connects to frps and exposes local services

### Key Features

| Feature | Description |
|---------|-------------|
| **TCP/UDP** | Basic port forwarding |
| **HTTP/HTTPS** | Domain-based virtual hosting |
| **STCP** | Secret TCP — preshared key required to access |
| **XTCP** | P2P mode — direct connection between clients |
| **Dashboard** | Built-in web UI for monitoring |
| **Client Admin** | Manage proxies via REST API + Web UI |
| **Token/OIDC** | Multiple auth methods |
| **TLS** | Encrypted transport, mutual TLS |
| **Load balancing** | Group-based round-robin |
| **Health checks** | TCP ping / HTTP status monitoring |
| **Hot reload** | Reload config without restart |
| **KCP/QUIC** | Alternative transports for high-latency links |
| **Plugins** | socks5, static_file, http_proxy, unix socket |
| **SSH Gateway** | Use SSH `-R` instead of frpc |

---

## Installation

### Quick Install

Download from [releases](https://github.com/fatedier/frp/releases):

```bash
# Linux amd64
wget https://github.com/fatedier/frp/releases/download/v0.69.1/frp_0.69.1_linux_amd64.tar.gz
tar xzf frp_0.69.1_linux_amd64.tar.gz
sudo cp frp_0.69.1_linux_amd64/frps /usr/local/bin/
sudo cp frp_0.69.1_linux_amd64/frpc /usr/local/bin/
```

### From Source

```bash
go install github.com/fatedier/frp/v2/cmd/frps@latest
go install github.com/fatedier/frp/v2/cmd/frpc@latest
```

---

## Quick Start

### Server (frps)

```toml
# frps.toml
bindPort = 7000

# Dashboard
webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "admin"
```

```bash
./frps -c frps.toml
```

### Client (frpc)

```toml
# frpc.toml
serverAddr = "your-server.com"
serverPort = 7000

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

```bash
./frpc -c frpc.toml
```

Now `ssh -oPort=6000 your-server.com` connects to the client's SSH.

### Config Format

Since v0.52.0, frp uses **TOML** (recommended). YAML and JSON are also supported. **INI is deprecated.**

- `frps.toml` — server config
- `frpc.toml` — client config
- Can split into multiple files with `includes = ["./confd/*.toml"]`
- Supports **environment variables**: `serverAddr = "{{ .Envs.FRP_SERVER_ADDR }}"`

---

## Proxy Types

### TCP

```toml
[[proxies]]
name = "mysql"
type = "tcp"
localIP = "127.0.0.1"
localPort = 3306
remotePort = 3306
```

Now `your-server.com:3306` → client's `localhost:3306`.

### UDP

```toml
[[proxies]]
name = "dns"
type = "udp"
localIP = "8.8.8.8"
localPort = 53
remotePort = 6000
```

```bash
dig @your-server.com -p 6000 www.google.com
```

### HTTP/HTTPS

Server needs `vhostHTTPPort`:

```toml
# frps.toml
bindPort = 7000
vhostHTTPPort = 8080
```

```toml
# frpc.toml
[[proxies]]
name = "web"
type = "http"
localPort = 80
customDomains = ["app.yourdomain.com"]
```

Point `app.yourdomain.com` DNS A record to frps server IP, then visit `http://app.yourdomain.com:8080`.

For **HTTPS**, use `vhostHTTPSPort` on server and `type = "https"` on client. You can also use the `https2http` plugin:

```toml
[[proxies]]
name = "secure-web"
type = "https"
customDomains = ["app.yourdomain.com"]

[proxies.plugin]
type = "https2http"
localAddr = "127.0.0.1:80"
crtPath = "./server.crt"
keyPath = "./server.key"
hostHeaderRewrite = "127.0.0.1"
```

### STCP (Secret TCP)

Creates a **private tunnel** — only accessible by visitors with the matching `secretKey`. The service is **not** exposed on a public port.

```toml
# frpc.toml (service provider — behind NAT)
[[proxies]]
name = "secret_ssh"
type = "stcp"
secretKey = "abcdefg"
localIP = "127.0.0.1"
localPort = 22
```

```toml
# frpc.toml (visitor — also behind NAT, but authorized)
[[visitors]]
name = "secret_ssh_visitor"
type = "stcp"
serverName = "secret_ssh"
secretKey = "abcdefg"
bindAddr = "127.0.0.1"
bindPort = 6000
```

Then `ssh -oPort=6000 127.0.0.1` from the visitor's machine connects through the secret tunnel.

### XTCP (P2P)

Like STCP but **direct peer-to-peer connection** — once the tunnel is established, data flows directly between clients (no server relay). Uses STUN for NAT traversal.

```toml
# frpc.toml (provider)
[[proxies]]
name = "p2p_ssh"
type = "xtcp"
secretKey = "abcdefg"
localIP = "127.0.0.1"
localPort = 22
```

```toml
# frpc.toml (visitor)
[[visitors]]
name = "p2p_ssh_visitor"
type = "xtcp"
serverName = "p2p_ssh"
secretKey = "abcdefg"
bindAddr = "127.0.0.1"
bindPort = 6000
keepTunnelOpen = false
```

> **⚠️ XTCP doesn't work with all NAT types.** Falls back to STCP if NAT traversal fails.

### TCPMUX

Multiple proxies sharing one server port via HTTP CONNECT:

```toml
# frps.toml
tcpmuxHTTPConnectPort = 5002
```

```toml
# frpc.toml
[[proxies]]
name = "ssh1"
type = "tcpmux"
multiplexer = "httpconnect"
customDomains = ["machine-a.example.com"]
localIP = "127.0.0.1"
localPort = 22

[[proxies]]
name = "ssh2"
type = "tcpmux"
multiplexer = "httpconnect"
customDomains = ["machine-b.example.com"]
localIP = "127.0.0.1"
localPort = 22
```

```bash
# Access via SOCAT
ssh -o 'proxycommand socat - PROXY:x.x.x.x:%h:%p,proxyport=5002' \
    test@machine-a.example.com
```

---

## Use Cases

### Database Backup Tunnel

```toml
# frpc.toml — on each VPS that has databases
serverAddr = "backup-center.com"
serverPort = 7000
auth.token = "shared-secret-token"

[[proxies]]
name = "vps1-mysql"
type = "tcp"
localIP = "127.0.0.1"
localPort = 3306
remotePort = 3301              # unique port per VPS

[[proxies]]
name = "vps1-postgres"
type = "tcp"
localIP = "127.0.0.1"
localPort = 5432
remotePort = 5431              # unique port per VPS
```

On backup server, schedule:

```bash
# backup-center.com:3301 → vps1's MySQL
# backup-center.com:5431 → vps1's PostgreSQL
mysqldump -h 127.0.0.1 -P 3301 -u backup -p'pass' --all-databases | gzip > vps1-$(date +%F).sql.gz
pg_dump -h 127.0.0.1 -p 5431 -U backup dbname | gzip > vps1-db-$(date +%F).sql.gz
```

### Multi-VPS Mesh

Central monitoring hub with each VPS exposing metrics:

```toml
# frpc.toml — each VPS
serverAddr = "monitor-hub.com"
serverPort = 7000

[[proxies]]
name = "node-exporter"
type = "tcp"
localIP = "127.0.0.1"
localPort = 9100
remotePort = 9100              # unique per VPS — 9100, 9101, 9102...
```

### Expose Web App with Domain

```toml
# frps.toml
bindPort = 7000
vhostHTTPPort = 80             # direct HTTP access
vhostHTTPSPort = 443           # optional HTTPS
subDomainHost = "frp.yourdomain.com"
```

```toml
# frpc.toml
[[proxies]]
name = "grafana"
type = "http"
localPort = 3000
subdomain = "grafana"
```

Now `grafana.frp.yourdomain.com` → localhost:3000.

### Load Balancing

```toml
# Two frpc instances serving the same backend
[[proxies]]
name = "web-1"
type = "tcp"
localPort = 8080
remotePort = 80
loadBalancer.group = "web"
loadBalancer.groupKey = "123"

[[proxies]]
name = "web-2"
type = "tcp"
localPort = 8081
remotePort = 80
loadBalancer.group = "web"
loadBalancer.groupKey = "123"
```

frps distributes connections to `:80` randomly between `web-1` and `web-2`.

### SSH Gateway

frps can accept SSH `-R` connections **without frpc**:

```toml
# frps.toml
sshTunnelGateway.bindPort = 2200
```

Then:

```bash
ssh -R :80:127.0.0.1:8080 v0@your-server.com -p 2200 tcp --proxy_name "test-tcp" --remote_port 9090
```

This exposes `localhost:8080` as `your-server.com:9090`, equivalent to running `frpc tcp`.

### Virtual Network (TUN)

*Alpha feature — requires `featureGates = { VirtualNet = true }`*

Enables IP-level routing between machines through a TUN interface — extends frp beyond port forwarding to full virtual networking.

---

## frp vs Chisel

| Aspect | frp | Chisel |
|--------|:---:|:------:|
| **Stars** | 108k ⭐ | 16.2k ⭐ |
| **Language** | Go | Go |
| **Binary** | 2 files (frps + frpc) | 1 file (client+server) |
| **Config format** | TOML/YAML/JSON | CLI flags |
| **Web Dashboard** | ✅ Built-in (server + client) | ❌ |
| **HTTP Reverse Proxy** | ✅ Virtual host routing | ✅ Backend proxy |
| **HTTPS Termination** | ✅ Built-in | ✅ (LetsEncrypt) |
| **STCP (secret tunnel)** | ✅ Preshared key access | ✅ users.json ACL |
| **P2P (direct connect)** | ✅ XTCP mode | ❌ |
| **Load Balancing** | ✅ Group-based | ❌ |
| **Health Checks** | ✅ TCP ping + HTTP | ❌ |
| **Hot Reload** | ✅ API + CLI | ❌ (restart required) |
| **REST API** | ✅ Full CRUD | ❌ |
| **Prometheus** | ✅ Metrics endpoint | ❌ |
| **KCP/QUIC** | ✅ | ❌ |
| **Bandwidth limit** | ✅ Per-proxy | ❌ |
| **Plugin system** | ✅ (socks5, file, etc.) | ❌ |
| **SSH Tunnel Gateway** | ✅ | ❌ |
| **Auth methods** | Token + OIDC | users.json + fingerprint |
| **TLS** | ✅ Mutual TLS | ✅ Mutual TLS |
| **Ease of use** | Config files required | Single CLI command |
| **Binary size** | ~15MB (combined) | ~10MB |
| **Active dev** | ✅ Very active | ✅ Active |

**When to use frp:**
- Need **web dashboard** to monitor tunnels
- Need **load balancing** across multiple backends
- Need **HTTP virtual hosting** (domain-based routing)
- Need **health checks** for high availability
- Need **REST API** for dynamic proxy management
- Need **P2P** direct connections (XTCP)
- Managing **many services** across multiple VPS

**When to use Chisel:**
- Want **single binary** simplicity (client+server in one)
- Need **quick ad-hoc tunnels** with CLI flags (no config file)
- Need **SOCKS5** proxy built-in
- Need **UDP tunneling** (frp also has UDP)
- SSH **ProxyCommand** support
- Simpler deployment for small setups

---

## Dashboard & Monitoring

### Server Dashboard

```toml
# frps.toml
webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "admin"

# Optional: HTTPS for dashboard
webServer.tls.certFile = "server.crt"
webServer.tls.keyFile = "server.key"
```

Visit `http://your-server.com:7500` to see:
- Connected clients
- Active proxies with traffic stats
- Bandwidth usage
- Client list with uptime

### Client Admin UI

```toml
# frpc.toml
webServer.addr = "127.0.0.1"
webServer.port = 7400
webServer.user = "admin"
webServer.password = "admin"

# Dynamic proxy management (persist to disk)
[store]
path = "./db.json"
```

Visit `http://127.0.0.1:7400` (via SSH tunnel or locally).

**Dynamic Proxy Management (Store):** Create, update, delete proxies at runtime via Web UI or REST API. Changes persist and restore on restart.

### Prometheus

```toml
# frps.toml (dashboard must be enabled)
webServer.addr = "0.0.0.0"
webServer.port = 7500
enablePrometheus = true
```

Metrics at `http://your-server.com:7500/metrics`.

---

## Authentication

### Token Auth

```toml
# frps.toml
auth.method = "token"
auth.token = "your-secure-token"
```

```toml
# frpc.toml
auth.method = "token"
auth.token = "your-secure-token"
```

Token from file:

```toml
# frpc.toml
auth.method = "token"
auth.tokenSource.type = "file"
auth.tokenSource.file.path = "/path/to/token/file"
```

### OIDC Auth

```toml
# frps.toml
auth.method = "oidc"
auth.oidc.issuer = "https://your-oidc-issuer.com/"
auth.oidc.audience = "https://audience.com/.default"
```

```toml
# frpc.toml
auth.method = "oidc"
auth.oidc.clientID = "your-client-id"
auth.oidc.clientSecret = "your-client-secret"
auth.oidc.audience = "https://audience.com/.default"
auth.oidc.tokenEndpointURL = "https://issuer.com/oauth2/v2.0/token"
```

### Per-Proxy Auth

HTTP/HTTPS proxies support **HTTP Basic Auth**:

```toml
[[proxies]]
name = "web"
type = "http"
localPort = 80
customDomains = ["app.example.com"]
httpUser = "abc"
httpPassword = "abc"
```

---

## Security

### TLS

TLS is **enabled by default** since v0.50.0.

```toml
# frpc.toml — with mutual TLS
transport.tls.enable = true
transport.tls.certFile = "client.crt"
transport.tls.keyFile = "client.key"
transport.tls.trustedCaFile = "ca.crt"
```

```toml
# frps.toml — force TLS only
transport.tls.force = true
transport.tls.certFile = "server.crt"
transport.tls.keyFile = "server.key"
transport.tls.trustedCaFile = "ca.crt"
```

### Encryption & Compression

Per-proxy, independent of TLS:

```toml
[[proxies]]
name = "ssh"
type = "tcp"
localPort = 22
remotePort = 6000
transport.useEncryption = true
transport.useCompression = true   # reduces bandwidth
```

### Port Whitelist

Prevent port abuse on server:

```toml
# frps.toml
allowPorts = [
  { start = 2000, end = 3000 },
  { single = 3001 },
  { single = 3003 },
  { start = 4000, end = 50000 }
]
```

---

## Docker

```bash
# Server
docker run --rm -p 7000:7000 -p 7500:7500 \
  -v $(pwd)/frps.toml:/etc/frp/frps.toml \
  snowdreamtech/frps

# Client
docker run --rm \
  -v $(pwd)/frpc.toml:/etc/frp/frpc.toml \
  snowdreamtech/frpc
```

### Docker Compose (frps)

```yaml
services:
  frps:
    image: snowdreamtech/frps:latest
    container_name: frps
    restart: unless-stopped
    ports:
      - "7000:7000"        # frp control
      - "7000:7000/udp"    # KCP/QUIC
      - "7500:7500"        # dashboard
      - "80:80"            # HTTP vhost
      - "443:443"          # HTTPS vhost
      - "2000-3000:2000-3000"  # proxy port range
    volumes:
      - ./frps.toml:/etc/frp/frps.toml:ro
    environment:
      - TZ=Asia/Jakarta
```

---

## Advanced Features

### Hot Reload

Reload config without restarting frpc:

```bash
frpc reload -c ./frpc.toml
```

Must have `webServer` configured. Takes ~10 seconds to apply.

### Health Check

Automatically remove unhealthy backends:

```toml
[[proxies]]
name = "web"
type = "http"
localPort = 80
customDomains = ["app.example.com"]

healthCheck.type = "http"
healthCheck.path = "/health"
healthCheck.timeoutSeconds = 3
healthCheck.maxFailed = 3
healthCheck.intervalSeconds = 10
```

Also supports `type = "tcp"` (TCP ping).

### Bandwidth Limit

```toml
[[proxies]]
name = "ssh"
type = "tcp"
localPort = 22
remotePort = 6000
transport.bandwidthLimit = "1MB"
transport.bandwidthLimitMode = "client"  # or "server"
```

### KCP/QUIC Transport

For high-latency/unreliable links:

```toml
# frps.toml
kcpBindPort = 7000        # same as bindPort
quicBindPort = 7000
```

```toml
# frpc.toml
transport.protocol = "kcp"   # or "quic"
```

### Connection Pooling

```toml
# frps.toml
transport.maxPoolCount = 5

# frpc.toml (per-proxy)
transport.poolCount = 1
```

### Plugin System

Built-in plugins:

| Plugin | Description |
|--------|-------------|
| `unix_domain_socket` | Expose Unix socket as TCP |
| `http_proxy` | HTTP CONNECT proxy server |
| `socks5` | SOCKS5 proxy server |
| `static_file` | Simple HTTP file server |
| `https2http` | Terminate HTTPS, forward as HTTP |
| `https2https` | Terminate HTTPS, forward as HTTPS |

```toml
[[proxies]]
name = "socks"
type = "tcp"
remotePort = 1080
[proxies.plugin]
type = "socks5"
```

Turn frpc into a SOCKS5 proxy — configure browser to use `your-server.com:1080`.

---

## Tips & Pitfalls

### ✅ Use `--user systemd` for production

```ini
# /etc/systemd/system/frps.service
[Unit]
Description=frp server
After=network.target

[Service]
Type=simple
User=nobody
ExecStart=/usr/local/bin/frps -c /etc/frp/frps.toml
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### ✅ Reserve port ranges on server

Use `allowPorts` to prevent rogue clients from binding random ports.

### ⚠️ Don't use INI format

INI is deprecated. All new features only ship in TOML/YAML/JSON. Migrate if you're still on INI.

### ⚠️ Antivirus false positives

Some antivirus flags frpc as malware (it's a reverse proxy tool). Whitelist frpc if needed.

### ⚠️ XTCP doesn't work behind symmetric NAT

XTCP (P2P) may fail with symmetric NAT (common on mobile/cellular networks). Fallback to STCP in those cases.

### ⚠️ Dashboard port should not be public

`webServer.addr = "0.0.0.0"` exposes the dashboard to the internet. Use a firewall or set `127.0.0.1` and access via SSH tunnel.

### ❌ Port reuse limitation

`bindPort`, `vhostHTTPPort`, and `vhostHTTPSPort` can share the same port now, but not all combinations are well-tested.

### ✅ Use STCP for sensitive services

Don't expose databases directly via TCP mode. Use STCP for an extra layer of protection with preshared keys.

### ✅ Compress for low-bandwidth links

Enable `transport.useCompression = true` for high-latency or low-bandwidth tunnels (but adds CPU overhead).
