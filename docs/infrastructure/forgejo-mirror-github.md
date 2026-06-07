# Mirror GitHub Repos ke Forgejo

> **Last updated:** 2026-06-07
> **Topik:** Cara mirror repo dari GitHub (public & private) ke Forgejo

## Table of Contents

- [Cara A: Via UI Forgejo (Recommended)](#cara-a-via-ui-forgejo-recommended)
- [Cara B: Via CLI (Manual One-Shot)](#cara-b-via-cli-manual-one-shot)
- [PAT Scopes](#pat-scopes)
- [Private → Public — Apa yang Terjadi?](#private--public--apa-yang-terjadi)

## Cara A: Via UI Forgejo (Recommended)

Ini cara termudah — auto-sync tiap 8 jam.

1. **Login ke Forgejo** → klik tombol **`+`** di kanan atas → **"Migrate External Repository"**
2. Isi form:
   - **Migrate Type:** `GitHub`
   - **Clone URL:** `https://github.com/user/repo.git`
   - **Owner:** pilih namespace (user / organisasi)
   - **Repository Name:** nama repo di Forgejo (bebas)
   - **Visibility:** Public / Private
   - ✅ **Centang "This repository will be a mirror"** — ini yang bikin auto-sync
   - **Authorization:**
     - **Public repo** → ga perlu token
     - **Private repo** → isi GitHub PAT (Personal Access Token)
   - **Mirror Interval:** default `8h0m0s` (tiap 8 jam)
3. Klik **"Migrate Repository"** → tunggu proses selesai.

Selesai! Forgejo otomatis sync dari GitHub sesuai interval yang diset.

## Cara B: Via CLI (Manual One-Shot)

```bash
# Clone mirror dari GitHub (bare repo — semua branch, tag, history)
git clone --mirror https://github.com/user/repo.git
cd repo.git

# Ganti remote ke Forgejo
git remote set-url origin https://git.domain.lu/user/repo.git

# Push semua (branch, tag, history)
git push --mirror origin

# Balik
cd ..
rm -rf repo.git
```

> ⚠️ **One-shot** — tidak auto-sync. Jalanin ulang `git push --mirror` kalo mau sync manual.

## PAT Scopes

### Classic PAT (`ghp_*`)

| Scope | Fungsi | Required? |
|-------|--------|-----------|
| **`repo`** | Akses private repo (baca semua isi) | ✅ **WAJIB** |
| `repo:status` | Commit status | Included |
| `repo_deployment` | Info deployment | Included |
| `public_repo` | Akses public repo | Included |
| `repo:invite` | Accept invites | Included |

**Minimal:** `repo` aja — udah mencakup semua sub-scope-nya.

### Fine-Grained PAT (Lebih Minimal)

| Scope | Required? |
|-------|-----------|
| **Contents** (Read-only) | ✅ Wajib |
| **Metadata** (Read-only) | ✅ Auto-include |

> Fine-grained lebih aman karena bisa dibatasi ke repo spesifik.

## Private → Public — Apa yang Terjadi?

Kalo repo berubah visibility:

| Skenario | Mirror di Forgejo |
|----------|------------------|
| Private → tetap Private | ✅ Jalan pake PAT |
| Private → Public | ✅ Tetap jalan (PAT ga diperlukan lagi) |
| Public → Private lagi | ✅ Masih jalan karena PAT masih valid |

**Intinya:** PAT tetap dibutuhkan cuma kalo repo private. Kalo repo jadi public, PAT diabaikan tapi ga masalah. Selama PAT lo valid, mirror aman.

> **Saran:** Kalo isi repo ga sensitif, mending buat public aja biar ga ribet urusan PAT expired.
