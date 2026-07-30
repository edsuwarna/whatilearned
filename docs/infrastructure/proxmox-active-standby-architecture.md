---
title: Proxmox Active-Standby — 2 DC with GPU, Garage, and App Stack
description: - [Architecture Overview](#architecture-overview) - [Storage Strategy](#storage-strategy) - [VM Layout](#vm-layout) - [GPU Passthrough (NVIDIA L40)](#gpu-passthrough-nvidia-l40) - [Garage Object Storage](#garage-object-storage) - [Database Replication](#database-replication) - [Observability Stack](#observability-stack) - [Failover Procedure](#failover-procedure) - [Quorum & Monitoring](#quorum--monitoring) - [Setup Flow](#setup-flow)
---

# Proxmox Active-Standby — 2 DC with GPU, Garage, and App Stack

> **Last updated:** 2026-07-30
> **Topik:** Detailed architecture for running Proxmox VE in an active-standby configuration across 2 data centers, with GPU passthrough (NVIDIA L40), Garage S3 cluster, PostgreSQL, self-hosted LLM (Ollama), and monitoring stack.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Storage Strategy](#storage-strategy)
- [VM Layout](#vm-layout)
- [GPU Passthrough (NVIDIA L40)](#gpu-passthrough-nvidia-l40)
- [Garage Object Storage](#garage-object-storage)
- [Database Replication](#database-replication)
- [Observability Stack](#observability-stack)
- [Failover Procedure](#failover-procedure)
- [Quorum & Monitoring](#quorum--monitoring)
- [Setup Flow](#setup-flow)

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────┐
│                      DC1 — ACTIVE                             │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────┐ │
│  │ VM Backend │ │ VM Frontend│ │ VM DB      │ │ VM Ollama │ │
│  │ (LXC/VM)   │ │ (LXC/VM)   │ │ (Postgres) │ │ (GPU L40) │ │
│  └────────────┘ └────────────┘ └──────┬─────┘ └─────┬─────┘ │
│  ┌────────────┐ ┌────────────┐  D┌────┴─────┐  D┌──┴────┐  │
│  │ VM Garage1 │ │ VM Garage2 │  │ Repl.    │  │ Repl. │  │
│  │  (localFS) │ │  (localFS) │  │ (30 min) │  │(60min)│  │
│  └────────────┘ └────────────┘  │          │  │       │  │
│  ┌────────────┐ ┌────────────┐  └──────────┘  └───────┘  │
│  │ VM Garage3 │ │ VM Beszel  │                           │
│  │  (localFS) │ │  (monitor) │                           │
│  └────────────┘ └────────────┘                           │
│  ┌────────────┐                                           │
│  │ VM Dozzle  │                                           │
│  │ (logging)  │                                           │
│  └────────────┘                                           │
└──────────────────────────┬────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │  3rd Node (VPS)          │
              │  - qdevice (quorum)      │
              │  - Health monitoring     │
              │  - DNS failover trigger  │
              │  - Optional: PBS backup  │
              └────────────┬────────────┘
                           │
┌──────────────────────────▼────────────────────────────────┐
│                      DC2 — STANDBY (all VMs STOPPED)      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────┐│
│  │ VM Backend │ │ VM Frontend│ │ VM DB      │ │ VM Ollama ││
│  │ (STOP)     │ │ (STOP)     │ │ (STOP)     │ │ (STOP)    ││
│  │ Disk repl. │ │ Disk repl. │ │ DB repl.   │ │ GPU L40   ││
│  └────────────┘ └────────────┘ └────────────┘ └───────────┘│
│  ┌────────────┐ ┌────────────┐ ┌────────────┐             │
│  │ VM Garage1'│ │ VM Garage2'│ │ VM Garage3'│             │
│  │   (STOP)   │ │   (STOP)   │ │   (STOP)   │             │
│  └────────────┘ └────────────┘ └────────────┘             │
│  ┌────────────┐ ┌────────────┐                             │
│  │ VM Beszel' │ │ VM Dozzle' │                             │
│  │   (STOP)   │ │   (STOP)   │                             │
│  └────────────┘ └────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

## Storage Strategy

### ZFS Pool Layout

```bash
# DC1 — NVMe/SSD pool buat DB + VM system
zpool create -o ashift=12 fast-pool mirror /dev/nvme0n1 /dev/nvme1n1
zfs set compression=lz4 fast-pool
zfs set atime=off fast-pool

# DC1 — HDD/SATA pool buat Garage object storage
zpool create -o ashift=12 bulk-pool raidz2 /dev/sda /dev/sdb /dev/sdc /dev/sdd
zfs set compression=lz4 bulk-pool

# DC2 — Sama
zpool create -o ashift=12 fast-pool mirror /dev/nvme0n1 /dev/nvme1n1
zpool create -o ashift=12 bulk-pool raidz2 /dev/sda /dev/sdb /dev/sdc /dev/sdd
```

### ZFS Replication (Built-in Proxmox)

Proxmox has native ZFS replication via GUI or CLI — no extra tools needed.

```bash
# Setup replication job via CLI
pvesm set local-zfs --replication-enabled 1

# Or via API
pvesh create /cluster/replication \
  --id 'dc1-to-dc2-db-vm' \
  --source 'dc1-node:vm/100' \
  --target 'dc2-node:vm/100' \
  --rate 50 \
  --schedule '*/30 * * * *'  # every 30 minutes
```

**Replication schedule recommendation:**

| VM | Schedule | Method | Notes |
|----|----------|--------|-------|
| DB (Postgres) | Every 30 min | ZFS send/recv | Last resort — prefer DB-native replication |
| Ollama GPU | Every 60 min | ZFS send/recv | Model files are large, incremental |
| Backend/Frontend | Every 30 min | ZFS send/recv | Stateless, config only |
| Garage disks | Every 30 min | ZFS send/recv | Garage handles internal quorum |
| Dozzle/Beszel | Every 60 min | ZFS send/recv | Non-critical, logs are ephemeral |

## VM Layout

### Recommended VM sizing

| VM | vCPU | RAM | OS Disk | Data Disk | Type | Notes |
|----|------|-----|---------|-----------|------|-------|
| Backend | 4 | 8 GB | 20 GB | - | LXC preferred | Lightweight container |
| Frontend | 2 | 4 GB | 10 GB | - | LXC preferred | Nginx/Node |
| Database | 4 | 16 GB | 50 GB | 100 GB (ZFS) | KVM | Postgres, disk on fast-pool |
| Ollama | 8 | 32 GB | 50 GB | 200 GB (models) | KVM | GPU passthrough, disk on fast-pool |
| Paddle OCR | 4 | 8 GB | 20 GB | 50 GB | KVM | GPU passthrough or CPU |
| Garage 1 | 2 | 4 GB | 20 GB | 500 GB | KVM | Data disk on bulk-pool |
| Garage 2 | 2 | 4 GB | 20 GB | 500 GB | KVM | Data disk on bulk-pool |
| Garage 3 | 2 | 4 GB | 20 GB | 500 GB | KVM | Data disk on bulk-pool |
| Beszel | 1 | 1 GB | 10 GB | - | LXC | Monitoring hub |
| Dozzle | 1 | 1 GB | 10 GB | - | LXC | Log viewer |

> Since both DCs have identical hardware (same GPU, same storage), the standby can take over at full capacity.

## GPU Passthrough (NVIDIA L40)

### Steps on Proxmox

```bash
# 1. Enable IOMMU in kernel
# Edit /etc/default/grub
# GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on" # Intel
# GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on"   # AMD
update-grub

# 2. Load VFIO modules
echo "vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd" > /etc/modules

# 3. Find L40 PCI ID
lspci -nn | grep -i nvidia   # e.g., 10de:27b8

# 4. Bind L40 to vfio-pci
echo "options vfio-pci ids=10de:27b8 disable_vga=1" > /etc/modprobe.d/vfio.conf

# 5. Blacklist nouveau (if present)
echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nvidia-nouveau.conf

# 6. Reboot & verify
dmesg | grep -i vfio
```

### VM Config

```bash
# Add PCI device to Ollama VM
qm set 101 -hostpci0 01:00.0,pcie=1,x-vga=1

# Optional: hugepages for GPU performance
echo 'vm.nr_hugepages = 16384' >> /etc/sysctl.conf
```

> Repeat the same setup on DC2 — the standby Ollama VM also has GPU passthrough ready.

## Garage Object Storage

Since you have only 2 physical servers but want 3 Garage nodes, run all 3 Garage VMs on DC1:

```
DC1 (ACTIVE)
├── Garage VM 1 ─ 10.0.1.51:3900 ─ disk: /dev/vdb (500GB)
├── Garage VM 2 ─ 10.0.1.52:3900 ─ disk: /dev/vdb (500GB)
└── Garage VM 3 ─ 10.0.1.53:3900 ─ disk: /dev/vdb (500GB)
```

**Garage configuration (`garage.toml`):**

```toml
metadata_dir = "/var/lib/garage/meta"
data_dir = "/var/lib/garage/data"
db_engine = "lmdb"
block_size = 1048576

replication_mode = "2"

[rpc]
bind_addr = "0.0.0.0:3901"
bootstrap_peers = [
    "10.0.1.51:3901",
    "10.0.1.52:3901",
    "10.0.1.53:3901",
]
```

**Replication:** Garage handles replication internally (2 copies, quorum 2/3). Each VM disk is independently replicated via Proxmox ZFS to its counterpart on DC2.

On failover, start all 3 Garage VMs on DC2 — they reassemble as a cluster automatically (Garage uses rendez-vous hashing, not consensus).

## Database Replication

### PostgreSQL — Active-Standby Streaming Replication

```
┌──────────────┐     WAL stream     ┌──────────────┐
│ DC1 (Primary)│──────────────────► │ DC2 (Standby)│
│ vm-db:5432   │   synchronous      │ vm-db:5432   │
└──────────────┘   (optional)       └──────────────┘
```

**Primary config (`postgresql.conf`):**
```ini
wal_level = replica
max_wal_senders = 3
wal_keep_size = 1024    # 1 GB WAL retention
synchronous_commit = off  # Set 'on' for zero data loss (higher latency)
```

**Standby setup:**
```bash
# On DC2 standby
pg_basebackup -h 10.0.1.10 -D /var/lib/postgresql/16/main -U replicator -P -R

# standby.signal
touch /var/lib/postgresql/16/main/standby.signal

# Standby config
echo "primary_conninfo = 'host=10.0.1.10 port=5432 user=replicator password=xxx'" >> postgresql.conf
```

**Application connection:**
- Normal: connect to DC1 primary IP
- Failover: promote standby (`pg_ctl promote`) + update connection string / DNS

> **Note:** ZFS replication of the DB VM disk is a backup of last resort — DB-native streaming replication is preferred for RPO control.

### Failover Procedure for DB

```bash
# On DC2 standby
pg_ctl promote -D /var/lib/postgresql/16/main

# Verify
psql -c "SELECT pg_is_in_recovery();"
# → f (false = primary mode)
```

---

## Observability Stack

### Beszel (Monitoring)

```
DC1: Beszel Agent (on each VM) ──► Beszel Hub (VM monitor)
DC2: Beszel Agent (on each VM) ──► same Hub (if reachable across DC)

Or: separate Hub per DC with manual switch
```

**Deployment:** Docker Compose in LXC container

```yaml
services:
  beszel:
    image: henrygd/beszel:latest
    container_name: beszel-hub
    restart: unless-stopped
    ports:
      - "8090:8090"
    volumes:
      - beszel-data:/beszel/data
    environment:
      - TZ=Asia/Jakarta

volumes:
  beszel-data:
```

### Dozzle (Log Viewer)

```
DC1: Dozzle agent → Docker socket → log viewer
DC2: Dozzle agent → Docker socket → log viewer
```

**Deployment:**

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    container_name: dozzle
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

---

## Failover Procedure

When DC1 is down, here's the step-by-step to bring DC2 live:

### Prerequisites

- ZFS replication running regularly (every 30 min)
- All DC2 VMs exist but in STOP state
- DNS managed via API (e.g., Cloudflare API)
- Monitoring script on 3rd node detects DC1 failure

### Step-by-step: DC1 → DC2 failover

```bash
# 1. Verify DC1 is truly down (no false positive)
ping -c 5 dc1-baremetal.internal

# 2. Stop/disable ZFS replication from DC1 (will fail anyway)
pvesh delete /cluster/replication/$(replication-id)

# 3. Start critical services in order on DC2
#    a. Garage cluster first (storage backend)
qm start 201  # Garage VM 1
qm start 202  # Garage VM 2
qm start 203  # Garage VM 3
#    Wait: verify Garage cluster healthy (garage status)

#    b. Database
qm start 104  # PostgreSQL
#    Wait: PostgreSQL recovery + WAL replay
#    Then promote to primary if needed

#    c. Application stack
qm start 101  # Backend
qm start 102  # Frontend

#    d. GPU workloads
qm start 105  # Ollama (GPU L40)
qm start 106  # Paddle OCR (GPU or CPU)

#    e. Observability (last — monitoring itself is non-critical)
qm start 107  # Beszel
qm start 108  # Dozzle

# 4. Update DNS → point to DC2 IPs
# Via Cloudflare API:
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"DC2_PUBLIC_IP"}'
```

### Estimated RTO

| Component | Time | Notes |
|-----------|------|-------|
| VM boot (KVM) | ~30s each | Parallel start |
| Garage recovery | ~30s | Re-connects automatically |
| PostgreSQL recovery | ~1-5 min | WAL replay depends on lag |
| Application start | ~10s | Service manager (systemd) |
| DNS propagation | ~1-5 min | TTL-dependent |
| **Total RTO** | **~5-10 min** | Worst case with DB replay |
| **Total RPO** | **30 min** | Limited by ZFS replication interval |

### Failback: DC2 → DC1

```bash
# 1. After DC1 is healthy again, reverse replication
#    DC2 → DC1 now (standby → former primary)

# 2. Sync data back
#    - Rebuild DB replication: DC2 (primary) → DC1 (standby)
#    - ZFS send/recv from DC2 back to DC1

# 3. Graceful switch
#    - Stop apps on DC2
#    - Update DNS back to DC1
#    - Start VMs on DC1
#    - Verify

# 4. Re-establish original replication direction
#    DC1 (active) → DC2 (standby)
```

> **Important:** After failback, re-run the ZFS replication job in the original direction (DC1→DC2).

## Quorum & Monitoring

### 3rd Node (VPS) Responsibilities

A small VPS ($5-10/month) handles the decision logic:

```
┌─────────────────────────┐
│  3rd Node (VPS)          │
│  ├── Corosync/qdevice    │  (Proxmox quorum tie-breaker)
│  ├── Health check script │  (ping/API check to both DCs)
│  ├── DNS API updater     │  (Cloudflare API)
│  └── Optional: PBS       │  (Proxmox Backup Server)
└─────────────────────────┘
```

**Simple health check script (pseudo):**

```bash
#!/bin/bash
# Run on 3rd node every 1 minute

check_dc1=$(curl -s -o /dev/null -w "%{http_code}" http://dc1-baremetal:8006)
check_dc2=$(curl -s -o /dev/null -w "%{http_code}" http://dc2-baremetal:8006)

if [[ "$check_dc1" != "200" && "$check_dc2" == "200" ]]; then
  echo "DC1 DOWN. Triggering failover..."
  # Send notification (Telegram/Discord)
  # Optionally start automated failover script
fi
```

**Notification on failover:** Send alert to Telegram/Discord via webhook so the admin can confirm or cancel.

### Proxmox qdevice setup

```bash
# On 3rd node (any Linux VPS with corosync-qnetd)
apt install corosync-qnetd
systemctl enable --now corosync-qnetd

# On Proxmox nodes (DC1 & DC2)
pvecm qdevice setup <3rd-node-ip> --vote-mode 1
pvecm status  # Verify quorum
```

---

## Setup Flow

### Implementation Roadmap

| Phase | Task | Est. Time |
|-------|------|-----------|
| **Phase 1** | Install Proxmox VE on both baremetal servers | 2 hours |
| **Phase 2** | Configure ZFS pools (fast + bulk) on both DCs | 1 hour |
| **Phase 3** | Setup 3rd node VPS: qdevice + health monitor | 1 hour |
| **Phase 4** | Create VMs: Backend, Frontend, DB, Ollama, Garage | 2 hours |
| **Phase 5** | GPU passthrough (L40) — both DCs | 1 hour |
| **Phase 6** | Garage cluster setup (3 VMs on DC1) | 1 hour |
| **Phase 7** | Configure ZFS replication jobs via Proxmox GUI | 30 min |
| **Phase 8** | Setup DB replication (PostgreSQL streaming) | 30 min |
| **Phase 9** | Deploy Beszel + Dozzle in LXC containers | 30 min |
| **Phase 10** | Test failover procedure + write runbook | 2 hours |
| **Total** | | **~11-12 hours** |

### Key Notes

- **DNS failover** — recommended to use Cloudflare API with low TTL (60s) for fast switch
- **Test failover regularly** — at least once a month, test the full procedure
- **Network bandwidth** — ZFS replication bandwidth depends on DC-DC link speed. Use `--rate` to throttle
- **Garage in active-standby** — Garage internal quorum only matters in the active DC. Standby DC just starts the VMs and Garage re-assembles automatically
- **No shared storage needed** — each DC has its own local ZFS pools, which simplifies the architecture significantly

### Related

- [Proxmox vs OpenStack vs CloudStack Comparison](./virtualization-comparison-proxmox-cloudstack-openstack.md)
- [Garage Object Storage Setup](../storage/object-storage-comparison.md)
- [Beszel Monitoring](../monitoring/beszel.md)
- [Dozzle Log Viewer](../monitoring/dozzle.md)
