---
title: Proxmox vs OpenStack vs CloudStack — Choosing Hypervisor for 2 DC
description: - [Overview](#overview) - [Comparison Table](#comparison-table) - [Proxmox VE](#proxmox-ve) - [OpenStack](#openstack) - [Apache CloudStack](#apache-cloudstack) - [Active-Standby Considerations](#active-standby-considerations) - [Decision Matrix](#decision-matrix)
---

# Proxmox vs OpenStack vs CloudStack — Choosing Hypervisor for 2 DC

> **Last updated:** 2026-07-30
> **Topik:** Choosing the right virtualization platform for 2 baremetal servers across 2 data centers in an active-standby setup

When you have **2 baremetal servers in 2 separate data centers**, picking the right virtualization platform is a critical decision. This comparison covers the three most mature open-source options: **Proxmox VE**, **OpenStack**, and **Apache CloudStack** — specifically for the active-standby use case.

Workload context: Backend, frontend, PostgreSQL, Garage (S3 object storage), Ollama with NVIDIA L40 GPU, Paddle OCR, plus monitoring (Beszel, Dozzle).

## Table of Contents

- [Overview](#overview)
- [Comparison Table](#comparison-table)
- [Proxmox VE](#proxmox-ve)
- [OpenStack](#openstack)
- [Apache CloudStack](#apache-cloudstack)
- [Active-Standby Considerations](#active-standby-considerations)
- [Decision Matrix](#decision-matrix)

## Overview

### Architecture at a Glance

```
DC1 (ACTIVE)                          DC2 (STANDBY)
┌─────────────────┐                  ┌─────────────────┐
│ Baremetal A     │  ZFS / storage   │ Baremetal B     │
│  - Proxmox/     │◄────────────────→│  - Proxmox/     │
│    CloudStack   │   replication    │    CloudStack   │
│  - VMs: active  │                  │  - VMs: standby │
│  - GPU L40      │                  │  - GPU L40      │
│  - Garage x3    │                  │  - Garage x3    │
└─────────────────┘                  └─────────────────┘
```

### What each platform handles

| Layer | Proxmox VE | OpenStack | CloudStack |
|-------|------------|-----------|------------|
| Virtualization | KVM + LXC | KVM (nova) | KVM (primary) |
| Control plane | Built-in per host | 20+ microservices | Management server |
| Storage | ZFS, Ceph, LVM | Ceph (default), NFS | NFS, Ceph, iSCSI, Local |
| Networking | Linux bridge / OVS | Neutron (OVN, VXLAN) | Advanced networking (VPC) |
| GPU passthrough | Mature (PCIe) | Complex (nova PCI alias) | Support exists |
| DR / Replication | ZFS send/recv (built-in) | Ceph rbd mirroring | Ceph / manual |
| Multi-tenancy | Limited | Full (Keystone IAM) | Full (Accounts/Domains) |

## Comparison Table

| Aspek | Proxmox VE | OpenStack | Apache CloudStack |
|-------|-----------|-----------|-------------------|
| **Arsitektur** | 2 node standalone cluster | Multi-service (20+ microservices) | Management Server + hypervisor agents |
| **Setup effort** | 1-2 jam | 2-5 hari (Kolla-Ansible) | 1-2 hari |
| **Min spec mgmt node** | N/A (built-in tiap host) | 16GB RAM, 4 vCPU | 8GB RAM, 4 vCPU |
| **Storage default** | ZFS, Ceph built-in, LVM | Ceph (mandatory for HA) | NFS, Ceph, iSCSI, Local |
| **High Availability** | Requires 3rd node quorum | Full HA | Full HA with mgmt server HA |
| **Live Migration** | Yes (shared storage needed) | Yes (Ceph) | Yes (shared storage) |
| **SDN** | Basic bridge/bond/OVS | Neutron (mature, complex) | Advanced networking |
| **Multi-tenancy** | Limited (datacenter/user) | Full IAM/keystone | Accounts/domains/projects |
| **Self-service UI** | Proxmox GUI (admin only) | Horizon (user + admin) | CloudStack UI (user + admin) |
| **API maturity** | REST API (lengkap) | REST API (paling mature) | REST API (lengkap) |
| **GPU Passthrough** | ✅ Simple PCIe passthrough | ⚠️ Possible but complex | ✅ Supported |
| **Terraform provider** | Yes | Yes (most mature) | Yes |
| **Community** | Besar, forum + subreddit aktif | Sangat besar, vendor-backed | Lebih kecil, ShapeBlue dominan |

## Proxmox VE

### Pros

- **Setup termudah** — ISO installer, join cluster, langsung jadi. Bisa production-ready dalam hitungan jam
- **Tanpa management node dedicated** — setiap node bisa standalone, HA cluster opsional
- **ZFS built-in** — ZFS send/recv replication antar DC built-in via GUI, incremental, compressed
- **GPU passthrough mature** — NVIDIA L40 passthrough langsung via PCIe, dokumentasi jelas
- **LXC container support** — ringan buat Beszel/Dozzle, overhead hampir nol
- **Backup integrated** — Proxmox Backup Server opsional (dedup + encryption)
- **Operasional ringan** — 1 orang bisa handle maintainance
- **Terraform + Ansible** — provider solid untuk IaC
- **Lisensi** — gratis penuh (enterprise repo cukup di-nonaktifkan)
- **Komunitas di Indonesia** — banyak pengguna, gampang cari referensi

### Cons

- **Quorum issue di 2 node** — cluster HA butuh 3rd vote (qdevice di VPS murah)
- **Multi-tenancy terbatas** — cocok untuk admin tim kecil, bukan cloud provider
- **SDN basic** — VLAN trunk + OVS, tidak ada VPC/advanced routing out of the box
- **Live migration antar DC** — butuh shared storage (Ceph stretched), latency-sensitive
- **Horizontal scaling limited** — ideal untuk 2-30 node, bukan ratusan
- **No native orchestration** — dibanding Heat (OpenStack), Proxmox tidak punya orchestration engine

## OpenStack

### Pros

- **Paling powerful** — full IaaS cloud dengan semua fitur
- **Multi-tenancy enterprise** — Keystone + RBAC + quotas + projects
- **Network virtualization advanced** — Neutron dengan VXLAN/VLAN/OVN, security groups, floating IP
- **Orchestration** — Heat (HOT templates), Mistral (workflow)
- **Baremetal provisioning** — Ironic untuk provisioning baremetal langsung
- **Scalability horizontal** — tak terbatas (ribuan node)
- **Ecosystem terluas** — Terraform, Ansible, Kubernetes (Magnum), monitoring (Ceilometer)
- **Vendor support** — Red Hat, Canonical, Mirantis

### Cons

- **Setup GILA berat** — minimal 20+ service containers (Kolla-Ansible)
- **Maintenance overhead** — upgrade tiap service independen, bisa pusing tiap siklus release
- **Resource consumption** — management plane lebih gede dari workload VM itu sendiri untuk 2 node
- **2-node HA problem** — MariaDB Galera + RabbitMQ HA di 2 node rawan split-brain
- **Ceph mandatory** — shared storage wajib Ceph untuk live migration, manage Ceph itu skill terpisah
- **GPU passthrough ribet** — perlu nova PCI alias, flavor extra specs, konfigurasi kustom
- **Tidak praktis untuk 2 server** — baru make sense di 10+ node dengan dedicated management
- **Tim dedicated** — butuh minimal 1-2 orang full-time maintain

## Apache CloudStack

### Pros

- **Setup lebih sederhana dari OpenStack** — management server single node (8GB RAM, 4 vCPU)
- **Multi-tenancy bagus** — accounts, domains, projects dengan resource limits
- **UI clean** — user portal + admin portal, cocok untuk tim non-admin
- **Hypervisor agnostic** — KVM, VMware, XenServer via satu management plane
- **Network advanced** — VPC, guest networks, port forwarding, load balancing
- **API mature** — AWS EC2-style API, kompatibel dengan banyak tools
- **GPU passthrough support** — bisa via KVM host configuration

### Cons

- **Management server SPOF** — butuh HA setup (2x mgmt server + DB HA cluster)
- **Setup tetap lebih ribet dari Proxmox** — perlu configure NFS/Ceph external, setup hypervisor agents
- **Storage live migration tricky** — tidak semulus Proxmox/ZFS
- **Quorum masalah** — management server HA di 2 DC juga butuh vote/3rd node
- **Dokumentasi terbatas** — komunitas lebih kecil dari Proxmox atau OpenStack
- **Release lag** — upgrade cycles kadang lambat
- **Instalasi hypervisor manual tiap host** — tidak seamless seperti Proxmox ISO

## Active-Standby Considerations

Active-standby (satu DC primary, satunya cold/warm standby) mengubah beberapa prioritas dibanding active-active cluster:

| Kebutuhan | Active-Active | Active-Standby |
|-----------|--------------|----------------|
| Quorum/Heartbeat | Critical | ✅ Tidak masalah — cukup monitoring script |
| Shared storage | Wajib (Ceph/FC) | Tidak perlu — ZFS replicate/rsync cukup |
| Live migration | Wajib | Tidak relevan — failover = reboot di standby |
| HA clustering | Mandatory | Opsional (bisa heartbeat sederhana) |
| Storage replication | Real-time sync | Async periodic (ZFS send/recv) |

### Recommended strategy for 2 DC

```
ZFS Replication (Proxmox native):
  DC1 ──zfs send/recv (incr, 30-60 menit)──→ DC2
  RTO: 5-15 menit (boot VMs di DC2)
  RPO: 30-60 menit (tergantung interval)

Failover flow:
  Monitoring detect DC1 down
  → Manual trigger / semi-auto script
  → Start VMs di DC2
  → Update DNS ke IP DC2
  → Service up setelah VM boot
```

## Decision Matrix

| Need | Proxmox | CloudStack | OpenStack |
|------|---------|------------|-----------|
| **GPU passthrough (L40)** | ✅ Mature, simple | ⚠️ Support ada | ❌ Ribet |
| **Setup speed** | ✅ Jam | ⚠️ 1-2 hari | ❌ 2-5 hari |
| **Active-standby DR** | ✅ ZFS repl built-in | ⚠️ Perlu konfigurasi | ❌ Overkill |
| **Multi-VM Garage cluster** | ✅ Bebas atur VM | ✅ Bebas atur VM | ✅ Bebas atur VM |
| **Ops cost (tim)** | ✅ 1 orang cukup | ⚠️ 1-2 orang | ❌ Tim dedicated |
| **Maintenance** | ✅ Ringan | ⚠️ Berat-sedang | ❌ Sangat berat |
| **Komunitas Indo** | ✅ Banyak | ⚠️ Jarang | ⚠️ Ada tapi mahal |
| **Multi-tenancy** | ❌ Terbatas | ✅ Bagus | ✅ Paling mature |

### Final Verdict

| Platform | Active-Standby cocok? | Setup effort | Maintenance | Rekomendasi |
|----------|----------------------|-------------|-------------|-------------|
| **Proxmox VE** | ✅ Sangat cocok | Rendah (1 hari) | Ringan | 🥇 **#1 choice** |
| **CloudStack** | ✅ Cocok | Sedang (2-3 hari) | Berat-sedang | 🥈 Kalo butuh UI multi-tenant |
| **OpenStack** | ⚠️ Bisa tapi tidak praktis | Tinggi (5-7 hari) | Sangat berat | ❌ Skip untuk 2 node |

**Proxmox VE** adalah rekomendasi utama untuk skenario 2 baremetal di 2 DC dengan workload yang mencakup GPU inference, object storage, dan aplikasi container/VM — karena kesederhanaan operasional, ZFS replication built-in, GPU passthrough yang mature, dan komunitas yang besar.
