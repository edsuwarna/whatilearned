# Database Backup Guide — PostgreSQL, MySQL, MariaDB

> **TL;DR:** Jangan pakai root user. Bikin dedicated backup user dengan minimal privilege. Test restore secara berkala.

---

## 🟢 MySQL & MariaDB

### 1. Buat Dedicated Backup User

```sql
CREATE USER 'backup_user'@'localhost' IDENTIFIED BY 'password-kuat';
GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER, RELOAD ON *.* TO 'backup_user'@'localhost';
FLUSH PRIVILEGES;
```

> **Penjelasan permission:**
> - `SELECT` — baca data
> - `LOCK TABLES` — konsisten backup (non-InnoDB)
> - `SHOW VIEW` — backup view definitions
> - `EVENT` — backup event scheduler
> - `TRIGGER` — backup trigger definitions
> - `RELOAD` — izin `FLUSH` untuk consistent snapshot

### 2. Backup Per-Database

```bash
mysqldump -u backup_user -p'password' \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  namadb > namadb.sql
```

### 3. Backup Semua Database

```bash
mysqldump -u backup_user -p'password' \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --all-databases > all-dbs.sql
```

### 4. Compressed Backup (Recommended)

```bash
mysqldump -u backup_user -p'password' \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  namadb | gzip > namadb-$(date +%Y%m%d).sql.gz
```

### 5. Restore

```bash
# Per-database
mysql -u root -p namadb < namadb.sql

# Dari compressed
gunzip < namadb.sql.gz | mysql -u root -p namadb

# All databases
mysql -u root -p < all-dbs.sql
```

### ⚠️ Penting untuk MySQL/MariaDB

| Flag | Fungsi |
|---|---|
| `--single-transaction` | Consistent snapshot tanpa locking (InnoDB). WAJIB. |
| `--routines` | Backup stored procedures & functions |
| `--triggers` | Backup triggers |
| `--events` | Backup event scheduler |
| `--quick` | Prevent memory exhaustion untuk large tables |

> **Catatan:** `--single-transaction` cuma work untuk InnoDB. Kalau masih ada tabel MyISAM, backup bakal lock tabel tersebut. Migrasi ke InnoDB atau siap-siap window maintenance.

---

## 🔵 PostgreSQL

### 1. Buat Dedicated Backup User

```sql
CREATE USER backup_user WITH LOGIN REPLICATION PASSWORD 'password-kuat';
GRANT pg_read_all_data TO backup_user;
```

> Alternatif (permission lebih granular):
> ```sql
> GRANT CONNECT ON DATABASE namadb TO backup_user;
> GRANT USAGE ON SCHEMA public TO backup_user;
> GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_user;
> GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO backup_user;
> ```

### 2. Backup Per-Database (Recommended: Custom Format)

```bash
pg_dump -U backup_user -h localhost \
  -d namadb \
  -Fc \
  -f namadb.dump
```

### 3. Backup All Databases (Cluster Level)

```bash
pg_dumpall -U backup_user -h localhost \
  -f all-dbs.sql
```

### 4. Compressed & Encrypted Backup

```bash
# Compressed SQL
pg_dump -U backup_user -h localhost -d namadb | gzip > namadb-$(date +%Y%m%d).sql.gz

# Custom format + compress level 9
pg_dump -U backup_user -h localhost -d namadb -Fc -Z 9 -f namadb.dump
```

### 5. Restore

```bash
# Custom format (bisa parallel restore)
pg_restore -U postgres -h localhost -d namadb --jobs=4 namadb.dump

# SQL format
psql -U postgres -h localhost -d namadb < namadb.sql

# All databases
psql -U postgres -h localhost -f all-dbs.sql
```

### 🔑 Kenapa Custom Format (`-Fc`)?

| Format | Kelebihan | Kekurangan |
|---|---|---|
| **Custom** (`-Fc`) | Compressed, parallel restore, selective restore per-table | Proprietary format |
| **Directory** (`-Fd`) | Parallel dump & restore, each table = file | Banyak file |
| **Plain SQL** (`-Fp`) | Human-readable, portable | Large, no parallel |
| **Tar** (`-Ft`) | Compressed, tapi gak bisa parallel | Jarang dipakai |

> **Recommendation:** Pake `-Fc` buat backup harian. Simpen SQL format untuk jaga-jaga compatibility.

### ⚙️ Advanced: Parallel Backup dengan Directory Format

```bash
pg_dump -U backup_user -h localhost -d namadb -Fd -j 4 -f namadb_dir/
```

