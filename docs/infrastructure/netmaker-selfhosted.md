---
title: Netmaker — Self-Hosted WireGuard Mesh VPN Platform
description: - [Overview](#overview) - [Architecture](#architecture) - [Key Features](#key-features) - [Requirements](#requirements) - [Installation](#installation) - [Configuration](#configuration) - [Joining Nodes](#joining-nodes) - [Networks & Mesh](#networks--mesh) - [Ingress Gateway](#ingress-gateway) - [Egress Gateway](#egress-gateway) - [ACL](#acls-acl) - [DNS](#dns) - [API & Automation](#api--automation) - [Production Setup](#production-setup) - [Monitoring](#monitoring) - [Netmaker vs Netbird vs Headscale](#netmaker-vs-netbird-vs-headscale) - [Tips & Pitfalls](#tips--pitfalls)
---

# Netmaker — Self-Hosted WireGuard Mesh VPN Platform

> **Last updated:** 2026-07-05
> **Repo:** [gravitl/netmaker](https://github.com/gravitl/netmaker) ⭐ 10k+
> **Language:** Go
> **License:** MIT
> **Docs:** https://docs.netmaker.org

**Netmaker** is a platform for creating and managing **WireGuard mesh networks** — fully self-hosted. It lets you connect any number of machines (VPS, mini PCs, Raspberry Pis, cloud servers) into a secure overlay network with automatic WireGuard configuration, mesh topology, and a web UI.

Each node gets a private IP and can communicate with every other node directly (P2P) or via relay — all encrypted with WireGuard.

---

## Overview

```
           ┌──────────────────────────┐
           │    Netmaker Server        │
           │  (VPS — public accessible)│
           │  Docker Compose stack     │
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
```

Netmaker handles the **orchestration** — you don't manually write `wg0.conf` files. You define a network, generate an enrollment key or token, install `netclient` on each node, and join them. The server pushes WireGuard configs, manages key rotation, and monitors status.

### How It Works

1. **Netmaker Server** runs the control plane (API + UI + broker)
2. Each node runs **Netclient** — an agent that talks to the server
3. When a node joins, the server generates WireGuard keys, assigns private IPs, and distributes peer configs
4. Nodes connect directly P2P where possible (via STUN/ICE NAT traversal)
5. If direct connection fails (symmetric NAT), traffic routes through a relay node
6. All control traffic is gRPC; data plane is standard WireGuard

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Mesh VPN** | Every node can reach every other node via WireGuard |
| **Auto NAT Traversal** | STUN/ICE — direct P2P when possible, relay fallback |
| **Web UI** | Dashboard with network graph, node status, traffic |
| **Ingress Gateway** | Expose internal services to the internet via the server |
| **Egress Gateway** | Route traffic from the mesh to external networks (e.g., LAN) |
| **DNS** | Internal name resolution (`node-name.netmaker`) |
| **ACL** | Access control lists — restrict which nodes talk to which |
| **API** | Full REST API — automate provisioning |
| **Multi-Network** | Create separate networks per environment (dev/staging/prod) |
| **Hub & Spoke** | Alternative to full mesh — hub routes between spokes |
| **Metrics** | Prometheus metrics endpoint |
| **Relay** | Automatic relay for nodes that can't establish P2P |
| **Failover** | Multi-server HA configuration |
| **SSO** | OAuth / OIDC integration for the web UI |

---

## Requirements

### Server

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| CPU | 2 vCPU | 4 vCPU |
| RAM | 2 GB | 4 GB |
| Disk | 20 GB | 40 GB (SSD) |
| Docker | 24+ | Latest |
| Domain | Required for UI/API | — |

**Open Ports:**

| Port | Protocol | Purpose |
|------|----------|---------|
| 443 | TCP | Web UI + REST API (HTTPS) |
| 51821 | UDP | WireGuard listener |
| 51822 | TCP | gRPC (agent ↔ server) |

### Client (each node)

- Linux (x86_64, arm64, armv7), macOS, Windows, FreeBSD
- Outbound internet access to the Netmaker server
- No ports need to be open behind NAT
- `netclient` binary (~15 MB)

---

## Installation

### 1. Clone & Configure

```bash
git clone https://github.com/gravitl/netmaker.git
cd netmaker
cp docker-compose.yml docker-compose.yml.backup
```

### 2. Environment Variables

Create `.env`:

```env
SERVER_HOST=netmaker.example.com
SERVER_HTTP_HOST=netmaker.example.com
API_PORT=443
GRPC_PORT=51822
WIREGUARD_PORT=51821
MASTER_KEY=your-strong-master-key-at-least-32-chars
NETCLIENT_AUTO_UPDATE=true
DNS_MODE=on
```

> **Server Host:** Must be a domain pointing to your VPS. IP-only will break TLS.

### 3. Start the Stack

```bash
docker compose up -d
```

This starts:
- **netmaker** — main API + controller
- **netmaker-ui** — web frontend (React)
- **mq** — message broker (NATS or RabbitMQ)
- **postgresql** — database

Verify:

```bash
docker compose ps
# All containers should be "Up"
docker compose logs netmaker | tail -5
# Look for: "server started" or similar
```

### 4. Access Web UI

```
https://netmaker.example.com
```

First login uses **Master Key** from `.env`:
- Navigate to `https://netmaker.example.com`
- Enter Master Key as password (default user: `admin` or any username)
- Or configure SSO/OIDC

---

## Configuration

### Network Creation

1. **Web UI → Networks → Create Network**
2. Network settings:

| Setting | Example | Notes |
|---------|---------|-------|
| Name | `homelab` | Lowercase, no spaces |
| Address Range | `10.10.0.0/16` | Private IP range for mesh nodes |
| Default ACL | `allow` or `deny` | Default: all nodes can talk |
| Is Mesh | `true` | Full mesh vs hub & spoke |

3. Click **Save** — the network now exists
4. Go to **Enrollment Keys** tab → generate a new key

### Enrollment Key

```json
{
  "key": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "networks": ["homelab"],
  "uses": 50,
  "expiration": "2026-12-31T23:59:59Z",
  "tags": ["production"]
}
```

- **uses:** How many nodes can join with this key (0 = unlimited)
- **expiration:** Auto-expire the key
- **tags:** Optional metadata

---

## Joining Nodes

### Linux (x86_64, ARM)

```bash
# Install netclient
curl -sfL https://raw.githubusercontent.com/gravitl/netclient/master/install.sh | sudo bash

# Join network
sudo netclient join -t a1b2c3d4-e5f6-7890-abcd-ef1234567890

# Verify
sudo wg show
sudo netclient list
```

### Docker (any Linux)

```bash
docker run -d \
  --name netclient \
  --cap-add NET_ADMIN \
  --device /dev/net/tun \
  -v /etc/netclient:/etc/netclient \
  gravitl/netclient:latest \
  join -t YOUR_TOKEN
```

### macOS

```bash
# Homebrew
brew install gravitl/netclient/netclient

# Join
sudo netclient join -t YOUR_TOKEN

# Note: requires System Extension approval on first run
```

### Windows

1. Download `netclient.exe` from releases
2. Run as Administrator:
```
netclient.exe join -t YOUR_TOKEN
```

### Verification

```bash
# Check node list via CLI
sudo netclient list

# Check WireGuard interface
sudo wg show
# Should show interface "nm-*" with peers

# Ping another node
ping 10.10.0.2
```

---

## Networks & Mesh

### Full Mesh (Default)

All nodes connect to all other nodes:

```
Node A ◄────► Node B
  ▲              ▲
  │              │
  ▼              ▼
Node C ◄────► Node D
```

Pros: Lowest latency, no single point of failure
Cons: N² connections, higher overhead with 20+ nodes

### Hub & Spoke

One hub node routes all traffic:

```
        Node A
        │
        ▼
     ┌──────┐
     │ HUB  │
     └──────┘
        ▲
        │
        ▼
     Node B     Node C
```

Pros: Predictable traffic flow, simpler ACL
Cons: Hub becomes bottleneck

Configure in **Network Settings → Is Mesh → false**, then designate hub nodes.

### Multi-Network

Create separate networks for isolation:

```yaml
# homelab — home servers + mini PC
# staging — VPS staging environment
# production — VPS production servers
```

Nodes can belong to multiple networks.

---

## Ingress Gateway

Expose a port from one mesh node to the **internet** through the Netmaker server.

Use case: Expose a web app running on your mini PC (behind NAT) to the public internet.

### Setup (Web UI)

1. **Networks → Select Network → Ingress Gateways → Create**
2. Choose the mesh node that hosts the service (e.g., `mini-pc`)
3. Configure port mapping:

| Setting | Example |
|---------|---------|
| Listener Port | 8080 |
| Target Node | `mini-pc` |
| Target Port | 3000 |
| Protocol | TCP |

4. Save → Netmaker opens port `8080` on the server and forwards traffic to `mini-pc:3000`

### Result

```
Internet ──► netmaker.example.com:8080
                    │
                (Ingress)
                    │
              ▼
          mini-pc:3000
       (behind NAT, no open ports)
```

### Via API

```bash
curl -X POST https://netmaker.example.com/api/networks/homelab/ingress \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "node_id": "mini-pc",
    "port": 8080,
    "target_port": 3000,
    "protocol": "tcp"
  }'
```

---

## Egress Gateway

Let mesh nodes access services on an **external network** (your home LAN, a cloud VPC, etc.) through a designated egress node.

Use case: All VPS nodes can reach devices on your home network (192.168.1.0/24) through the mini PC.

### Setup (CLI on the node)

On the node that will act as egress (e.g., mini PC with access to `192.168.1.0/24`):

```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1

# Add egress range via netclient
sudo netclient egw add --range 192.168.1.0/24
```

### Result

```
VPS Node (10.10.0.2) ──► 192.168.1.10 (home NAS)
               │
               │ via egress
               ▼
    mini-pc (egress gateway)
               │
               ▼
       192.168.1.0/24 (home LAN)
```

### Verification

```bash
# From any mesh node
ping 192.168.1.10   # Should reach home NAS through egress
```

### Via Web UI

1. **Networks → Select Network → Egress Gateways → Create**
2. Choose the node
3. Enter CIDR ranges (e.g., `192.168.1.0/24,10.0.0.0/8`)

---

## ACL (Access Control)

Control which nodes can communicate within the mesh.

### Default Modes

- **Allow All:** Any node can talk to any node (default)
- **Deny All:** No inter-node communication unless explicitly allowed

### Configure (Web UI)

1. **Networks → Select Network → ACL → Manage**
2. Create rules:

| Source | Destination | Action |
|--------|-------------|--------|
| `group:web-servers` | `group:databases` | Allow |
| `node:backup-server` | `*` | Allow |
| `group:dev-nodes` | `group:prod-nodes` | Deny |

### Groups

Group nodes by function:

```bash
# Tag nodes
sudo netclient tag add database
sudo netclient tag add web-server

# Then create ACL rules per group
```

---

## DNS

Netmaker provides internal DNS resolution.

### Default Behavior

Each node gets a DNS name:

```
<node-name>.<network-name>.netmaker
```

Example:

```
web-01.homelab.netmaker  →  10.10.0.5
db-01.homelab.netmaker   →  10.10.0.6
backup.homelab.netmaker   →  10.10.0.7
```

### Configure DNS Server

On each node, the DNS mode must be enabled:

```bash
# Check current setting
sudo netclient info

# Enable DNS
# Edit /etc/netclient/config.toml → set dns = "on"
# Then restart netclient
sudo netclient service restart
```

### Custom DNS Entries

Via API:

```bash
curl -X POST https://netmaker.example.com/api/dns \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "myapp", "address": "10.10.0.5"}'
```

Now `myapp` resolves to that node.

---

## API & Automation

### Authentication

```bash
# Get a token
TOKEN=$(curl -s -X POST https://netmaker.example.com/api/users/admin/login \
  -H "Content-Type: application/json" \
  -d '{"password": "'$MASTER_KEY'"}' | jq -r '.token')
```

### Key Endpoints

```bash
# List networks
curl -H "Authorization: Bearer $TOKEN" \
  https://netmaker.example.com/api/networks

# List nodes
curl -H "Authorization: Bearer $TOKEN" \
  https://netmaker.example.com/api/nodes

# Create enrollment key
curl -X POST https://netmaker.example.com/api/enrollment-keys \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "networks": ["homelab"],
    "uses": 10,
    "expiration": "2027-01-01T00:00:00Z"
  }'

# Delete a node
curl -X DELETE https://netmaker.example.com/api/nodes/NODE_ID \
  -H "Authorization: Bearer $TOKEN"

# Get metrics
curl -H "Authorization: Bearer $TOKEN" \
  https://netmaker.example.com/api/nodes/NODE_ID/metrics
```

### Automation Script

```bash
#!/bin/bash
# Provision a new VPS into the mesh

TOKEN="your-api-token"
SERVER="https://netmaker.example.com"
VPS_IP="$1"
VPS_NAME="$2"

# Generate enrollment key
KEY=$(curl -s -X POST "$SERVER/api/enrollment-keys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"networks": ["homelab"], "uses": 1}' | jq -r '.key')

# SSH into the new VPS and join
ssh "root@$VPS_IP" "
  curl -sfL https://raw.githubusercontent.com/gravitl/netclient/master/install.sh | bash
  sudo netclient join -t $KEY
"
```

---

## Production Setup

### TLS with Let's Encrypt

Use a reverse proxy (Caddy, Traefik, Nginx) in front of Netmaker:

```yaml
services:
  caddy:
    image: caddy:latest
    ports:
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data

  netmaker:
    expose:
      - "8081"
    # ... internal port, not public

  netmaker-ui:
    expose:
      - "80"
```

`Caddyfile`:

```caddyfile
netmaker.example.com {
    reverse_proxy netmaker:8081
}

netmaker.example.com /api/* {
    reverse_proxy netmaker:8081
}

# UI is served by netmaker-ui on port 80
# (Or integrated into netmaker:8081 in newer versions)
```

### Database

By default, Netmaker uses the bundled PostgreSQL. For production:

- Use a managed PostgreSQL (Cloud SQL, RDS, etc.)
- Or add persistent volume + regular backups

```bash
# Backup database
docker compose exec postgresql pg_dump -U netmaker netmaker > backup.sql

# Restore
docker compose exec -T postgresql psql -U netmaker netmaker < backup.sql
```

### SSO / OIDC

Configure in `.env`:

```env
# OIDC Settings
OIDC_ISSUER=https://auth.example.com/application/o/netmaker/
OIDC_CLIENT_ID=your-client-id
OIDC_CLIENT_SECRET=your-client-secret
OIDC_NAME=Authentik
```

Then in Web UI → Settings → SSO → Enable.

---

## Monitoring

### Built-in Metrics

Netmaker exposes Prometheus metrics:

```bash
curl http://localhost:8081/metrics
```

Configure Prometheus:

```yaml
scrape_configs:
  - job_name: 'netmaker'
    static_configs:
      - targets: ['netmaker.example.com:443']
    scheme: https
```

### Grafana Dashboard

Import the official Netmaker dashboard from [grafana.com](https://grafana.com/grafana/dashboards/) or use community dashboards.

### Health Check

```bash
# Check service health
curl https://netmaker.example.com/health

# Check node status via API
curl -H "Authorization: Bearer $TOKEN" \
  https://netmaker.example.com/api/nodes \
  | jq '.[] | {name: .name, status: .connected, address: .address}'
```

---

## Netmaker vs Netbird vs Headscale

| Feature | Netmaker | Netbird | Headscale |
|---------|:--------:|:-------:|:---------:|
| **Control Plane** | gRPC + REST | REST + gRPC | REST (gRPC planned) |
| **Web UI** | ✅ Full dashboard | ✅ Separate dashboard | 🔶 Optional (3rd party) |
| **Network Graph** | ✅ Real-time visual | ❌ | ❌ |
| **NAT Traversal** | STUN/ICE + relay | **TURN relay** (better) | STUN/ICE + DERP relay |
| **Ingress Gateway** | ✅ Built-in | ❌ (requires reverse proxy) | ✅ Subnet routing |
| **Egress Gateway** | ✅ Built-in | ✅ Routing Peers | ✅ Subnet routing |
| **DNS** | ✅ Internal | ✅ Internal + Split DNS | ✅ MagicDNS |
| **ACL** | ✅ Node/group ACL | ✅ Groups + Policies | ✅ ACL policies (Hujson) |
| **SSO / OIDC** | 🔶 Limited | ✅ Full (Google, Azure, OIDC) | ✅ OIDC supported |
| **Auto Join** | Enrollment keys | Pre-auth keys | Pre-auth keys |
| **Client CLI** | `netclient` | `netbird` | `tailscale` (standard) |
| **Resource Usage** | Medium (~1GB) | Medium (~1GB) | **Lowest** (~200MB) |
| **Stability** | Occasional breaking updates | More stable | Very stable |
| **Maturity** | Established | Mature | Mature |
| **License** | MIT | BSD 3-Clause | BSD 3-Clause |

### When to Choose Each

**Netmaker** → You want a visual dashboard, need ingress/egress gateways built-in, have 5-10+ nodes, and don't mind occasional maintenance

**Netbird** → You need reliable NAT traversal (symmetric NAT/CGNAT), want SSO integration, prefer stability over feature velocity

**Headscale** → You want something lightweight, are comfortable with CLI, have 2-10 nodes, and prefer the standard Tailscale client

---

## Tips & Pitfalls

### ✅ Use a Persistent Key

Netmaker generates WireGuard keys per node automatically — but for the server:

```bash
# Generate a persistent private key for the server
wg genkey | tee /etc/netmaker/wg.key
```

Add to `.env`:

```env
SERVER_WIREGUARD_KEY=content-of-wg-key-file
```

### ✅ Set Realistic Address Range

Use a `/16` for the network even with few nodes — leaves room for expansion:

```
10.10.0.0/16  ← good
10.10.0.0/24  ← too small, will need migration
```

### ✅ Enable Auto-Update

```env
NETCLIENT_AUTO_UPDATE=true
```

Keeps `netclient` up to date across all nodes.

### ❌ Don't Use IP as SERVER_HOST

Netmaker uses TLS certificates. Setting `SERVER_HOST` to an IP breaks certificate validation.

**Fix:** Use a domain with a DNS A record pointing to your server.

### ❌ WireGuard Port Collisions

If the server already has WireGuard running (e.g., for tailscale, another WG config), port 51821 will conflict.

**Fix:** Change `WIREGUARD_PORT` in `.env` and open the new port.

### ❌ Nodes Show Disconnected

Common causes:

- gRPC port (51822) blocked by firewall → open it
- Node clock out of sync → install NTP
- netclient version mismatch → run `sudo netclient update`
- Network changes require restart → `sudo netclient service restart`

### ❌ Ingress Gateway Not Working

- Ensure the target service is listening on `0.0.0.0` (not `127.0.0.1`)
- Check the node's firewall isn't blocking internal traffic
- Verify the target port in the ingress config matches the actual service port

### ❌ Database Connection Refused

PostgreSQL container restarts may lose data if not using persistent volume:

```yaml
volumes:
  - pgdata:/var/lib/postgresql/data
```

### ❌ Upgrade Considerations

Breaking changes between major versions are common:

```bash
# Before upgrading
docker compose down
docker compose pull
docker compose up -d

# Always check release notes:
# https://github.com/gravitl/netmaker/releases
```

Backup database first:

```bash
docker compose exec postgresql pg_dump -U netmaker netmaker > backup-$(date +%F).sql
```
