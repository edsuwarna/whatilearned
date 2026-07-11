---
title: WireGuard — Fast, Modern VPN Tunnel
description: - [Overview](#overview) - [Installation](#installation) - [Quick Start](#quick-start) - [Configuration Guide](#configuration-guide) - [Hub & Spoke Topology](#hub--spoke-topology) - [Site-to-Site](#site-to-site) - [NAT Traversal & Persistence](#nat-traversal--persistence) - [Advanced Config](#advanced-config) - [Monitoring & Debugging](#monitoring--debugging) - [Security](#security) - [Migration from OpenVPN](#migration-from-openvpn) - [Docker](#docker) - [Comparison](#comparison) - [Pitfalls](#pitfalls)
---

# WireGuard — Fast, Modern VPN Tunnel

> **Last updated:** 2026-07-05
> **Repo:** [WireGuard](https://www.wireguard.com) — built into Linux kernel (5.6+)
> **Language:** C (kernel module + userspace Go implementation)
> **License:** GPL v2 / MIT
> **Docs:** https://www.wireguard.com/quickstart

**WireGuard** is the most modern VPN protocol, now built directly into the Linux kernel. It's faster, simpler, and more secure than OpenVPN or IPsec — a single UDP port, modern cryptography (Curve25519, ChaCha20, BLAKE2s), and a codebase measured in thousands of lines instead of hundreds of thousands.

## Table of Contents

- [Overview](#overview)
  - [What Makes WireGuard Different](#what-makes-wireguard-different)
  - [Key Features](#key-features)
- [Installation](#installation)
  - [Linux (Kernel Module)](#linux-kernel-module)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Docker](#docker)
- [Quick Start](#quick-start)
  - [Generate Keys](#step-1-generate-keys)
  - [Create Config](#step-2-create-config)
  - [Start the Tunnel](#step-3-start-the-tunnel)
  - [Enable Auto-Start](#step-4-enable-auto-start)
- [Configuration Guide](#configuration-guide)
  - [Interface Section](#interface-section)
  - [Peer Section](#peer-section)
  - [AllowedIPs Deep Dive](#allowedips-deep-dive)
- [Hub & Spoke Topology](#hub--spoke-topology)
  - [Hub Config (VPS)](#hub-config-vps)
  - [Mini PC Config](#mini-pc-config)
  - [VPS Config](#vps-1-config)
- [Site-to-Site](#site-to-site)
  - [Home Gateway Config](#home-gateway-config)
  - [VPS Config (Accepting Home Traffic)](#vps-config-accepting-home-traffic)
- [NAT Traversal & Persistence](#nat-traversal--persistence)
  - [PersistentKeepalive](#persistentkeepalive)
  - [Firewall Rules](#firewall-rules)
  - [Behind CGNAT](#behind-cgnat)
- [Advanced Config](#advanced-config)
  - [Full Tunnel](#full-tunnel-all-traffic-through-vpn)
  - [Kill Switch](#kill-switch)
  - [Multi-Peer](#multi-peer-client-connects-to-multiple-servers)
  - [Pre-Shared Key](#pre-shared-key-psk)
  - [Custom MTU](#custom-mtu)
- [Monitoring & Debugging](#monitoring--debugging)
  - [Quick Status](#quick-status)
  - [Monitoring Script](#monitoring-script)
- [Security](#security)
  - [Best Practices](#best-practices)
- [Migration from OpenVPN](#migration-from-openvpn)
  - [Quick Comparison](#quick-comparison)
  - [Migration Steps](#migration-steps)
- [Docker](#docker)
  - [Server with Docker](#server-with-docker)
  - [Client in Docker](#client-in-docker)
- [Comparison](#comparison)
  - [WireGuard vs Other VPN Solutions](#wireguard-vs-other-vpn-solutions)
- [Pitfalls](#pitfalls)

---

## Overview

```
┌─────────────┐          UDP :51820          ┌─────────────┐
│   Peer A    │ ◄══════════════════════════► │   Peer B    │
│  10.0.0.1   │    Encrypted WireGuard       │  10.0.0.2   │
│  (NAT/Home) │         Tunnel               │  (VPS/Cloud)│
└─────────────┘                               └─────────────┘
```

### What Makes WireGuard Different

| Aspect | WireGuard | OpenVPN / IPsec |
|--------|-----------|-----------------|
| **Code size** | ~4,000 lines | 100,000+ lines |
| **Crypto** | Modern (Curve25519, ChaCha20, Poly1305, BLAKE2s) | Legacy / complex |
| **Transport** | Single UDP port | TCP or UDP, multiple ports |
| **Key management** | Public/private keys (static) | X.509 certificates, complex PKI |
| **Roaming** | Built-in — change IP, tunnel stays up | Needs reconnect |
| **Kernel integration** | In-kernel since 5.6 | Userspace (slow) |
| **Handshake latency** | ~1 RTT (often < 10ms) | Multiple round trips |
| **Throughput** | Near line rate | 60-80% of line rate |
| **Auditability** | Full manual audit possible | Too complex to fully audit |

### Key Features

- **Built into Linux kernel** — no extra daemon, just `wg` and `wg-quick`
- **Cryptokey routing** — public key = identity, allowed IPs = routing
- **Silent after handshake** — no keepalive noise (unless configured)
- **Perfect forward secrecy** — ephemeral session keys, rekeyed every 2 minutes
- **DoS resistance** — cookie mechanism, no state before authentication
- **Roaming** — change network (WiFi → mobile), tunnel survives
- **Cross-platform** — Linux, Windows, macOS, FreeBSD, OpenBSD, Android, iOS

---

## Installation

### Linux (Kernel Module)

```bash
# Check if kernel module is available
modinfo wireguard
# If not found, install:
sudo apt install wireguard  # Debian/Ubuntu
sudo dnf install wireguard-tools  # Fedora/RHEL
sudo pacman -S wireguard-tools    # Arch

# Load module
sudo modprobe wireguard
lsmod | grep wireguard
```

Most distros with kernel 5.6+ have WireGuard built-in. Older kernels need `wireguard-dkms`.

### macOS

```bash
brew install wireguard-tools
# Also install the macOS app from https://www.wireguard.com/install/
```

### Windows

Download from [wireguard.com/install](https://www.wireguard.com/install/) — includes GUI + CLI.

### Docker

```bash
docker pull linuxserver/wireguard
```

---

## Quick Start

### Step 1: Generate Keys

Every peer needs a private + public key pair:

```bash
# Generate private key
wg genkey | tee private.key
# Output: uOr/3T0...Sn5X=

# Derive public key
cat private.key | wg pubkey | tee public.key
# Output: 9F7L...fPw=
```

> **Save both keys.** The private key stays on the peer. The public key is shared (like an address).

### Step 2: Create Config

Minimal config for a **VPS server** (`/etc/wireguard/wg0.conf`):

```ini
[Interface]
Address = 10.0.0.1/24
PrivateKey = <vps-private-key>
ListenPort = 51820

[Peer]
# Mini PC / Laptop
PublicKey = <client-public-key>
AllowedIPs = 10.0.0.2/32
```

Minimal config for a **Mini PC client** (`/etc/wireguard/wg0.conf`):

```ini
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client-private-key>

[Peer]
# VPS Server
PublicKey = <vps-public-key>
Endpoint = vps.example.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

### Step 3: Start the Tunnel

```bash
# Start
sudo wg-quick up wg0

# Check status
sudo wg show
# interface: wg0
#   public key: ...
#   private key: (hidden)
#   listening port: 51820
#
# peer: <public-key>
#   endpoint: vps.example.com:51820
#   allowed ips: 10.0.0.0/24
#   latest handshake: 5 seconds ago
#   transfer: 1.23 KiB received, 4.56 KiB sent

# Test
ping 10.0.0.1
```

### Step 4: Enable Auto-Start

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
```

---

## Configuration Guide

### Interface Section

```ini
[Interface]
Address = 10.0.0.1/24        # IP address + subnet mask
PrivateKey = <private-key>    # This peer's private key (SECRET)
ListenPort = 51820            # UDP port to listen on (default)
DNS = 1.1.1.1                 # Push DNS to clients (optional)
MTU = 1420                    # MTU (default 1420, lower for overhead)
Table = auto                  # Routing table (auto = main table)
PreUp = iptables ...          # Commands before interface goes up
PostUp = iptables ...         # Commands after interface goes up
PreDown = iptables ...        # Commands before interface goes down
PostDown = iptables ...       # Commands after interface goes down
```

### Peer Section

```ini
[Peer]
PublicKey = <peer-public-key>           # The other peer's public key
Endpoint = vps.example.com:51820        # Public address (only needed on clients)
AllowedIPs = 10.0.0.0/24               # Routes to send through this tunnel
PersistentKeepalive = 25                # Seconds between keepalive pings
PresharedKey = <psk>                    # Optional extra layer of symmetric encryption
```

### AllowedIPs Deep Dive

`AllowedIPs` does **two things** at once:

1. **Routing** — which IPs should be reached through this tunnel
2. **ACL** — which source IPs to accept from this peer

Examples:

```
# Route all traffic through tunnel (kill switch)
AllowedIPs = 0.0.0.0/0, ::/0

# Route only the WireGuard subnet
AllowedIPs = 10.0.0.0/24

# Route specific IPs
AllowedIPs = 10.0.0.1/32, 192.168.1.0/24, 172.16.0.0/12

# Server side: only accept from this specific client
AllowedIPs = 10.0.0.2/32
```

> On the **server**, `AllowedIPs` acts as an ACL — only traffic from these IPs is accepted from that peer.
> On the **client**, `AllowedIPs` tells the routing table where to send traffic.

---

## Hub & Spoke Topology

This is the most common setup for connecting a mini PC at home to multiple VPS servers.

```
                    ┌──────────────┐
                    │   VPS Hub    │
                    │  10.0.0.1/24 │
                    │  WireGuard   │
                    │  :51820      │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │  Mini PC   │ │  VPS 1     │ │  VPS 2     │
     │ 10.0.0.2   │ │ 10.0.0.3  │ │ 10.0.0.4   │
     │ (NAT/Home) │ │ (Provider) │ │ (Provider) │
     └────────────┘ └────────────┘ └────────────┘
           │               │              │
           └───────────────┼──────────────┘
                     Can reach each other
                     (via hub routing)
```

### Hub Config (VPS)

```ini
# /etc/wireguard/wg0.conf — VPS Hub
[Interface]
Address = 10.0.0.1/24
PrivateKey = <hub-private-key>
ListenPort = 51820
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Mini PC
PublicKey = <minipc-public-key>
AllowedIPs = 10.0.0.2/32

[Peer]
# VPS 1
PublicKey = <vps1-public-key>
AllowedIPs = 10.0.0.3/32

[Peer]
# VPS 2
PublicKey = <vps2-public-key>
AllowedIPs = 10.0.0.4/32
```

### Mini PC Config

```ini
# /etc/wireguard/wg0.conf — Mini PC
[Interface]
Address = 10.0.0.2/24
PrivateKey = <minipc-private-key>
DNS = 10.0.0.1

[Peer]
# VPS Hub
PublicKey = <hub-public-key>
Endpoint = vps-hub.example.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

### VPS 1 Config

```ini
# /etc/wireguard/wg0.conf — VPS 1
[Interface]
Address = 10.0.0.3/24
PrivateKey = <vps1-private-key>

[Peer]
# VPS Hub
PublicKey = <hub-public-key>
Endpoint = vps-hub.example.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

Repeat for VPS 2 with `10.0.0.4`.

### Enable Routing on Hub

```bash
# Enable IP forwarding (persistent)
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf
```

### Result

Now from your mini PC:

```bash
ping 10.0.0.3   # → VPS 1 via hub
ping 10.0.0.4   # → VPS 2 via hub
scp file.txt 10.0.0.3:/tmp/  # Transfer via tunnel
```

---

## Site-to-Site

Connect two entire networks (e.g., home LAN ↔ cloud VPC).

```
Home Network              WireGuard               Cloud VPC
192.168.1.0/24          10.0.0.0/24             10.0.0.0/24
    │                       │                        │
┌────┴─────┐         ┌──────┴──────┐          ┌─────┴─────┐
│ Home GW  │◄═══════►│  VPS Hub    │◄════════►│ Cloud GW  │
│ 10.0.0.2 │         │ 10.0.0.1    │          │ 10.0.0.3  │
└──────────┘         └─────────────┘          └───────────┘
```

### Home Gateway Config

Route entire home LAN through the tunnel:

```ini
[Interface]
Address = 10.0.0.2/24
PrivateKey = <home-private-key>
PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = iptables -t nat -A POSTROUTING -o wg0 -j MASQUERADE

[Peer]
PublicKey = <vps-public-key>
Endpoint = vps.example.com:51820
AllowedIPs = 10.0.0.0/24     # WireGuard subnet
PersistentKeepalive = 25
```

### VPS Config (Accepting Home Traffic)

```ini
[Peer]
# Home Gateway
PublicKey = <home-public-key>
AllowedIPs = 10.0.0.2/32, 192.168.1.0/24
```

Now from any cloud VPS in the mesh:

```bash
ping 192.168.1.50   # Reach a device on home LAN
```

---

## NAT Traversal & Persistence

WireGuard has no built-in NAT traversal or DPI bypass. Use these techniques:

### PersistentKeepalive

Essential for peers behind NAT:

```ini
[Peer]
PersistentKeepalive = 25  # Send a ping every 25 seconds
```

Keeps the NAT mapping alive so the peer is reachable when it initiates.

- **25s** — good default for most NATs
- **10s** — aggressive (ISP CGNAT, mobile networks)
- **5s** — extreme (unstable connections)

### UDP Hole Punching

WireGuard supports **roaming by design** — if the client's IP changes, the server sees traffic from the new IP and updates the endpoint automatically. No config change needed.

### Firewall Rules

```bash
# Allow incoming WireGuard
sudo ufw allow 51820/udp

# Or via iptables
sudo iptables -A INPUT -p udp --dport 51820 -j ACCEPT
```

### Behind CGNAT

Cannot receive incoming connections? Use a **hub** model where only the hub needs a public port:

```
Mini PC (CGNAT) ──outbound──► VPS Hub (public) ◄──outbound── VPS 2 (public)
```

Mini PC initiates → hub knows it → hub can reply. VPS 2 also initiates → hub knows it. Now mini PC and VPS 2 can communicate through the hub.

---

## Advanced Config

### Full Tunnel (All Traffic Through VPN)

Route all internet traffic through the VPS:

```ini
[Peer]
Endpoint = vps.example.com:51820
PublicKey = <vps-public-key>
AllowedIPs = 0.0.0.0/0, ::/0    # Route everything
PersistentKeepalive = 25
```

> ⚠️ This breaks internet if the tunnel drops. Add `Table = off` and manage routes manually if you need failover.

### Kill Switch

Prevent traffic leaks if WireGuard disconnects:

```bash
# Option 1: Firewall rule (during PostUp)
PostUp = iptables -I OUTPUT ! -o wg0 -m mark ! --mark $(wg show wg0 fwmark) -j REJECT

# Option 2: Only route through tunnel
PostUp = ip rule add from 10.0.0.2 table 200
PostUp = ip route add default via 10.0.0.1 table 200
PostDown = ip rule del from 10.0.0.2 table 200
```

### Multi-Peer (Client Connects to Multiple Servers)

One interface, many peers:

```ini
[Interface]
Address = 10.0.0.5/24
PrivateKey = <client-private-key>

[Peer]
# VPS in DO
PublicKey = <do-public-key>
Endpoint = do-vps.example.com:51820
AllowedIPs = 10.0.0.1/32
PersistentKeepalive = 25

[Peer]
# VPS in Hetzner
PublicKey = <hetzner-public-key>
Endpoint = hetzner-vps.example.com:51820
AllowedIPs = 10.0.0.2/32
PersistentKeepalive = 25

[Peer]
# VPS in BiznetGIO
PublicKey = <biznet-public-key>
Endpoint = biznet-vps.example.com:51820
AllowedIPs = 10.0.0.3/32
PersistentKeepalive = 25
```

### Pre-Shared Key (PSK)

Add an extra layer of post-quantum resistance:

```bash
# Generate PSK
wg genpsk > psk.key

# Distribute to both peers
```

Config:

```ini
[Peer]
PresharedKey = <psk-content>
```

PSK is optional but recommended for defense-in-depth. Both peers must have the same PSK.

### Custom MTU

Adjust for specific network conditions:

| Network | Recommended MTU |
|---------|----------------|
| Ethernet | 1420 (default) |
| PPPoE | 1412 |
| LTE/4G | 1360 |
| LTE/5G | 1340 |
| Starlink | 1350 |
| OpenVZ VPS | 1400 |

```ini
[Interface]
MTU = 1360
```

### Table Off (Manual Routing)

Don't let `wg-quick` touch the routing table:

```ini
[Interface]
Table = off

# Then manage routes manually
PostUp = ip route add 10.0.0.0/24 dev wg0
```

Useful when you have complex routing requirements or use BGP.

---

## Monitoring & Debugging

### Quick Status

```bash
sudo wg show
# Human-readable summary

sudo wg show wg0
# Single interface

sudo wg show wg0 dump
# Machine-parsable (good for scripts)
```

### Detailed Metrics

```bash
# Transfer stats
sudo wg show wg0 | grep transfer
# transfer: 1.23 GiB received, 456.78 MiB sent

# Handshake time
sudo wg show wg0 | grep handshake
# latest handshake: 2 minutes, 3 seconds ago

# Interface stats
ip -s link show wg0
# RX/TX bytes, packets, errors, dropped
```

### tcpdump for WireGuard

```bash
# See WireGuard handshake packets
sudo tcpdump -i any udp port 51820 -nn

# See decrypted traffic (on the wg interface)
sudo tcpdump -i wg0 -nn
```

### Monitoring Script

```bash
#!/bin/bash
# WireGuard health check

INTERFACE="wg0"
TIMEOUT=180  # 3 minutes without handshake = alert

LAST_HANDSHAKE=$(sudo wg show $INTERFACE latest-handshakes | awk '{print $2}')
NOW=$(date +%s)
DIFF=$((NOW - LAST_HANDSHAKE))

if [ $DIFF -gt $TIMEOUT ]; then
    echo "⚠️  WireGuard $INTERFACE: no handshake for ${DIFF}s"
    exit 1
else
    echo "✅ WireGuard $INTERFACE: OK (last handshake ${DIFF}s ago)"
fi
```

### Prometheus Export

Use `wg_exporter`:

```yaml
# docker-compose.yml for monitoring
services:
  wg_exporter:
    image: mindflavor/prometheus_wireguard_exporter:latest
    network_mode: host
    environment:
      - WIREGUARD_EXPORTER_INTERFACE_REGEX=wg.*
```

Grafana dashboards available on [grafana.com](https://grafana.com/grafana/dashboards/).

---

## Security

### Default Security Properties

| Property | Implementation |
|----------|---------------|
| **Key exchange** | Curve25519 ECDH |
| **Encryption** | ChaCha20-Poly1305 (AEAD) |
| **Hashing** | BLAKE2s |
| **Perfect Forward Secrecy** | Yes — rekey every 120s |
| **Post-quantum** | Optional PSK added |
| **Identity hiding** | No (public key visible) |

### Best Practices

**1. Firewall the tunnel**

```ini
# Only accept WireGuard traffic
PostUp = iptables -I INPUT -p udp --dport 51820 -j ACCEPT
PostUp = iptables -I FORWARD -i wg0 -j ACCEPT
PostUp = iptables -I FORWARD -o wg0 -j ACCEPT
PostDown = iptables -D INPUT -p udp --dport 51820 -j ACCEPT
```

**2. Rate limit handshakes**

```bash
# Prevent handshake flood
sudo iptables -A INPUT -p udp --dport 51820 -m recent --set --name WG
sudo iptables -A INPUT -p udp --dport 51820 -m recent --update --seconds 1 --hitcount 10 --name WG -j DROP
```

**3. Rotate keys periodically**

```bash
# Monthly key rotation
wg genkey | tee /etc/wireguard/private.key
cat /etc/wireguard/private.key | wg pubkey > /etc/wireguard/public.key

# Update config with new private key
# Distribute new public key to peers
sudo wg-quick down wg0 && sudo wg-quick up wg0
```

**4. Use PSK for all peers**

```bash
# Add PSK to existing config
wg genpsk | sudo tee /etc/wireguard/psk.key
```

### What WireGuard Does NOT Protect

- **Metadata** — the handshake reveals the server's public key and IP
- **Traffic patterns** — packet size, timing, and volume are visible (like any VPN)
- **Identity** — if someone sees your public key, they can identify your peers (if they know the IP)

---

## Migration from OpenVPN

### Quick Comparison

| Task | OpenVPN | WireGuard |
|------|---------|-----------|
| **Generate keys** | `easyrsa build-ca` ... | `wg genkey \| wg pubkey` |
| **Port** | 1194 UDP (or TCP 443) | 51820 UDP |
| **Config size** | 50+ lines | 5-10 lines |
| **Start** | `systemctl start openvpn@server` | `wg-quick up wg0` |
| **Add user** | Generate cert + sign + config | Add peer block + distribute public key |

### Migration Steps

**1. Set up WireGuard alongside OpenVPN:**

```bash
# Both can run simultaneously
sudo wg-quick up wg0
```

**2. Migrate clients one by one:**

```bash
# Old: openvpn client.ovpn
# New: wg-quick up wg0
```

**3. Remove OpenVPN:**

```bash
sudo systemctl stop openvpn@server
sudo systemctl disable openvpn@server
sudo apt remove openvpn easy-rsa
sudo ufw delete allow 1194
```

**4. Update firewall:**

```bash
sudo ufw allow 51820/udp
```

### Config Comparison

| OpenVPN | WireGuard |
|---------|-----------|
| `dev tun` | `[Interface]` |
| `ifconfig 10.0.0.1 10.0.0.2` | `Address = 10.0.0.1/24` |
| `secret static.key` | `PrivateKey = <key>` |
| `remote 1.2.3.4 1194` | `Endpoint = 1.2.3.4:51820` |
| `push "route 10.0.0.0 255.255.255.0"` | `AllowedIPs = 10.0.0.0/24` |
| `keepalive 10 60` | `PersistentKeepalive = 25` |

---

## Docker

### Server with Docker

```yaml
services:
  wireguard:
    image: linuxserver/wireguard:latest
    container_name: wireguard-server
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Jakarta
      - SERVERURL=vps.example.com
      - SERVERPORT=51820
      - PEERS=minipc,vps1,vps2
      - PEERDNS=auto
      - INTERNAL_SUBNET=10.0.0.0/24
    volumes:
      - ./config:/config
      - /lib/modules:/lib/modules
    ports:
      - "51820:51820/udp"
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv6.conf.all.forwarding=1
    restart: unless-stopped
```

After startup, peer configs are generated at `./config/peer_<name>/`.

### Client in Docker

```yaml
services:
  wireguard-client:
    image: linuxserver/wireguard:latest
    container_name: wireguard-client
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    volumes:
      - ./wg0.conf:/config/wg0.conf:ro
      - /lib/modules:/lib/modules
    sysctls:
      - net.ipv4.ip_forward=1
    restart: unless-stopped
```

### Test Inside Docker

```bash
docker exec wireguard-client ping 10.0.0.1
```

---

## Comparison

### WireGuard vs Other VPN Solutions

| Feature | WireGuard | Tailscale | Netmaker | Netbird |
|---------|:---------:|:---------:|:--------:|:-------:|
| **Self-hosted** | ✅ Yes | ❌ (SaaS) | ✅ Yes | ✅ Yes |
| **Control plane** | None (manual) | Coordinated | Automated | Automated |
| **Web UI** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Auto mesh** | ❌ Manual config | ✅ Auto | ✅ Auto | ✅ Auto |
| **NAT traversal** | ❌ Manual (Keepalive) | ✅ Built-in | ✅ STUN/relay | ✅ TURN/relay |
| **Client size** | ~0.5 MB | ~10 MB | ~15 MB | ~15 MB |
| **Kernel integration** | ✅ Native | ✅ Native | ✅ Native | ✅ Native |
| **CPU overhead** | **Minimal** | Minimal | Minimal | Minimal |
| **Management overhead** | Manual (config per peer) | Zero | Low (UI) | Low (UI) |

### When to Use Plain WireGuard vs an Orchestrator

**Use plain WireGuard when:**

- You have **2-5 static peers** (mini PC + a few VPS)
- You want **zero dependencies** — no Docker, no DB, no extra services
- You're comfortable editing configs manually
- You need **maximum performance** (no extra layer)
- You want **simplicity** — one port, one protocol, one binary

**Use an orchestrator (Tailscale/Netmaker/Netbird) when:**

- You have **5+ nodes** that change frequently
- You need **auto-discovery and mesh**
- You want **access control** (groups, policies)
- Peers are behind **complex NAT/CGNAT**
- You want a **web UI** for management

---

## Pitfalls

### ❌ Firewall Blocking UDP

WireGuard uses UDP. Some cloud providers or corporate firewalls block or rate-limit UDP.

**Fix:** Try port 443 UDP instead of 51820, or use `udptunnel`/`udp2raw` to wrap UDP in TCP.

### ❌ Kernel Module Not Loaded

```bash
sudo modprobe wireguard
# Module not found
```

**Fix:** Install `wireguard-dkms` or use the userspace implementation (`wireguard-go`):

```bash
sudo apt install wireguard-go wireguard-tools
# wireguard-go creates a userspace tunnel (slower, but works)
```

### ❌ No Handshake

```bash
sudo wg show
# peer: ... (no handshake in N seconds)
```

**Checklist:**

1. Is the server's port open? → `nc -uvz vps.example.com 51820`
2. Is the firewall allowing UDP 51820? → `ufw status` / `iptables -L`
3. Are keys correct? → Compare public keys on both sides
4. Is `PersistentKeepalive` set on the NAT side?
5. Is `net.ipv4.ip_forward=1` on the server?
6. Is the client's `AllowedIPs` matching what the server expects?

### ❌ AllowedIPs = 0.0.0.0/0 Breaks Internet

This routes ALL traffic through the tunnel. If the tunnel drops, you lose connectivity.

**Fix:** Add a kill switch or only route specific subnets:

```ini
# Instead of 0.0.0.0/0
AllowedIPs = 10.0.0.0/24, 192.168.0.0/16
```

### ❌ DNS Leaks

When using full tunnel mode, DNS may bypass the tunnel.

**Fix:** Set DNS explicitly:

```ini
[Interface]
DNS = 1.1.1.1  # or your internal DNS
```

### ❌ MTU Issues

Some networks (PPPoE, LTE) fragment WireGuard packets:

```bash
# Symptoms: connection works but file transfers stall
# Fix: lower MTU
MTU = 1360  # For LTE
```

### ❌ Multiple wg-quick Instances

You can run multiple WireGuard interfaces:

```bash
sudo wg-quick up wg0   # Config at /etc/wireguard/wg0.conf
sudo wg-quick up wg1   # Config at /etc/wireguard/wg1.conf
```

But ensure different subnets and ports:

```bash
# wg0.conf
Address = 10.0.0.1/24
ListenPort = 51820

# wg1.conf
Address = 10.0.1.1/24
ListenPort = 51821
```

### ❌ Systemd Timeout on Boot

If the network isn't ready when WireGuard starts:

```bash
# Edit systemd service
sudo systemctl edit wg-quick@wg0
```

```ini
[Unit]
After=network-online.target
Wants=network-online.target
```

### ❌ Config File Permissions

WireGuard private keys must be readable only by root:

```bash
sudo chmod 600 /etc/wireguard/*.key
sudo chmod 600 /etc/wireguard/*.conf
```
