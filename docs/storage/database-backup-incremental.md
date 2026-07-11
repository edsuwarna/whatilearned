---
title: Incremental Database Backup — PostgreSQL, MySQL, MariaDB
description: - [PostgreSQL](#postgresql)
---

# Incremental Database Backup — PostgreSQL, MySQL, MariaDB

> **TL;DR:** For incremental backups, use **pgBackRest** (PostgreSQL) or **Percona XtraBackup** (MySQL/MariaDB). Avoid `pg_dump`/`mysqldump` for incremental — they only do full backups.

## Table of Contents

- [PostgreSQL](#postgresql)
  - [Option 1: pgBackRest (Recommended)](#option-1-pgbackrest-recommended)
  - [Option 2: WAL Archiving (PITR)](#option-2-wal-archiving-pitr)
  - [Option 3: pg_probackup](#option-3-pg_probackup)
- [MySQL](#mysql)
  - [Option 1: Percona XtraBackup (Recommended)](#option-1-percona-xtrabackup-recommended)
  - [Option 2: Binary Log-Based](#option-2-binary-log-based-incremental)
- [MariaDB](#mariadb)
  - [Option: MariaDB Backup (Native)](#option-mariadb-backup-native)
- [Tool Comparison](#tool-comparison)
- [Recommended Strategy](#recommended-strategy)
- [Pitfalls](#pitfalls)

---

## PostgreSQL

PostgreSQL doesn't support incremental backup natively in `pg_dump`. You need **WAL archiving** + a dedicated tool.

### Option 1: pgBackRest (Recommended)

The most mature incremental backup tool for PostgreSQL. Supports full, differential, and incremental backups.

**Install:**
```bash
# Ubuntu/Debian
sudo apt install pgbackrest

# Configure /etc/pgbackrest/pgbackrest.conf
[mydb]
pg1-path=/var/lib/postgresql/16/main

[global]
repo1-path=/backups/pgbackrest
repo1-retention-full=2
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=your-encryption-key
```

**Usage:**
```bash
# Full backup (first time — required before incremental)
pgbackrest --stanza=mydb --type=full backup

# Incremental — only backs up changed pages since last backup
pgbackrest --stanza=mydb --type=incr backup

# Differential — backs up changed pages since last full backup
pgbackrest --stanza=mydb --type=diff backup

# Restore
pgbackrest --stanza=mydb restore

# List backups
pgbackrest --stanza=mydb info
```

**Key features:**
- Page-level delta checksums — only backs up changed 8KB pages
- Parallel backup & restore (`--process-max=4`)
- Built-in AES-256 encryption
- Compression (zstd, gzip, lz4)
- Backup validation on creation
- Point-in-Time Recovery (PITR)

### Option 2: WAL Archiving (PITR)

Free, built-in method. Full backup once, then continuously archive WAL segments.

**Configure:**
```ini
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backups/wal/%f'
archive_timeout = 60
```

**Backup strategy:**
```bash
# 1. Take base backup
pg_basebackup -U backup_user -D /backups/base/$(date +%Y%m%d) -X stream

# 2. WAL files are archived continuously by PostgreSQL

# 3. Clean old WALs
find /backups/wal -type f -mtime +7 -delete
```

**Restore to point-in-time:**
```bash
# 1. Restore base backup
# 2. Create recovery.conf:
restore_command = 'cp /backups/wal/%f %p'
recovery_target_time = '2026-07-04 12:00:00'

# 3. Start PostgreSQL — it replays WALs automatically
```

**Limitations:** Manual management. No compression, no encryption, no validation. WAL files can accumulate fast.

### Option 3: pg_probackup

From Postgres Professional — similar to pgBackRest.

```bash
# Init
pg_probackup init -B /backups/pg_probackup

# Full
pg_probackup backup -B /backups/pg_probackup --instance=mydb --backup-mode=FULL

# Delta (dirty page tracking)
pg_probackup backup -B /backups/pg_probackup --instance=mydb --backup-mode=DELTA

# Page-level incremental
pg_probackup backup -B /backups/pg_probackup --instance=mydb --backup-mode=PAGE
```

---

## MySQL

### Option 1: Percona XtraBackup (Recommended)

The de facto standard for MySQL incremental backups. Uses InnoDB page tracking.

**Install:**
```bash
# Percona repo
wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
sudo apt update
sudo apt install percona-xtrabackup-80
```

**Usage:**
```bash
# Full backup (first time)
xtrabackup --backup --target-dir=/backups/full \
  --user=backup_user --password=strong-password

# Incremental — only backs up changed pages since basedir
xtrabackup --backup --target-dir=/backups/inc1 \
  --incremental-basedir=/backups/full \
  --user=backup_user --password=strong-password

# Next incremental
xtrabackup --backup --target-dir=/backups/inc2 \
  --incremental-basedir=/backups/inc1 \
  --user=backup_user --password=strong-password
```

**Prepare & Restore:**
```bash
# Prepare full backup first (apply redo logs)
xtrabackup --prepare --apply-log-only --target-dir=/backups/full

# Apply incremental on top (do NOT use --apply-log-only for last inc)
xtrabackup --prepare --apply-log-only --target-dir=/backups/full \
  --incremental-dir=/backups/inc1

# Last incremental — finalize (without --apply-log-only)
xtrabackup --prepare --target-dir=/backups/full \
  --incremental-dir=/backups/inc2

# Restore (requires MySQL datadir to be empty)
xtrabackup --copy-back --target-dir=/backups/full
```

**Key features:**
- Page-level incremental (dirty page tracking)
- Non-blocking — hot backup without downtime
- Compression (`--compress=zstd`)
- Parallel threads (`--parallel=4`)
- Throttling for IO-heavy servers (`--throttle=100`)

### Option 2: Binary Log-Based Incremental

No extra tools — relies on MySQL binary logs.

**Enable binary logs:**
```ini
# my.cnf
log_bin = /var/log/mysql/mysql-bin.log
expire_logs_days = 7
binlog_format = ROW      # ✅ Use ROW format for consistency
```

**Backup binlog daily:**
```bash
# Show current binlog
mysql -u backup_user -p -e "SHOW MASTER STATUS\G"

# Backup all binlogs since last backup
mysqlbinlog --read-from-remote-server --host=localhost \
  --user=backup_user --password=strong-password \
  mysql-bin.000001 mysql-bin.000002 > incremental.sql

# Or stream continuously
mysqlbinlog --read-from-remote-server --host=localhost \
  --user=backup_user --password=strong-password \
  --raw --stop-never mysql-bin.000001 &
```

**Restore:** Apply base backup + all binlogs.
```bash
mysql -u root -p < full-backup.sql
mysql -u root -p < incremental.sql  # replay all binary logs
```

**Limitations:** No validation, no compression, sequential restore only. Only as good as your last base backup.

---

## MariaDB

### Option: MariaDB Backup (Native)

MariaDB 10.5+ ships with `mariabackup` — a fork of Percona XtraBackup with MariaDB compatibility fixes.

```bash
# Install (included with MariaDB server package)
sudo apt install mariadb-backup

# Full backup
mariabackup --backup --target-dir=/backups/full \
  --user=backup_user --password=strong-password

# Incremental
mariabackup --backup --target-dir=/backups/inc1 \
  --incremental-basedir=/backups/full \
  --user=backup_user --password=strong-password

# Prepare
mariabackup --prepare --apply-log-only --target-dir=/backups/full
mariabackup --prepare --target-dir=/backups/full \
  --incremental-dir=/backups/inc1

# Restore
mariabackup --copy-back --target-dir=/backups/full
```

> **Note:** Same interface as XtraBackup. If you already use XtraBackup for MySQL, `mariabackup` will feel identical.

---

## Tool Comparison

| Tool | PostgreSQL | MySQL | MariaDB | Incremental Level | Parallel | Compression | Encryption | PITR |
|---|---|---|---|---|---|---|---|---|
| **pgBackRest** | ✅ Native | ❌ | ❌ | Page delta | ✅ | ✅ | ✅ | ✅ |
| **pg_probackup** | ✅ Native | ❌ | ❌ | Page delta | ✅ | ✅ | ✅ | ✅ |
| **WAL Archive** | ✅ Built-in | ❌ | ❌ | WAL segment | ❌ | Manual | Manual | ✅ |
| **XtraBackup** | ❌ | ✅ Native | ✅ Fork | Page delta | ✅ | ✅ | ✅ | ✅ |
| **MariaDB Backup** | ❌ | ❌ | ✅ Native | Page delta | ✅ | ✅ | ✅ | ✅ |
| **Binlog** | ❌ | ✅ Built-in | ✅ Built-in | Row/Statement | ❌ | ❌ | ❌ | ✅ |

---

## Recommended Strategy

```
Frequency  | PostgreSQL          | MySQL/MariaDB
-----------|---------------------|---------------------
Daily      | pgBackRest incr     | XtraBackup incr
Weekly     | pgBackRest diff     | XtraBackup full
Monthly    | pgBackRest full     | XtraBackup full
Continuous | WAL archiving       | Binlog streaming
```

**RTO expectations:**
- Incremental restore: 1–5 minutes per 10GB
- Full restore from backup: 5–30 minutes per 10GB (depending on compression)
- PITR (replay WAL/binlog): 1–15 minutes per day of logs

---

## Pitfalls

### ⚠️ PostgreSQL

1. **WAL files accumulate** — set `archive_timeout` and clean regularly. A busy server generates 1–16 MB per minute.
2. **pgBackRest stanza misconfig** — test your stanza config before relying on it. Run `pgbackrest --stanza=mydb check`.
3. **Full backup required first** — incremental doesn't work without a full base.

### ⚠️ MySQL / MariaDB

1. **Prepare order matters** — you must prepare incrementals in sequence. Applying out of order corrupts the backup.
2. **Don't use `--apply-log-only` on the last incremental** — skip it for the final one so crash recovery runs.
3. **XtraBackup needs `pid-file` access** — make sure the MySQL pid file is readable by the backup user.
4. **Binlog disk space** — `binlog_format = ROW` generates larger logs than STATEMENT. Monitor disk usage.

### ⚠️ All

1. **Test incremental restore** — even more important than full backup testing. Incremental chains break silently.
2. **Don't mix tools** — pick one tool and stick with it. Mixing pgBackRest + pg_probackup causes confusion.
3. **Encrypt offsite backups** — incremental backups still contain all your data eventually.
4. **Monitor backup duration** — if incremental starts taking as long as full, take a new full backup.

---

*See also: [Database backup guide](database-backup.md) — full backup strategies, dedicated users, automation scripts.*
