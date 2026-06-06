# Kopia: Backup dengan R2 di VPS

> Kopia: backup tool — incremental, dedup, encrypted. Cocok kombinasi sama **Cloudflare R2** untuk VPS dengan disk terbatas.


## Table of Contents

- [Quick Summary](#quick-summary)
- [Kenapa Kopia untuk IDP?](#kenapa-kopia-untuk-idp)
  - [1. Storage ke R2 Langsung](#1-storage-ke-r2-langsung)
  - [2. Dedup + Compression + Encryption (Default)](#2-dedup-compression-encryption-default)
  - [3. Snapshot (Point-in-time restore)](#3-snapshot-point-in-time-restore)
  - [4. Policy Retention (Auto Cleanup)](#4-policy-retention-auto-cleanup)
  - [5. Web UI](#5-web-ui)
- [Bandingin Backup Tools](#bandingin-backup-tools)
- [Skenario untuk VPS (4-8 GB RAM, 40GB Disk, R2)](#skenario-untuk-vps-4-8-gb-ram-40gb-disk-r2)
  - [Arsitektur Ideal](#arsitektur-ideal)
  - [Setup Cepat](#setup-cepat)
  - [Kapan Pake Kopia vs Lainnya](#kapan-pake-kopia-vs-lainnya)
- [Tips](#tips)

## Quick Summary

| | |
|---|---|
| **License** | ✅ **Apache 2.0** |
| **Bahasa** | Go (single binary ~30 MB) |
| **Storage** | R2, S3, B2, GCS, Azure, SFTP, lokal |
| **Dedup** | ✅ Chunk-level (default) |
| **Encryption** | ✅ AES-256-GCM (client-side) |
| **Compression** | ✅ Zstd (default) |
| **Web UI** | ✅ Built-in (`kopia server start`) |
| **Vendor** | Kopia Inc — opensource full (no proprietary layer) |
| **Stars** | 8.5K+ |

## Kenapa Kopia untuk IDP?

### 1. Storage ke R2 Langsung

```bash
kopia repository create s3 \
  --bucket=backup-bucket \
  --endpoint=https://<account-id>.r2.cloudflarestorage.com \
  --region=auto \
  --access-key=xxx \
  --secret-key=xxx
```

- Data langsung ke R2 — ga perlu intermediate storage
- Koneksi HTTPS langsung dari VPS ke Cloudflare
- R2 egress **gratis** — cocok buat restore

### 2. Dedup + Compression + Encryption (Default)

Kopia chunk semua file jadi ~4MB block, hash SHA256, simpan hanya block unik.

```
Snapshot v1: file1.txt, file2.txt  →  chunk A, B, C     (10 MB disimpan)
Snapshot v2: file1.txt (diedit), file2.txt (sama)  →  chunk A', C     (cuma 4 MB baru)

Total storage: 14 MB (bukan 20 MB)
```

- **Compression**: Zstd — kenceng, rasio bagus
- **Encryption**: AES-256-GCM — R2 ga bisa baca data lu
- Semua **on by default**, ga perlu config manual

### 3. Snapshot (Point-in-time restore)

Kopia record kondisi direktori di **waktu tertentu**. Bisa restore ke kondisi kemarin, minggu lalu, atau bulan lalu.

```bash
# Lihat semua snapshot
kopia snapshot list

# Restore file tertentu dari snapshot kemarin
kopia restore kopia://backup-bucket/path/to/snapshot /tmp/restore
```

Bisa juga **mount snapshot** sebagai FUSE filesystem:

```bash
kopia mount kopia://backup-bucket/path/to/snapshot /mnt/restore
```

### 4. Policy Retention (Auto Cleanup)

Setting global — Kopia otomatis hapus snapshot lama sesuai policy:

```bash
kopia policy set --global \
  --keep-latest 24 \
  --keep-hourly 48 \
  --keep-daily 30 \
  --keep-weekly 12 \
  --keep-monthly 12
```

Ga perlu script cron terpisah buat cleanup.

### 5. Web UI

```bash
kopia server start
```

Buka `http://localhost:51515` — bisa browse snapshot, restore file pilih-pilih.

## Bandingin Backup Tools

| | **Kopia** | **Restic** | **Borg** | **Duplicati** |
|---|---|---|---|---|
| **License** | ✅ Apache 2.0 | ✅ BSD | ✅ BSD-3 | ⚠️ AGPL-3.0 |
| **Single binary** | ✅ 30 MB | ✅ 20 MB | ❌ (Python) | ❌ (.NET) |
| **R2/S3 native** | ✅ | ✅ | ❌ (via rclone) | ✅ |
| **Dedup** | ✅ Chunk-level | ✅ Chunk-level | ✅ Fixed chunk | ✅ Block-level |
| **Encryption** | ✅ AES-256-GCM | ✅ AES-256 | ✅ AES-256 | ✅ AES-256 |
| **Compression** | ✅ Zstd (default) | ❌ (manual) | ✅ Zstd | ✅ |
| **Web UI** | ✅ Built-in | ❌ (3rd party) | ❌ | ✅ |
| **Retention** | ✅ Sangat rich | ✅ Basic | ✅ Basic | ✅ Rich |
| **Speed** | ⚡ Sangat cepat | ⚡ Cepat | ⚡ Cepat | 🐢 Lambat |

## Skenario untuk VPS (4-8 GB RAM, 40GB Disk, R2)

### Arsitektur Ideal

```
┌──────────────────────────────────────┐
│  Cron 02:00 + Cron 03:00            │
│                                      │
│  kopia snapshot create \             │
│    /home/ubuntu/projects             │  ← source code & config
│                                      │
│  kopia snapshot create \             │
│    /var/lib/docker/volumes           │  ← Postgres, Redis, dll
│                                      │
│  ── R2 ── encrypted + dedup ──────▶  │
│  (storage unlimited, data aman)      │
└──────────────────────────────────────┘
```

### Setup Cepat

```bash
# 1. Install
curl -s https://kopia.io/install.sh | bash

# 2. Init repository di R2
kopia repository create s3 \
  --bucket=kopia-backup \
  --endpoint=https://<account-id>.r2.cloudflarestorage.com/ \
  --region=auto \
  --access-key=xxx \
  --secret-key=xxx \
  --password=master-password-rahasia

# 3. Set global retention (hapus otomatis)
kopia policy set --global \
  --keep-latest 7 \
  --keep-daily 30 \
  --keep-weekly 12

# 4. Cron job (pastikan KOPIA_PASSWORD di env)
0 2 * * * /usr/local/bin/kopia snapshot create /home/ubuntu/projects
0 3 * * * /usr/local/bin/kopia snapshot create /var/lib/docker/volumes
```

### Kapan Pake Kopia vs Lainnya

| Kebutuhan | Pilihan |
|-----------|---------|
| Backup source code + config ke R2 | 🏆 **Kopia** — dedup, encrypt, retention |
| Backup database (dump file) ke R2 | 🏆 **Kopia** — kompres Zstd, chunk-level dedup |
| Backup volume Docker langsung | 🏆 **Kopia** — support direktori langsung |
| Archive besar (tahunan) ke R2 | 🏆 **Kopia + R2** — murah, unlimited |
| Sync real-time antar server | ❌ Kopia kurang cocok → pakai **rsync/SeaweedFS** |
| Database live backup (Point-in-Time) | ❌ Kopia ga bisa → pakai **pg_dump + Kopia** |

## Tips

- **Env variable**: `KOPIA_PASSWORD` — kalo ada di env, ga perlu `--password` tiap perintah
- **Cache**: Kopia cache metadata di `~/.cache/kopia/`. Bisa diarahkan ke `/tmp` kalo RAM cukup
- **Check snapshot**: `kopia snapshot verify` — verifikasi integritas semua snapshot
- **Migrasi repo**: Kopia export/import config — tinggal ganti endpoint buat pindah storage
- **Snapshot progress**: `kopia snapshot create --progress-interval=5s` buat liat progress real-time
- **Restore cepat**: `kopia restore --parallel=8` — paralel download dari R2
