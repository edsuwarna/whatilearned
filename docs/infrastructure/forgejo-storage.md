# Forgejo Storage & Cleanup

> **Last updated:** 2026-06-07
> **Topik:** Storage architecture, backup, cleanup strategies, Docker build cache management

## Table of Contents

- [Storage Architecture](#storage-architecture)
- [Estimasi Ukuran](#estimasi-ukuran)
- [Backup](#backup)
- [Storage Management](#storage-management)
- [Docker Build Cache — Masalah Utama](#docker-build-cache--masalah-utama)
- [Kapan Darurat? — Yang Terjadi Kalo Disk Penuh](#kapan-darurat--yang-terjadi-kalo-disk-penuh)
- [Cleanup Checklist — Dari Ringan ke Berat](#cleanup-checklist--dari-ringan-ke-berat)

## Storage Architecture

### Setup Optimal: Local SSD + R2 untuk LFS & Artifacts

| Data | Lokasi | Kapasitas |
|------|--------|-----------|
| **Git repo / code / history** 🔥 | **Volume Docker local** (`forgejo_data:/data`) → SSD | Yang paling besar |
| **Git LFS** (file besar) | **Cloudflare R2** (via Minio config) | Unlimited |
| **Actions artifacts** (CI output) | **Cloudflare R2** (via Minio config) | Unlimited |
| **PostgreSQL** (users, issues, PRs) | **Volume Docker** (`postgres_data`) → SSD | Kecil (<1GB) |
| **Runner cache** | **Volume Docker** (`runner_data`) → SSD | Bisa numpuk |

### Config R2 yang bener:

```yaml
FORGEJO__actions__ARTIFACT_STORAGE_TYPE: minio
FORGEJO__actions__MINIO_ENDPOINT: ${R2_ACCOUNT_ID}.r2.cloudflarestorage.com
FORGEJO__actions__MINIO_ACCESS_KEY_ID: ${R2_ACCESS_KEY_ID}
FORGEJO__actions__MINIO_SECRET_ACCESS_KEY: ${R2_SECRET_ACCESS_KEY}
FORGEJO__actions__MINIO_BUCKET: forgejo-actions
FORGEJO__actions__MINIO_LOCATION: auto
FORGEJO__actions__MINIO_USE_SSL: true

FORGEJO__lfs__STORAGE_TYPE: minio
FORGEJO__lfs__MINIO_ENDPOINT: ${R2_ACCOUNT_ID}.r2.cloudflarestorage.com
# ... sama kayak di atas
FORGEJO__lfs__MINIO_BUCKET: forgejo-lfs
```

### Isi Volume `forgejo_data:/data`:

```
forgejo_data/
└── data/
    ├── git/repositories/     ← Git objects, history code (YANG BESAR!)
    ├── forgejo/conf/         ← Config (kecil)
    ├── forgejo/attachments/  ← File attachment issue/PR
    ├── forgejo/avatars/      ← Avatar users (kecil)
    └── sessions/             ← Session data (kecil)
```

## Estimasi Ukuran

| Tipe Repo | Ukuran per Repo |
|-----------|----------------|
| Kode biasa (tanpa binary) | ~50-200MB (full history) |
| Dengan binary assets | ~500MB-2GB |
| Dengan LFS | LFS di R2, aman |

**Realita:** 512GB buat git data doang itu besar. 100 repo kode biasa cuma ~5-20GB.

**Yang beneran makan storage di MiniPC:**
1. ❌ **Docker build cache** — bisa 10-30GB
2. ❌ **Docker logs** — numpuk GB kalo ga di-rotate
3. ❌ **Old Docker images** — bekas upgrade

## Backup

### Level 1: Backup Docker Volumes

```bash
docker compose stop forgejo db
tar czf forgejo-backup-$(date +%Y%m%d).tar.gz \
  /var/lib/docker/volumes/forgejo_forgejo_data/ \
  /var/lib/docker/volumes/forgejo_postgres_data/
docker compose start
```

### Level 2: `forgejo dump` (Built-in)

```bash
docker exec forgejo forgejo dump \
  --tempdir /tmp \
  --database postgres \
  --skip-repository \
  -c /data/forgejo/conf/app.ini
```

Output: ZIP file di `/data/` — isinya config + database + semua repo.

### Level 3: Cron Backup ke R2

Jadwalin `forgejo dump` tiap minggu + upload ke R2.

## Storage Management

### Git GC & Repack (Compress 30-50%)

```bash
# Manual: compress semua repo
docker exec forgejo bash -c \
  "find /data/git/repositories -name '*.git' -exec git -C {} gc --aggressive \\;"
```

Auto-GC di `app.ini`:
```ini
[git]
GC_ARGS = --aggressive
AUTO_GC_INTERVAL = 100
```

### Bersihin Actions Artifacts

```bash
# Hapus artifacts >7 hari
docker exec forgejo forgejo actions artifacts-cleanup \
  --older-than 168h
```

### Runner Cache

```bash
docker exec forgejo-runner rm -rf /data/cache/*
```

### Mirror dengan Depth Terbatas (Alternatif)

Kalo storage kritis dan ga butuh full history:
```bash
git clone --bare --depth 50 https://github.com/user/repo.git
```

## Docker Build Cache — Masalah Utama

Kalo pake **docker-in-docker (dind)** di compose:

```yaml
docker-in-docker:
  image: docker:dind
  privileged: true
  command: ['dockerd', '-H', 'tcp://0.0.0.0:2375', '--tls=false']
```

Dind punya storage sendiri (`/var/lib/docker/` di dalam container). Tiap workflow jalan, **cache build numpuk terus dan tidak auto-terhapus**.

### Solusi: Cron `docker system prune`

Tambahin cron di host:

```bash
# Tiap Minggu jam 3 pagi — bersihin cache >24 jam
0 3 * * 0 docker exec forgejo-dind docker system prune -af --volumes --filter "until=24h"
```

Atau kalo pake Docker socket host (bukan dind):
```bash
0 3 * * 0 docker system prune -af --volumes --filter "until=24h"
```

### Level Agresif: Tiap Malam
```bash
0 2 * * * docker exec forgejo-dind docker system prune -af --volumes --filter "until=12h"
```

### Level Brutal: Restart Dind
```bash
0 3 * * 0 docker restart forgejo-dind
```
> Dind restart → storage dalem dind reset total. Tapi workflow berikutnya harus pull image dari awal.

### Tambahin Juga di Workflow
```yaml
- name: Cleanup Docker
  if: always()
  run: docker system prune -af --volumes
```

## Kapan Darurat? — Yang Terjadi Kalo Disk Penuh

| Komponen | Efek |
|----------|------|
| **PostgreSQL** | ❌ DB corruption — kalo disk penuh pas nulis |
| **Forgejo** | ❌ Gagal serve Git — clone/push error |
| **Mirror** | ❌ Gagal sync |
| **Docker** | ❌ Container crash |
| **Runner CI** | ❌ Gagal spawn job |
| **OS** | ❌ SSH login aja bisa gagal |

**Threshold:**
- 🟡 **80%** → peringatan, cleanup ringan
- 🔴 **90%** → darurat, aksi agresif
- 🆘 **95%+** → risikonya serius

## Cleanup Checklist — Dari Ringan ke Berat

| # | Action | Perintah | Efek |
|---|--------|----------|------|
| 1 | Docker system prune | `docker system prune -a --volumes` | Free 1-5GB+ |
| 2 | Truncate container logs | `truncate -s 0 /var/lib/docker/containers/*/*-json.log` | Free GB-an |
| 3 | Hapus artifacts lama | `forgejo actions artifacts-cleanup --older-than 168h` | Tergantung |
| 4 | Git GC all repos | `find ... -name '*.git' -exec git gc --aggressive` | Compress 30-50% |
| 5 | Hapus runner cache | `rm -rf /data/cache/*` | Tergantung |
| 6 | Hapus image ga kepake | `docker image prune -a` | Free GB-an |
| 7 | Hapus mirror repo | Lewat UI Forgejo | Tergantung size |
| 8 | Pindahin volume ke external | Stop → move → symlink | Free space lokal |

### Darurat Banget: Pindahin Volume ke External Storage

```bash
docker compose stop forgejo db
sudo mv /var/lib/docker/volumes/forgejo_forgejo_data /mnt/external/
sudo ln -s /mnt/external/forgejo_forgejo_data /var/lib/docker/volumes/
docker compose start
```
