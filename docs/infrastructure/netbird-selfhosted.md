---
title: Netbird — Self-Hosted WireGuard Mesh VPN with SSO
description: - [Overview](#overview) - [Key Features](#key-features) - [Requirements](#requirements) - [Installation](#installation-self-hosted) - [Quick Start](#quick-start) - [Joining Nodes](#joining-nodes) - [Groups & Policies](#groups--policies) - [Routing Peers](#routing-peers) - [DNS](#dns) - [IDP / SSO Integration](#idp--sso-integration) - [API & Automation](#api--automation) - [Monitoring](#monitoring) - [Production Tips](#production-tips) - [Netbird vs Netmaker vs Headscale](#netbird-vs-netmaker-vs-headscale) - [Tips & Pitfalls](#tips--pitfalls)
---

# Netbird — Self-Hosted WireGuard Mesh VPN with SSO

> **Last updated:** 2026-07-05
> **Repo:** [netbirdio/netbird](https://github.com/netbirdio/netbird) ⭐ 12k+
> **Language:** Go
> **License:** BSD 3-Clause
> **Docs:** https://docs.netbird.io
> **Website:** https://netbird.io

**Netbird** (formerly Wiretrustee / Netbird) is a **zero-configuration WireGuard mesh VPN** platform. It connects machines into a secure overlay network with automatic peer discovery, NAT traversal, and encryption — all self-hosted.

What sets Netbird apart: **reliable NAT traversal** (uses a dedicated TURN relay), **SSO/OIDC integration** out of the box, and **group-based access policies** for fine-grained network segmentation.

## Table of Contents

- [Overview](#overview)
  - [Architecture Components](#architecture-components)
- [Key Features](#key-features)
- [Requirements](#requirements)
  - [Server (Management + Signal + Dashboard)](#server-management--signal--dashboard)
  - [TURN Relay](#turn-relay-optional--recommended)
  - [Client (Each Node)](#client-each-node)
- [Installation (Self-Hosted)](#installation-self-hosted)
  - [All-in-One](#option-a-all-in-one-recommended)
  - [Configure Environment](#1-configure-environment)
  - [Configure Management Server](#2-configure-management-server)
  - [Start Services](#3-start-services)
  - [Access Dashboard](#5-access-dashboard)
- [Quick Start](#quick-start)
  - [Generate a Setup Key](#step-1-generate-a-setup-key)
  - [Install & Join](#step-2-install--join-a-node)
- [Joining Nodes](#joining-nodes)
  - [Linux](#linux-all-distros)
  - [Docker](#docker)
  - [macOS](#macos)
  - [Raspberry Pi / ARM](#raspberry-pi--arm)
- [Groups & Policies](#groups--policies)
  - [Groups](#groups)
  - [Policies (Flow Rules)](#policies-flow-rules)
- [Routing Peers](#routing-peers)
- [DNS](#dns)
  - [Internal DNS](#internal-dns)
  - [Split DNS](#split-dns)
- [IDP / SSO Integration](#idp--sso-integration)
  - [Authentik](#authentik)
  - [Google Workspace](#google-workspace)
  - [GitHub](#github)
- [API & Automation](#api--automation)
  - [Key Endpoints](#key-endpoints)
- [Monitoring](#monitoring)
  - [Prometheus Metrics](#prometheus-metrics)
  - [Health Check](#health-check)
- [Production Tips](#production-tips)
  - [Domain Must Be HTTPS](#domain-must-be-https)
  - [Persistent Storage](#persistent-storage)
  - [Database](#database)
  - [TURN Security](#turn-security)
- [Netbird vs Netmaker vs Headscale](#netbird-vs-netmaker-vs-headscale)
- [Tips & Pitfalls](#tips--pitfalls)

---

## Overview

```
           ┌──────────────────────────┐
           │    Management Server      │
           │  + Dashboard (optional)   │
           │  (VPS — public)           │
           └──────┬───────────────────┘
                  │ Control Plane
        ┌─────────┼─────────┬──────────┐
        ▼         ▼         ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
   │ Mini PC│ │  VPS 1 │ │  VPS 2 │ │  VPS 3 │
   │ (rumah)│ │(server)│ │(server)│ │(server)│
   │10.x.x.1│ │10.x.x.2│ │10.x.x.3│ │10.x.x.4│
   └────────┘ └────────┘ └────────┘ └────────┘
       │           │           │           │
       └───────────┼───────────┼───────────┘
                  Mesh P2P
             (WireGuard tunnels)
         ╔══════════════════════╗
         ║  TURN Relay          ║ ← only when P2P fails
         ║  (also self-hosted)  ║
         ╚══════════════════════╝
```

### Architecture Components

Netbird has **4 main components** that can be self-hosted:

| Component | Purpose | Default Address |
|-----------|---------|----------------|
| **Management Server** | Auth, peer coordination, config distribution | `:443` (gRPC + REST) |
| **Signal Server** | ICE signaling for NAT traversal | `:443` (WebSocket) |
| **TURN Relay** | Relay traffic when P2P fails | `:3478` UDP/TCP |
| **Dashboard** | Web UI for managing peers, groups, policies | `:443` (separate container) |

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Zero-Config Mesh** | Join a node — it automatically discovers and connects to peers |
| **NAT Traversal** | ICE + STUN + TURN — works behind CGNAT, symmetric NAT |
| **SSO / IDP** | Native OIDC integration (Google, Azure, GitHub, Authentik, etc.) |
| **Groups & Policies** | Organize peers into groups, define flow rules between them |
| **Routing Peers** | Route traffic to external networks (home LAN, VPC, etc.) |
| **DNS** | Internal DNS + split DNS (route specific domains via the mesh) |
| **Web UI** | Dashboard for managing network, peers, and policies |
| **REST API** | Full API for automation |
| **Activity Log** | Audit trail of peer connections and disconnections |
| **Multi-Network** | Separate networks per environment |
| **FIDO2 / WebAuthn** | Hardware key support for dashboard login |
| **Prometheus Metrics** | Built-in metrics endpoint |

---

## Requirements

### Server (Management + Signal + Dashboard)

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| CPU | 2 vCPU | 4 vCPU |
| RAM | 2 GB | 4 GB |
| Disk | 10 GB | 20 GB |
| Docker | 24+ | Latest |
| Domain | Required | For TLS + SSO callbacks |

**Open Ports:**

| Port | Protocol | Purpose |
|------|----------|---------|
| 443 | TCP (gRPC + REST) | Management + Signal + Dashboard API |
| 80 | TCP | Let's Encrypt HTTP challenge |
| 3478 | TCP/UDP | TURN relay |

> Port 443 serves both gRPC (netbird client ↔ management) and HTTP (dashboard) — multiplexed via a reverse proxy or Netbird's built-in HTTP/gRPC split.

### TURN Relay (Optional — Recommended)

| Requirement | Value |
|-------------|-------|
| CPU | 1 vCPU |
| RAM | 512 MB |
| Open Ports | `3478` TCP/UDP |

- Can run on the same server as management
- Only used when P2P direct connection fails (symmetric NAT, strict firewalls)

### Client (Each Node)

- Linux, macOS, Windows, FreeBSD, Docker, Router (OpenWrt)
- Outbound HTTPS to management server
- No ports need to be open

---

## Installation (Self-Hosted)

### Option A: All-in-One (Recommended)

```bash
git clone https://github.com/netbirdio/netbird.git
cd netbird/infrastructure_files

# Copy example config
cp docker-compose.yml.example docker-compose.yml
cp management.json.example management.json
cp turnserver.conf.example turnserver.conf
```

### Option B: Official Compose

Netbird provides a pre-configured `docker-compose.yml` with all components:

```bash
wget https://raw.githubusercontent.com/netbirdio/netbird/main/docker-compose.yml
wget https://raw.githubusercontent.com/netbirdio/netbird/main/docker-compose.management.yml
wget https://raw.githubusercontent.com/netbirdio/netbird/main/docker-compose.dashboard.yml
```

### 1. Configure Environment

Create `.env`:

```env
NETBIRD_DOMAIN=netbird.example.com
NETBIRD_MGMT_API_ENDPOINT=https://netbird.example.com
NETBIRD_MGMT_DATA_DIR=/var/lib/netbird
NETBIRD_SIGNAL_ENDPOINT=https://netbird.example.com
NETBIRD_TURN_ENDPOINT=turn:netbird.example.com:3478
NETBIRD_TURN_USERNAME=netbird
NETBIRD_TURN_PASSWORD=your-turn-password

# For Let's Encrypt
NETBIRD_LETSENCRYPT_EMAIL=admin@example.com

# For SSO / OIDC (optional — configure later)
NETBIRD_AUTH_OIDC_CONFIGURATION_ENDPOINT=https://auth.example.com/.well-known/openid-configuration
NETBIRD_AUTH_CLIENT_ID=netbird-client-id
NETBIRD_AUTH_CLIENT_SECRET=netbird-client-secret
```

### 2. Configure Management Server

Edit `management.json`:

```json
{
  "HttpConfig": {
    "Address": ":443",
    "AuthAudience": "netbird.example.com",
    "AuthIssuer": "https://auth.example.com/application/o/netbird/",
    "AuthClientID": "netbird-client-id",
    "AuthClientSecret": "netbird-client-secret",
    "AuthKeysLocation": "/var/lib/netbird/auth-keys.json",
    "IdpManagerType": "none",
    "IdpSignKeyRefreshEnabled": false
  },
  "Datadir": "/var/lib/netbird",
  "DeviceAuthorizationFlow": {
    "Provider": "hosted"
  },
  "TurnConfig": {
    "TURNHost": "netbird.example.com",
    "TURNUser": "netbird",
    "TWOPass": "your-turn-password"
  }
}
```

### 3. Start Services

```bash
# Without dashboard (CLI-only management)
docker compose -f docker-compose.yml -f docker-compose.management.yml up -d

# With dashboard (recommended)
docker compose -f docker-compose.yml -f docker-compose.management.yml -f docker-compose.dashboard.yml up -d
```

### 4. Verify

```bash
docker compose ps
# Expected: coturn, netbird-mgmt, netbird-signal, netbird-dashboard (maybe), certbot (maybe)

# Check management logs
docker compose logs netbird-mgmt | tail -10
# Look for: "server started"
```

### 5. Access Dashboard

```
https://netbird.example.com
```

First login requires SSO/OIDC set up. If no SSO configured, Netbird uses setup keys for initial node joining.

---

## Quick Start

### Step 1: Generate a Setup Key

```bash
# Via API (replace TOKEN first)
curl -X POST https://netbird.example.com/api/setup-keys \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "initial-key",
    "type": "reusable",
    "expires_in": "720h",
    "auto_groups": ["all"]
  }'
```

Or via Dashboard → Setup Keys → Create Key.

### Step 2: Install & Join a Node

```bash
# Linux
curl -fsSL https://github.com/netbirdio/netbird/releases/latest/download/netbird_linux_x86_64.tar.gz | tar xz
sudo mv netbird /usr/local/bin/

# Join
sudo netbird up --management-url https://netbird.example.com --setup-key YOUR_SETUP_KEY
```

### Step 3: Verify

```bash
# Check status
sudo netbird status

# List peers
sudo netbird peers

# Ping another node
ping 10.x.x.2
```

---

## Joining Nodes

### Linux (All Distros)

```bash
# Install
sudo apt install netbird  # Debian/Ubuntu
sudo dnf install netbird  # Fedora/RHEL
# OR download from GitHub releases

# Join
sudo netbird up \
  --management-url https://netbird.example.com \
  --setup-key YOUR_KEY

# Persist config (so it reconnects on reboot)
sudo netbird service install
sudo netbird service start

# Check interface
ip link show wt0
```

### Docker

```yaml
services:
  netbird:
    image: netbirdio/netbird:latest
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    devices:
      - /dev/net/tun
    volumes:
      - ./netbird-client:/etc/netbird
    command: up --management-url https://netbird.example.com --setup-key YOUR_KEY
```

### macOS

```bash
# Homebrew
brew install netbirdio/tap/netbird

# Join
sudo netbird up --management-url https://netbird.example.com --setup-key YOUR_KEY
```

### Raspberry Pi / ARM

```bash
curl -fsSL https://github.com/netbirdio/netbird/releases/latest/download/netbird_linux_arm64.tar.gz | tar xz
sudo mv netbird /usr/local/bin/
sudo netbird up --management-url https://netbird.example.com --setup-key YOUR_KEY
```

---

## Groups & Policies

Netbird's **Groups** and **Policies** are its most powerful feature — they control which peers can communicate.

### Groups

Organize peers by function or environment:

```bash
# Create group via CLI (on management server)
netbird group add web-servers
netbird group add databases
netbird group add dev

# Add peer to group (via API or dashboard)
# Dashboard → Peers → Select peer → Groups → Add
```

### Policies (Flow Rules)

Define traffic rules between groups:

| Source Group | Destination Group | Port | Protocol |
|-------------|-------------------|------|----------|
| `dev` | `databases` | 5432 | TCP |
| `monitoring` | `all` | 9100 | TCP |
| `web-servers` | `internet` | * | * |

Configure via Dashboard → Policies → Create Policy:

| Setting | Example |
|---------|---------|
| Name | `dev-db-access` |
| Description | Allow dev team to access databases |
| Source | `dev` |
| Destination | `databases` |
| Port | `5432,3306` |
| Protocol | `TCP` |
| Action | `Allow` |

### Default Policy

The default `allow-all` policy can be disabled for zero-trust:

```json
{
  "DefaultPolicy": "deny"
}
```

Then explicitly create policies for each allowed communication path.

---

## Routing Peers

Netbird's routing peers are analogous to Netmaker's egress gateways — they route traffic from the mesh to external networks.

Use case: All mesh nodes can access 192.168.1.0/24 (home LAN) through the mini PC.

### Setup

1. **Dashboard → Routing Peers → Create**
2. Configure:

| Setting | Example |
|---------|---------|
| Peer | `mini-pc` |
| Network Range | `192.168.1.0/24` |
| Metric | `10` (lower = preferred) |
| Distribution Group | `all` (or specific group) |

3. Enable IP forwarding on the routing peer:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
# Make permanent
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

# If behind NAT, add NAT rule
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Result

```
VPS Node (10.x.x.2) ──► 192.168.1.50 (home NAS)
               │
               │ via routing peer
               ▼
         mini-pc (routing peer)
               │
               ▼
       192.168.1.0/24 (home LAN)
```

### Verification

```bash
# From any mesh node
ping 192.168.1.50  # Should route through mini-pc
```

---

## DNS

Netbird provides built-in DNS with two modes:

### Internal DNS

Each peer gets a DNS name:

```
<peer-name>.netbird.cloud
```

Example:

```
web-01.netbird.cloud  →  10.x.x.5
db-01.netbird.cloud   →  10.x.x.6
```

### Split DNS

Route specific domains through the mesh:

Configure in Dashboard → DNS → Create Nameserver Group:

| Setting | Example |
|---------|---------|
| Name | `internal-dns` |
| Nameserver | `192.168.1.1` |
| Domains | `*.internal.example.com,*.corp` |
| Distribution Group | `all` |

Now any mesh node querying `*.internal.example.com` gets routed through the mesh to `192.168.1.1`.

---

## IDP / SSO Integration

Netbird shines here — it supports **any OIDC provider** natively.

### Authentik

1. Create an OIDC provider in Authentik:

```
Provider Type: OAuth2/OpenID Provider
Client ID: netbird
Client Secret: generate
Redirect URIs: https://netbird.example.com/auth/callback
Signing Key: any RSA key
```

2. Create an application in Authentik linked to that provider.

3. Configure Netbird `.env`:

```env
NETBIRD_AUTH_OIDC_CONFIGURATION_ENDPOINT=https://auth.example.com/application/o/netbird/.well-known/openid-configuration
NETBIRD_AUTH_CLIENT_ID=netbird
NETBIRD_AUTH_CLIENT_SECRET=your-client-secret
```

4. Recreate containers:

```bash
docker compose up -d
```

### Google Workspace

```env
NETBIRD_AUTH_OIDC_CONFIGURATION_ENDPOINT=https://accounts.google.com/.well-known/openid-configuration
NETBIRD_AUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
NETBIRD_AUTH_CLIENT_SECRET=your-google-client-secret
```

### GitHub

```env
NETBIRD_AUTH_OIDC_CONFIGURATION_ENDPOINT=https://token.actions.githubusercontent.com/.well-known/openid-configuration
NETBIRD_AUTH_CLIENT_ID=your-github-app-client-id
NETBIRD_AUTH_CLIENT_SECRET=your-github-app-client-secret
```

---

## API & Automation

### Authentication

```bash
# Get API token (via dashboard)
# Dashboard → Personal Access Tokens → Create

TOKEN="your-pat-token"
API="https://netbird.example.com/api"
```

### Key Endpoints

```bash
# List peers
curl -H "Authorization: Bearer $TOKEN" \
  $API/peers

# List groups
curl -H "Authorization: Bearer $TOKEN" \
  $API/groups

# Create setup key
curl -X POST $API/setup-keys \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auto-provision",
    "type": "reusable",
    "expires_in": "8760h",
    "auto_groups": ["all"]
  }'

# Create group
curl -X POST $API/groups \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "web-servers"}'

# Create policy
curl -X POST $API/policies \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dev-db-access",
    "description": "Allow dev to access databases",
    "enabled": true,
    "rules": [{
      "source": ["dev"],
      "destination": ["databases"],
      "ports": ["5432", "3306"],
      "protocol": "tcp",
      "action": "allow"
    }]
  }'
```

### Automation Script

```bash
#!/bin/bash
# Auto-provision a new VPS into Netbird mesh

API="https://netbird.example.com/api"
TOKEN="your-pat-token"
NEW_VPS_IP="$1"
NEW_VPS_NAME="$2"

# Generate a one-time setup key
KEY=$(curl -s -X POST "$API/setup-keys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "provision-'$NEW_VPS_NAME'",
    "type": "one-off",
    "expires_in": "1h",
    "auto_groups": ["all"]
  }' | jq -r '.key')

# Join via SSH
ssh "root@$NEW_VPS_IP" "
  curl -fsSL https://github.com/netbirdio/netbird/releases/latest/download/netbird_linux_x86_64.tar.gz | tar -xz
  mv netbird /usr/local/bin/
  netbird up --management-url $API --setup-key $KEY
  netbird service install
  netbird service start
"
```

---

## Monitoring

### Prometheus Metrics

Netbird management server exposes metrics:

```bash
curl https://netbird.example.com/metrics
```

Key metrics:
- `netbird_peers_online` — connected peers count
- `netbird_peers_offline` — disconnected peers
- `netbird_traffic_bytes` — bytes transferred

### Health Check

```bash
curl https://netbird.example.com/health
# {"status":"OK"}
```

### Grafana

Import community dashboards or create your own from the metrics.

---

## Production Tips

### Domain Must Be HTTPS

Netbird requires HTTPS for the management server. Use:

- **Let's Encrypt** (built-in certbot in the compose stack)
- **Reverse proxy** (Caddy, Nginx, Traefik)
- **Cloudflare Tunnel** (if behind strict firewall)

### Persistent Storage

Mount volumes for:

```yaml
volumes:
  - netbird-mgmt:/var/lib/netbird    # Database + config
  - netbird-signal:/var/lib/netbird  # Signal data
  - netbird-dashboard:/var/lib/netbird-dashboard  # Dashboard data
```

### Database

Netbird uses SQLite by default. For multi-server HA, can use PostgreSQL but requires custom config.

Backup:

```bash
# SQLite backup
docker compose exec netbird-mgmt cp /var/lib/netbird/store.db /tmp/backup.db
docker compose cp netbird-mgmt:/tmp/backup.db ./backup-$(date +%F).db
```

### TURN Security

Restrict TURN access:

```conf
# turnserver.conf
fingerprint
lt-cred-mech
user=netbird:your-turn-password
realm=netbird.example.com
```

Rotate TURN credentials regularly.

---

## Netbird vs Netmaker vs Headscale

| Feature | Netbird | Netmaker | Headscale |
|---------|:-------:|:--------:|:---------:|
| **NAT Traversal** | ✅✅ **Best** (with TURN) | ✅ Good (STUN/relay) | ✅ Good (DERP relay) |
| **SSO / IDP** | ✅✅ **Native + rich** | 🔶 Limited | ✅ OIDC supported |
| **Groups & ACL** | ✅✅ **Groups + policies** | ✅ Node/group ACL | ✅ ACL policies |
| **Web UI** | ✅ Separate dashboard | ✅ Full dashboard | 🔶 Optional |
| **Network Graph** | ❌ | ✅ Real-time | ❌ |
| **Ingress Gateway** | ❌ (needs reverse proxy) | ✅ Built-in | ✅ Subnet routing |
| **Egress / Routing** | ✅ Routing Peers | ✅ Egress Gateway | ✅ Subnet routing |
| **Split DNS** | ✅ Yes | ❌ | ✅ MagicDNS |
| **Client** | `netbird` binary | `netclient` binary | Standard `tailscale` |
| **Server Resources** | ~1GB | ~1GB | ~200MB |
| **Setup Complexity** | Medium | Medium | Low |
| **Stability** | ✅ Very stable | ⚠️ Occasional breaking | ✅ Very stable |
| **License** | BSD 3-Clause | MIT | BSD 3-Clause |
| **Client Auto-Update** | ✅ Built-in | ✅ Built-in | Requires agent |
| **FIDO2 / WebAuthn** | ✅ Dashboard | ❌ | ❌ |
| **Activity Log** | ✅ Rich audit | Basic | Via webhook |

### When to Choose Each

**Netbird** → You need reliable NAT traversal for nodes behind CGNAT/symmetric NAT, want SSO/OIDC integration, prefer group-based access policies, and value stability

**Netmaker** → You want a visual dashboard with network graph, need built-in ingress/egress gateways, manage 5-10+ nodes, and don't mind occasional maintenance

**Headscale** → You want the lightest setup, are CLI-native, have 2-10 nodes, and prefer using the standard Tailscale client

---

## Tips & Pitfalls

### ✅ Use TURN on a Different Port

By default TURN uses 3478. If you run Coturn on the same server as management, don't conflict:

```env
NETBIRD_TURN_ENDPOINT=turn:netbird.example.com:3478
```

### ✅ Set Up SSO First

Netbird without SSO requires managing API tokens and setup keys. Configure OIDC early — it's much easier to manage users.

### ✅ Use Reusable Setup Keys

For lab/experimental nodes:

```bash
# Key that lasts 1 year and can be used 50 times
curl -X POST ... -d '{
  "name": "long-term",
  "type": "reusable",
  "expires_in": "8760h",
  "max_uses": 50,
  "auto_groups": ["all"]
}'
```

### ❌ TURN Not Working

If P2P connections fail and traffic isn't relayed:

- Check port 3478 UDP is open
- Verify TURN credentials in management.json match turnserver.conf
- Test with `netbird up --relay-address turn:netbird.example.com:3478`
- Check Coturn logs: `docker compose logs coturn`

### ❌ Clock Skew Issues

Netbird uses JWT tokens. If a node's clock is off:

```bash
# Fix with NTP
sudo timedatectl set-ntp true
sudo apt install ntp
```

### ❌ DNS Conflicts with Local Resolution

If `wt0` interface affects your existing DNS:

```bash
# Disable Netbird DNS management
sudo netbird up --dns-resolver-disable
```

### ❌ Management Server Behind Reverse Proxy

Netbird management uses gRPC which needs special proxy config:

**Nginx:**

```nginx
server {
    listen 443 ssl;
    server_name netbird.example.com;

    # Dashboard
    location / {
        proxy_pass http://netbird-dashboard:80;
    }

    # Signal (WebSocket)
    location /signal {
        proxy_pass http://netbird-signal:10000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Management (gRPC)
    location /management {
        grpc_pass grpc://netbird-mgmt:443;
        # Requires nginx grpc module
    }
}
```

### ❌ Node Shows Offline

- Management server reachable? → `curl https://netbird.example.com/health`
- Signal server reachable? → outbound WS to port 443 should work
- Check firewall: outbound HTTPS must be allowed
- Restart the node: `sudo netbird service stop && sudo netbird service start`

### ❌ Upgrade Issues

Netbird has a clean upgrade path between versions:

```bash
# Pull new images
docker compose pull

# Recreate containers
docker compose up -d

# Update clients
sudo netbird up --update  # on each client
```