---

## 📋 Automation Script

```bash
#!/bin/bash
# database-backup.sh — Backup all databases to compressed files

set -euo pipefail

BACKUP_DIR="/var/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7
DB_USER="backup_user"
DB_PASS="password-kuat"
PG_HOST="/var/run/postgresql"  # Unix socket

mkdir -p "$BACKUP_DIR/{mysql,postgres}"

# ── MySQL / MariaDB ──
echo "[$(date)] Backing up MySQL databases..."
databases=$(mysql -u"$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES;" | grep -Ev "(Database|information_schema|performance_schema|sys|mysql)")

for db in $databases; do
    mysqldump -u"$DB_USER" -p"$DB_PASS" \
        --single-transaction --routines --triggers --events \
        "$db" | gzip > "$BACKUP_DIR/mysql/${db}-${DATE}.sql.gz"
done

# ── PostgreSQL ──
echo "[$(date)] Backing up PostgreSQL databases..."
su - postgres -c "pg_dumpall -U backup_user -h $PG_HOST -f $BACKUP_DIR/postgres/all-dbs-${DATE}.sql"

# Backup each database individually in custom format
databases=$(psql -U backup_user -h $PG_HOST -t -c "SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres';")
for db in $databases; do
    db=$(echo "$db" | xargs)  # trim
    pg_dump -U backup_user -h $PG_HOST -d "$db" -Fc -f "$BACKUP_DIR/postgres/${db}-${DATE}.dump"
done

# ── Cleanup old backups ──
echo "[$(date)] Cleaning backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.dump" -type f -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.sql" -type f -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Backup complete."
```

### Cron Setup (Daily Backup)

```bash
# Backup tiap jam 2 pagi
0 2 * * * /usr/local/bin/database-backup.sh >> /var/log/database-backup.log 2>&1
```

---

## 🧪 Test Restore (Critical!)

Backup tanpa test restore = **ilusi keamanan**. Jadwalin test otomatis:

```bash
# Testing MySQL restore
mysql -u root -p -e "CREATE DATABASE test_restore;"
mysql -u root -p test_restore < backup.sql
# Verify data exists
mysql -u root -p test_restore -e "SELECT COUNT(*) FROM key_table;"
mysql -u root -p -e "DROP DATABASE test_restore;"
```

> **Best practice:** Test restore tiap 2 minggu sekali. Catat durasi restore biar tau estimasi RTO (Recovery Time Objective).

---

## 🔐 Security Best Practices

1. **Jangan simpan password di script** — pake `.my.cnf` (MySQL) atau `.pgpass` (PostgreSQL)
2. **Encrypt backup** sebelum kirim ke remote storage
3. **Isolasi backup user** — jangan pake user yang sama buat aplikasi
4. **Restrict backup user** — `localhost` only, jangan buka dari remote
5. **Monitor backup job** — pake alert kalau backup gagal

### Contoh `.my.cnf`

```ini
[client]
user=backup_user
password=password-kuat
```

Lalu set permission: `chmod 600 ~/.my.cnf`

### Contoh `.pgpass`

```
localhost:5432:*:backup_user:password-kuat
```

Lalu set permission: `chmod 600 ~/.pgpass`

---

## 📊 Perbandingan Tools

| Tool | MySQL/MariaDB | PostgreSQL | Parallel | Compression | Encryption |
|---|---|---|---|---|---|
| `mysqldump` | ✅ Native | ❌ | ❌ | Pipe gzip | Manual |
| `pg_dump` | ❌ | ✅ Native | ✅ (`-j N`) | ✅ Built-in (`-Z`) | Manual |
| `mydumper` | ✅ | ❌ | ✅ | ✅ | Manual |
| `pg_dumpall` | ❌ | ✅ Cluster | ❌ | Manual | Manual |
| `xtrabackup` | ✅ (Percona) | ❌ | ✅ | ✅ | Manual |
| `pgBackRest` | ❌ | ✅ Advanced | ✅ | ✅ | ✅ Built-in |

---

## 🚀 Recommended Strategy

```
Daily:   pg_dump -Fc (PG) + mysqldump --single-transaction (MySQL) → local disk
Weekly:  Same backup → upload ke object storage (R2/S3) — encrypted
Monthly: Full dump archive — cold storage
Quarterly: Test restore from scratch — verify RTO
```

---

*See also: [Kopia backup guide](kopia-backup.md) — encrypted, incremental, dedup backup for VPS to Cloudflare R2.*
