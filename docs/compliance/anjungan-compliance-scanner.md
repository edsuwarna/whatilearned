---
title: Anjungan Compliance Scanner
description: - [Overview](#overview)
---

# Anjungan Compliance Scanner


## Table of Contents

- [Overview](#overview)
- [CIS Level 1 (cis1)](#cis-level-1-cis1)
  - [Categories & Checks (40 total)](#categories-checks-40-total)
- [CIS Level 2 (cis2)](#cis-level-2-cis2)
  - [Additional Level 2 Checks](#additional-level-2-checks)
  - [When to Use Level 2](#when-to-use-level-2)
- [Lynis](#lynis)
  - [Prerequisites](#prerequisites)
  - [What Lynis Scans](#what-lynis-scans)
  - [Output Structure](#output-structure)
  - [How to Interpret Results](#how-to-interpret-results)
  - [Limitation](#limitation)
- [Scoring Formula](#scoring-formula)
  - [Score Tiers](#score-tiers)
  - [Lynis Scoring](#lynis-scoring)
- [References](#references)

Documentation for the compliance scanning system in Anjungan — covering scan profiles (CIS Level 1, CIS Level 2), category breakdown, and Lynis integration.

- **Author**: Anjungan IDP Team
- **Language**: Bilingual (EN/ID)

---

## Overview

Anjungan's compliance scanner runs **automated security checks** against remote Linux servers via SSH, modeled after the [CIS Distribution Independent Linux Benchmark](https://www.cisecurity.org/benchmark/distribution_independent_linux) and [Prowler](https://github.com/prowler-cloud/prowler)-style individual check execution.

Three scan modes are available:

| Scan Profile | Scope | Total Checks |
|---|---|---|
| **CIS Level 1** | Essential security baseline (automated or easily enforceable) | 40 checks |
| **CIS Level 2** | All Level 1 + advanced hardened controls | 53 checks |
| **Lynis** | External [Lynis](https://cisofy.com/lynis/) audit — separate tool | N/A (external) |

---

## CIS Level 1 (cis1)

> **Goal**: Foundational security posture — easy to implement, automated, low operational overhead.

CIS Level 1 checks are the **minimum security baseline** for any Linux server. Every check is:

- Automated — no manual intervention required to verify
- Non-disruptive — only reads config files or runs `sysctl`/`systemctl` queries
- Benchmark-referenced — mapped to specific CIS rule IDs

### Categories & Checks (40 total)

#### 🔐 SSH (`ssh`) — 18 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `ssh_password_auth` | SSH Password Auth | 5.2.1 | 🔴 critical | Checks if `PasswordAuthentication yes` — passwords are vulnerable to brute-force |
| `ssh_root_login` | SSH Root Login | 5.2.2 | 🔴 critical | Checks `PermitRootLogin` — direct root access bypasses audit trails |
| `ssh_port` | SSH Port | 5.2.3 | 🟡 medium | Warns if SSH is on default port 22 |
| `ssh_protocol` | SSH Protocol | 5.2.4 | 🟠 high | Ensures only Protocol 2 is allowed |
| `ssh_max_auth_tries` | MaxAuthTries | 5.2.5 | 🟡 medium | Ensures `MaxAuthTries ≤ 3` |
| `ssh_x11_forwarding` | X11 Forwarding | 5.2.7 | 🟡 medium | Checks `X11Forwarding` is disabled |
| `ssh_log_level` | LogLevel | 5.2.9 | 🟡 medium | Ensures `LogLevel` is INFO or VERBOSE |
| `ssh_hostbased_auth` | Hostbased Auth | 5.2.10 | 🟡 medium | Checks `HostbasedAuthentication` is disabled |
| `ssh_permit_empty_passwords` | Empty Passwords | 5.2.11 | 🔴 critical | Checks `PermitEmptyPasswords` is disabled |
| `ssh_ignore_rhosts` | IgnoreRhosts | 5.2.12 | 🟡 medium | Ensures `.rhosts` files are ignored |
| `ssh_banner` | SSH Banner | — | 🟡 medium | Checks if legal banner is configured |
| `ssh_max_startups` | MaxStartups | — | 🟡 medium | Limits concurrent unauthenticated connections |

**Level 1 SSH checks: 14 checks** (from 18 total SSH — 4 are Level 2)

#### 🧱 Kernel (`kernel`) — 6 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `kernel_reboot_required` | Reboot Required | 1.1 | 🟡 medium | Checks `/var/run/reboot-required` |
| `kernel_ip_forward` | IP Forwarding | 3.1.1 | 🟠 high | Checks `net.ipv4.ip_forward` is disabled |
| `kernel_icmp_redirects` | ICMP Redirects | 3.2.1 | 🟠 high | Ensures `accept_redirects=0` |
| `kernel_aslr` | ASLR | 1.6.1 | 🟠 high | Ensures `kernel.randomize_va_space=2` |
| `kernel_core_dumps` | Core Dumps | 1.5.1 | 🟡 medium | Ensures `fs.suid_dumpable=0` |
| `kernel_syn_cookies` | SYN Cookies | 3.3.1 | 🟡 medium | Ensures `net.ipv4.tcp_syncookies=1` |
| `kernel_icmp_ignore_broadcasts` | ICMP Broadcasts | 3.2.2 | 🟡 medium | Ensures broadcast echo is ignored |
| `kernel_martian_packets` | RP Filter | 3.2.3 | 🟡 medium | Ensures `rp_filter=1` (anti-spoofing) |

**Level 1 kernel checks: 8 checks** (all kernel checks are Level 1)

#### 📁 Filesystem (`filesystem`) — 6 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `fs_suid_home` | SUID Files in /home | 6.1.1 | 🟡 medium | Counts SUID files in user-writable dirs |
| `fs_ssh_world_readable` | World-Readable SSH | 6.2.1 | 🔴 critical | Checks `/root/.ssh` file permissions |
| `fs_authorized_keys_perms` | Authorized Keys | 6.2.2 | 🟡 medium | Verifies `authorized_keys` is `chmod 600` |
| `fs_shadow_perms` | /etc/shadow | 6.2.3 | 🔴 critical | Ensures shadow file is not world-readable |
| `fs_passwd_perms` | /etc/passwd | 6.2.4 | 🟡 medium | Ensures passwd is `644` |
| `fs_sticky_bit_tmp` | Sticky Bit /tmp | 6.1.2 | 🟠 high | Checks sticky bit is set on `/tmp` |

**Level 1 filesystem checks: 6 checks** (from 8 total — 2 are Level 2)

#### 👤 Users (`users`) — 5 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `users_empty_passwords` | Empty Passwords | 5.5.1 | 🟠 high | Checks `/etc/shadow` for blank passwords |
| `users_uid_zero` | UID 0 Accounts | 5.4.1 | 🔴 critical | Finds non-root accounts with UID 0 |
| `users_password_aging` | Password Aging | 5.4.1.1 | 🟡 medium | Ensures `PASS_MAX_DAYS ≤ 90` |
| `users_password_length` | Password Length | 5.4.1.2 | 🟡 medium | Ensures `PASS_MIN_LEN ≥ 14` |
| `users_duplicate_uids` | Duplicate UIDs | 6.2.5 | 🟡 medium | Checks for duplicate user IDs |
| `users_sudoers_config` | Sudoers Perms | 5.3.1 | 🟠 high | Ensures sudoers files are not world-writable |

**Level 1 users checks: 6 checks** (from 7 total — 1 is Level 2)

#### ⚙️ Services (`services`) — 5 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `svc_fail2ban` | Fail2ban Active | 2.2.1 | 🟠 high | Checks fail2ban service is running |
| `svc_auditd` | Auditd Running | 4.1.1 | 🟠 high | Checks auditd is installed and active |
| `svc_chrony_ntp` | NTP Sync | 2.2.1.1 | 🟡 medium | Checks time synchronization is enabled |
| `svc_package_updates` | Pending Updates | 1.7 | 🟠 high | Counts pending package updates (50+ = critical) |

**Level 1 services checks: 4 checks** (from 6 total — 2 are Level 2)

#### 🌐 Network (`network`) — 3 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `net_firewall_active` | Firewall Active | 3.5.1 | 🔴 critical | Checks UFW or iptables is active |
| `net_public_ports` | Public Ports | 3.5.2 | 🟡 medium | Lists services bound to `0.0.0.0` |
| `net_ufw_default_deny` | UFW Default Deny | 3.5.3 | 🟠 high | Ensures default policy is deny |

**Level 1 network checks: 3 checks** (from 5 total — 2 are Level 2)

#### 📝 Logging (`logging`) — 3 checks

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `log_rsyslog` | Rsyslog Running | 4.2.1 | 🟠 high | Checks rsyslog service is active |
| `log_logrotate` | Logrotate Configured | 4.3 | 🟡 medium | Checks `/etc/logrotate.conf` exists |

**Level 1 logging checks: 2 checks** (from 3 total — 1 is Level 2)

#### 🐳 Docker (`docker`) — 1 check

| Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|
| `docker_privileged` | Privileged Containers | Docker 5.4 | 🟠 high | Scans running containers for `--privileged` flag |

**Level 1 docker checks: 1 check** (from 2 total — 1 is Level 2)

---

## CIS Level 2 (cis2)

> **Goal**: Defense-in-depth — all Level 1 checks **plus** enhanced security controls that may require operational planning.

Level 2 includes everything from Level 1, plus the following **additional hardened checks** (13 checks):

### Additional Level 2 Checks

| Category | Check ID | Title | CIS Ref | Severity | What It Scans |
|---|---|---|---|---|---|
| `ssh` | `ssh_client_alive` | ClientAlive | 5.2.6 | 🟡 medium | Ensures idle sessions timeout |
| `ssh` | `ssh_allow_users` | AllowUsers | 5.2.8 | 🟡 medium | Restricts SSH to specific users |
| `ssh` | `ssh_ciphers` | Strong Ciphers | 5.2.13 | 🟠 high | Validates cipher configuration |
| `ssh` | `ssh_macs` | Strong MACs | 5.2.14 | 🟠 high | Validates MAC algorithm config |
| `ssh` | `ssh_kex` | Strong KEX | — | 🟠 high | Validates key exchange algorithms |
| `filesystem` | `fs_unowned_files` | Unowned Files | 6.1.3 | 🟡 medium | Finds orphaned files on system |
| `filesystem` | `fs_separate_partition` | Separate Partitions | 1.1.1 | 🟡 medium | Checks /tmp, /var, /home are separate |
| `users` | `users_home_perms` | Home Perms | 6.2.6 | 🟡 medium | Ensures no world-writable homes |
| `services` | `svc_cron_allowed` | Cron Allow | 5.1.1 | 🟡 medium | Ensures cron.allow restricts cron |
| `services` | `svc_unnecessary_services` | Unnecessary Svcs | 2.2.2 | 🟡 medium | Checks avahi, cups, bluetooth, etc. |
| `network` | `net_iptables_policy` | iptables Policy | 3.5.4 | 🟠 high | Ensures INPUT chain default is DROP |
| `network` | `net_unused_interfaces` | Unused Interfaces | 3.6 | 🟢 low | Detects down/unused interfaces |
| `logging` | `log_auditd_rules` | Audit Rules | 4.1.2 | 🟠 high | Ensures audit rules are loaded |
| `docker` | `docker_socket_perms` | Docker Socket | Docker 5.1 | 🟠 high | Ensures docker.sock is not world-readable |

### When to Use Level 2

Use Level 2 when:

- Servers are **public-facing** (internet-facing web apps, APIs)
- **Compliance requirements** mandate CIS Level 2 (PCI-DSS, SOC2)
- Servers handle **sensitive data** (PII, financial, credentials)
- **High-trust environments** where all services are known and controlled

⚠️ Some Level 2 checks may break existing workflows:
- `ssh_client_alive` can disconnect long-running SSH sessions
- `ssh_ciphers`/`ssh_macs` may break compatibility with older SSH clients
- `fs_separate_partition` requires partition-level changes

---

## Lynis

> **External tool**: [Lynis](https://cisofy.com/lynis/) is a mature open-source security auditing tool for Linux/Unix systems.

Anjungan runs Lynis on the remote server over SSH, parses the output, and extracts structured results.

### Prerequisites

Lynis must be installed on the target server:

```bash
# Debian/Ubuntu
sudo apt install lynis

# Or from CISOfy repo
sudo wget -O - https://packages.cisofy.com/keys/cisofy-software-public.key | sudo apt-key add -
sudo echo "deb https://packages.cisofy.com/community/lynis/deb/ stable main" > /etc/apt/sources.list.d/cisofy-lynis.list
sudo apt update && sudo apt install lynis
```

### What Lynis Scans

Lynis runs ~200–400 tests across these categories (parsed by Anjungan):

| Category | What It Checks |
|---|---|
| **Authentication** | Password policies, PAM config, SSH settings, sudoers |
| **Kernel** | Sysctl params, module loading, core dumps, SUID files |
| **Filesystem** | Permissions on sensitive files, mount options, ACLs |
| **Firewall** | iptables/nftables rules, UFW, firewalld |
| **Networking** | Open ports, DNS config, network stacks |
| **Services** | Running daemons, unnecessary services, Docker |
| **Logging** | Rsyslog, auditd, logrotate |
| **Software** | Package updates, installed tools, malware scans |
| **Custom** | Shell configs, home dirs, cron jobs, tmp files |

### Output Structure

```json
{
  "hardening_score": 75,
  "tests": 285,
  "plugins": 0,
  "warnings": 3,
  "suggestions": 12,
  "os_version": "Ubuntu 22.04",
  "hostname": "web-01",
  "warnings_list": [
    {
      "test_id": "TEST-1234",
      "category": "authentication",
      "description": "..."
    }
  ],
  "suggestions_list": [
    {
      "test_id": "TEST-5678",
      "category": "kernel",
      "description": "..."
    }
  ]
}
```

### How to Interpret Results

| Metric | Meaning | Good Range |
|---|---|---|
| **Hardening Score** | Overall security score (0–100) | > 70 |
| **Tests** | Number of checks performed | 250–400 |
| **Warnings** | High-severity issues found | < 5 |
| **Suggestions** | Medium/low recommendations | < 20 |

### Limitation

Lynis runs as a **separate scan** — not part of CIS scan. Results are stored separately and shown in the Lynis tab on the Compliance page.

---

## Scoring Formula

Anjungan calculates a **security score** for CIS scans:

```
score = 100 - (criticals × 15) - ((high + medium) × 5)
```

- Each **critical** failure: −15 points
- Each **high/medium** failure: −5 points
- Minimum score: 0
- All checks start at 100

### Score Tiers

| Score | Label |
|---|---|
| ≥ 90 | ✅ Good |
| 70–89 | ⚠️ Warning |
| < 70 | 🔴 Critical |

### Lynis Scoring

Lynis hardening score is produced by Lynis itself based on its own proprietary formula (not calculated by Anjungan).

---

## References

- [CIS Distribution Independent Linux Benchmark](https://www.cisecurity.org/benchmark/distribution_independent_linux)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Lynis — Security Auditing Tool](https://cisofy.com/lynis/)
- [Prowler — AWS Security Tool](https://github.com/prowler-cloud/prowler) (inspiration for single-check execution)
- [Mozilla OpenSSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
