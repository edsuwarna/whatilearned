---
title: Database Backup Guide — PostgreSQL, MySQL, MariaDB
description: - [MySQL & MariaDB](#mysql--mariadb)
---

# Database Backup Guide — PostgreSQL, MySQL, MariaDB

> **TL;DR:** Never use root for backups. Create a dedicated backup user with minimal privileges. Test restore regularly.

## Table of Contents

- [MySQL & MariaDB](#mysql--mariadb)
  - [Create Dedicated Backup User](#1-create-dedicated-backup-user)
  - [Per-Database Backup](#2-per-database-backup)
  - [All Databases Backup](#3-all-databases-backup)
  - [Compressed Backup (Recommended)](#4-compressed-backup-recommended)
  - [Restore](#5-restore)
  - [Important Flags](#6-important-flags)
- [PostgreSQL](#postgresql)
  - [Create Dedicated Backup User](#1-create-dedicated-backup-user-1)
  - [Per-Database Backup (Custom Format)](#2-per-database-backup-custom-format)
  - [All Databases (Cluster Level)](#3-all-databases-cluster-level)
  - [Compressed & Encrypted Backup](#4-compressed--encrypted-backup)
  - [Restore](#5-restore-1)
  - [Why Custom Format?](#6-why-custom-format-fc)
  - [Advanced: Parallel Backup](#7-advanced-parallel-backup-with-directory-format)
- [Automation Script](#automation-script)
  - [Cron Setup](#cron-setup-daily-backup)
- [Test Restore (Critical!)](#test-restore-critical)
- [Security Best Practices](#security-best-practices)
- [Tool Comparison](#tool-comparison)
- [Recommended Strategy](#recommended-strategy)

---

## MySQL & MariaDB

### 1. Create Dedicated Backup User

```sql
CREATE USER 'backup_user'@'localhost' IDENTIFIED BY 'strong-password';
GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER, RELOAD ON *.* TO 'backup_user'@'localhost';
FLUSH PRIVILEGES;
```

> **Permission breakdown:**
> - `SELECT` — read data
> - `LOCK TABLES` — consistent backup (non-InnoDB tables)
> - `SHOW VIEW` — backup view definitions
> - `EVENT` — backup event scheduler
> - `TRIGGER` — backup trigger definitions
> - `RELOAD` — required for `FLUSH` consistent snapshot

### 2. Per-Database Backup

```bash
mysqldump -u backup_user -p'strong-password' \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  dbname > dbname.sql
```

### 3. All Databases Backup

```bash
mysqldump -u backup_user -p'strong-password' \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --all-databases > all-dbs.sql
```

### 4. Compressed Backup (Recommended)

```bash
mysqldump -u backup_user -p'strong-password' \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  dbname | gzip > dbname-$(date +%Y%m%d).sql.gz
```

### 5. Restore

```bash
# Per-database
mysql -u root -p dbname < dbname.sql

# From compressed
gunzip < dbname.sql.gz | mysql -u root -p dbname

# All databases
mysql -u root -p < all-dbs.sql
```

### 6. Important Flags

| Flag | Purpose |
|---|---|
| `--single-transaction` | Consistent snapshot without locking (InnoDB). **Required.** |
| `--routines` | Backup stored procedures & functions |
| `--triggers` | Backup triggers |
| `--events` | Backup event scheduler |
| `--quick` | Prevent memory exhaustion for large tables |

> **Note:** `--single-transaction` only works with InnoDB. If you still have MyISAM tables, the backup will lock those tables. Migrate to InnoDB or schedule a maintenance window.

---

## PostgreSQL

### 1. Create Dedicated Backup User

```sql
CREATE USER backup_user WITH LOGIN REPLICATION PASSWORD 'strong-password';
GRANT pg_read_all_data TO backup_user;
```

> Alternative (more granular permissions):
> ```sql
> GRANT CONNECT ON DATABASE dbname TO backup_user;
> GRANT USAGE ON SCHEMA public TO backup_user;
> GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_user;
> GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO backup_user;
> ```

### 2. Per-Database Backup (Custom Format)

```bash
pg_dump -U backup_user -h localhost \
  -d dbname \
  -Fc \
  -f dbname.dump
```

### 3. All Databases (Cluster Level)

```bash
pg_dumpall -U backup_user -h localhost \
  -f all-dbs.sql
```

### 4. Compressed & Encrypted Backup

```bash
# Compressed SQL
pg_dump -U backup_user -h localhost -d dbname | gzip > dbname-$(date +%Y%m%d).sql.gz

# Custom format + compress level 9
pg_dump -U backup_user -h localhost -d dbname -Fc -Z 9 -f dbname.dump
```

### 5. Restore

```bash
# Custom format (supports parallel restore)
pg_restore -U postgres -h localhost -d dbname --jobs=4 dbname.dump

# SQL format
psql -U postgres -h localhost -d dbname < dbname.sql

# All databases
psql -U postgres -h localhost -f all-dbs.sql
```

### 6. Why Custom Format (`-Fc`)?

| Format | Pros | Cons |
|---|---|---|
| **Custom** (`-Fc`) | Compressed, parallel restore, selective restore per-table | Proprietary format |
| **Directory** (`-Fd`) | Parallel dump & restore, one file per table | Many files |
| **Plain SQL** (`-Fp`) | Human-readable, portable | Large, no parallel |
| **Tar** (`-Ft`) | Compressed | No parallel, rarely used |

> **Recommendation:** Use `-Fc` for daily backups. Keep a SQL-format copy for cross-version compatibility.

### 7. Advanced: Parallel Backup with Directory Format

```bash
pg_dump -U backup_user -h localhost -d dbname -Fd -j 4 -f dbname_dir/
```

---

## Automation Script

```bash
#!/bin/bash
# database-backup.sh — Backup all databases to compressed files

set -euo pipefail

BACKUP_DIR="/var/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7
DB_USER="backup_user"
DB_PASS="strong-password"
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
    db=$(echo "$db" | xargs)  # trim whitespace
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
# Run daily at 2 AM
0 2 * * * /usr/local/bin/database-backup.sh >> /var/log/database-backup.log 2>&1
```

---

## Test Restore (Critical!)

Backup without test restore = **false sense of security**. Schedule automated restore tests:

```bash
# Testing MySQL restore
mysql -u root -p -e "CREATE DATABASE test_restore;"
mysql -u root -p test_restore < backup.sql
# Verify data exists
mysql -u root -p test_restore -e "SELECT COUNT(*) FROM key_table;"
mysql -u root -p -e "DROP DATABASE test_restore;"
```

> **Best practice:** Test restore every 2 weeks. Record restore duration to estimate RTO (Recovery Time Objective).

---

## Security Best Practices

1. **Never store passwords in scripts** — use `.my.cnf` (MySQL) or `.pgpass` (PostgreSQL)
2. **Encrypt backups** before sending to remote storage
3. **Isolate backup user** — don't reuse the same user for applications
4. **Restrict backup user** — `localhost` only, never expose remotely
5. **Monitor backup jobs** — set up alerts for failures

### `.my.cnf` Example

```ini
[client]
user=backup_user
password=strong-password
```

Then set permissions: `chmod 600 ~/.my.cnf`

### `.pgpass` Example

```
localhost:5432:*:backup_user:strong-password
```

Then set permissions: `chmod 600 ~/.pgpass`

---

## Tool Comparison

| Tool | MySQL/MariaDB | PostgreSQL | Parallel | Compression | Encryption |
|---|---|---|---|---|---|
| `mysqldump` | ✅ Native | ❌ | ❌ | Pipe gzip | Manual |
| `pg_dump` | ❌ | ✅ Native | ✅ (`-j N`) | ✅ Built-in (`-Z`) | Manual |
| `mydumper` | ✅ | ❌ | ✅ | ✅ | Manual |
| `pg_dumpall` | ❌ | ✅ Cluster | ❌ | Manual | Manual |
| `xtrabackup` | ✅ (Percona) | ❌ | ✅ | ✅ | Manual |
| `pgBackRest` | ❌ | ✅ Advanced | ✅ | ✅ | ✅ Built-in |

---

## Recommended Strategy

```
Daily:   pg_dump -Fc (PG) + mysqldump --single-transaction (MySQL) → local disk
Weekly:  Same backup → upload to object storage (R2/S3) — encrypted
Monthly: Full dump archive → cold storage
Quarterly: Test restore from scratch — verify RTO
```

---

*See also: [Kopia backup guide](kopia-backup.md) — encrypted, incremental, dedup backup for VPS to Cloudflare R2.*
