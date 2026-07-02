---
title: OpenCode — Advanced Tips & Workflows
description: - [📋 Table of Contents](#table-of-contents)
---

# OpenCode — Advanced Tips & Workflows


## Table of Contents

- [📋 Table of Contents](#table-of-contents)
- [1. 🏠 Per-Project Commands](#1-per-project-commands)
  - [Directory Structure](#directory-structure)
  - [Usage](#usage)
  - [Example: Project Command](#example-project-command)
- [2. 🔗 Chained Commands (Pipelines)](#2-chained-commands-pipelines)
  - [Pipeline Command](#pipeline-command)
- [3. 🔥 Live Log Tailing + OpenCode](#3-live-log-tailing-opencode)
  - [Basic Patterns](#basic-patterns)
  - [Aliases for Quick Use](#aliases-for-quick-use)
  - [Pattern: Filter → Analyze](#pattern-filter-analyze)
- [4. 🖥️ Remote Server Analysis via SSH](#4-remote-server-analysis-via-ssh)
  - [One-Liner Health Check](#one-liner-health-check)
  - [Dedicated Command File](#dedicated-command-file)
- [5. 📊 Plan Mode for Architecture Decisions](#5-plan-mode-for-architecture-decisions)
  - [When to Use Plan Mode](#when-to-use-plan-mode)
  - [Examples](#examples)
  - [Pro Tip](#pro-tip)
- [6. 📁 Per-Directory `.opencoderc`](#6-per-directory-opencoderc)
  - [Example](#example)
  - [Benefits](#benefits)
- [7. 🚨 SRE Emergency Kit Commands](#7-sre-emergency-kit-commands)
  - [On-Call Handoff](#on-call-handoff)
  - [Post-Deploy Verification](#post-deploy-verification)
  - [Incident Timeline](#incident-timeline)
- [8. 🔌 MCP Servers (Direct Tool Execution)](#8-mcp-servers-direct-tool-execution)
  - [Configuration](#configuration)
  - [Recommended MCP Servers for Each Role](#recommended-mcp-servers-for-each-role)
  - [What MCP Enables](#what-mcp-enables)
  - [Installation](#installation)
- [9. ⚡ One-Shot Shell Aliases Summary](#9-one-shot-shell-aliases-summary)
- [10. 🔄 Workflow: Incident Response](#10-workflow-incident-response)
  - [Step 1: Alert Fires](#step-1-alert-fires)
  - [Step 2: Investigate](#step-2-investigate)
  - [Step 3: Mitigate](#step-3-mitigate)
  - [Step 4: Postmortem](#step-4-postmortem)
- [11. 🔄 Workflow: New Server Onboarding](#11-workflow-new-server-onboarding)
- [12. 🔄 Workflow: Zero-Downtime Deploy](#12-workflow-zero-downtime-deploy)
- [💡 Final Tips](#final-tips)

Advanced OpenCode patterns for DevOps, SRE, Cloud, Infrastructure, and full-stack developers who use it daily across multiple projects and servers.

> **Prerequisite**: Basic OpenCode setup with 9Router or direct API key. See [opencode-daily-use-cases](opencode-daily-use-cases.md) for fundamentals and [opencode-commands-by-role](opencode-commands-by-role.md) for role-specific commands.

---

## 📋 Table of Contents

- [1. Per-Project Commands](#1-per-project-commands)
- [2. Chained Commands (Pipelines)](#2-chained-commands-pipelines)
- [3. Live Log Tailing + OpenCode](#3-live-log-tailing-opencode)
- [4. Remote Server Analysis via SSH](#4-remote-server-analysis-via-ssh)
- [5. Plan Mode for Architecture Decisions](#5-plan-mode-for-architecture-decisions)
- [6. Per-Directory `.opencoderc`](#6-per-directory-opencoderc)
- [7. SRE Emergency Kit Commands](#7-sre-emergency-kit-commands)
- [8. MCP Servers (Direct Tool Execution)](#8-mcp-servers-direct-tool-execution)
- [9. One-Shot Shell Aliases Summary](#9-one-shot-shell-aliases-summary)
- [10. Workflow: Incident Response](#10-workflow-incident-response)
- [11. Workflow: New Server Onboarding](#11-workflow-new-server-onboarding)
- [12. Workflow: Zero-Downtime Deploy](#12-workflow-zero-downtime-deploy)

---

## 1. 🏠 Per-Project Commands

OpenCode loads commands from **both** global and project directories. Project-level commands take priority and stay relevant to that codebase.

### Directory Structure

```
~/.config/opencode/commands/     # Global — available everywhere
├── create-dockerfile.md
├── security-audit-config.md
├── generate-readme.md
└── ...

~/projects/anjungan/.opencode/commands/   # Project-specific
├── add-compliance-page.md
├── add-registry-user.md
├── fix-build.md
├── deploy-staging.md
└── docker-tag-push.md

~/projects/serversphere/.opencode/commands/
├── add-monitoring-page.md
├── fix-ssh-terminal.md
└── deploy-cf-pages.md
```

### Usage

Press **Ctrl+K** in the TUI — project commands appear first, then global ones. Context stays project-specific without `-f` flags.

### Example: Project Command

**`~/projects/anjungan/.opencode/commands/deploy-staging.md`**:

```markdown
# Deploy to Staging
Deploy the current branch to the staging server:
1. Build Docker images: `docker compose build`
2. Tag with SHA and `staging-latest`
3. Push to Zot registry at reg.edsuwarna.xyz
4. SSH to staging server and pull new images
5. Restart stacks with `docker compose up -d --force-recreate`
6. Run health checks on all endpoints
7. Rollback to previous images if health checks fail
```

No need to describe the project setup — the command lives inside the project.

---

## 2. 🔗 Chained Commands (Pipelines)

Group related commands into a **meta-command** that runs multiple prompts in sequence.

### Pipeline Command

**`deploy-full-stack.md`** (global):

```markdown
# Full Stack Deploy $SERVICE
Full deployment pipeline for $SERVICE:

Step 1 — Security audit all configs
Run `user:security-audit-config` on:
- Dockerfile, docker-compose.yml, .env.example
- nginx.conf, Caddyfile, Traefik config
- .github/workflows/*.yml
- any *.tf or Terraform files

Step 2 — Generate Docker setup
Run `user:create-dockerfile` for the service language
Include: .dockerignore, docker-compose.yml, health checks

Step 3 — Generate CI/CD
Run `user:create-github-actions` for:
- lint + test + build + scan + publish
- deploy to staging on PR
- deploy to production on tag/main

Step 4 — Generate deploy script
Run `user:create-deploy-script` with:
- zero-downtime strategy
- health check verification
- rollback on failure
- notification on completion
```

Run once → get 4 command outputs in sequence. Each output feeds context into the next.

---

## 3. 🔥 Live Log Tailing + OpenCode

Pipe **live logs directly** into OpenCode for real-time analysis. Works with any log source.

### Basic Patterns

```bash
# Docker logs
docker logs -f --tail 50 service-name 2>&1 | o9r \
  "Analyze these logs in real-time. Flag errors, warnings, and anomalies" -f -

# Journald
journalctl -fu docker.service -n 50 | o9r \
  "Why is Docker failing? Analyze these live logs" -f -

# Nginx access log
tail -f /var/log/nginx/access.log | o9r \
  "Analyze traffic patterns: 4xx/5xx spikes, slow requests, suspicious IPs" -f -

# Application error log
tail -f /var/log/app/error.log | o9r \
  "Monitor for critical errors and suggest immediate fixes" -f -
```

### Aliases for Quick Use

```bash
# ~/.zshrc
alias o9watch-docker='docker logs -f --tail 50 "$1" 2>&1 | o9r "Analyze logs in real-time" -f -'
alias o9watch-nginx='tail -f /var/log/nginx/error.log | o9r "Flag anomalies in nginx logs" -f -'
alias o9watch-app='journalctl -fu app.service -n 50 | o9r "Monitor app logs for errors" -f -'
```

### Pattern: Filter → Analyze

```bash
# Only pipe error-level logs
journalctl -fu docker.service -n 200 | grep -i "error\|fail\|panic\|oom\|killed" | o9r \
  "What's causing these Docker errors? Suggest fixes" -f -
```

---

## 4. 🖥️ Remote Server Analysis via SSH

Instead of SSH → copy-paste output → paste into OpenCode, pipe it directly.

### One-Liner Health Check

```bash
ssh bang-server "df -h && free -h && uptime && ps aux --sort=-%mem | head -10 && ss -tlnp" \
  | o9r "Analyze server health: flag issues and suggest fixes" -f -
```

### Dedicated Command File

**`remote-server-health.md`**:

```markdown
# Remote Server Health $HOST
SSH into $HOST and collect diagnostics together:
1. `df -h` — disk usage
2. `free -h` — memory pressure
3. `uptime` — load averages
4. `dmesg | tail -20` — kernel errors
5. `ss -tlnp` — listening ports
6. `docker ps --format '{{.Names}} {{.Status}}'` — container states
7. `journalctl -p err --since "24 hours ago" | tail -30` — recent errors

Then analyze everything together. Flag:
- Disk > 80%
- Memory pressure / swap usage
- Zombie / defunct processes
- Port conflicts
- Container restarts / crash loops
- Kernel errors (OOM, disk errors, network drops)

Suggest: cleanup targets, config fixes, scaling needs
```

Usage:

```bash
ssh bang-server "$(cat ~/.config/opencode/commands/remote-server-health.md)" \
  | o9r "Analyze server health from collected data" -f -
```

Or better — chain into a one-shot:

```bash
o9r "SSH to $HOST and run full health analysis" -f <(ssh bang-server \
  "df -h && free -h && uptime && dmesg | tail -20 && ss -tlnp && docker ps && journalctl -p err --since '24h ago' | tail -30")
```

---

## 5. 📊 Plan Mode for Architecture Decisions

Use `--agent plan` (or `o9p` alias) when the task requires **design before execution**. OpenCode will produce a plan, ask for approval, then implement.

### When to Use Plan Mode

| Situation | Without Plan Mode | With Plan Mode |
|-----------|-------------------|----------------|
| New architecture | Writes code immediately, might miss constraints | Designs first, explains trade-offs, asks for confirmation |
| Multi-service setup | Focuses on one service | Maps all services, dependencies, networking |
| Infrastructure design | Jumps to Terraform | Analyzes options (Terraform vs Pulumi vs manual) |
| Security audit | Flags issues one by one | Structured report with severity, impact, fix order |

### Examples

```bash
# Monitoring stack design
o9p 'Design the monitoring architecture for our VPS cluster:
  - 5 VPS nodes with Docker Compose services
  - Need: metrics, logs, alerts, dashboards
  - Constraints: minimal resource usage, self-hosted, no external SaaS
  - Current stack: Prometheus + Grafana on one node

  Output:
  - Architecture diagram (text)
  - Component choices with reasoning
  - Pros/cons of recommended vs alternatives
  - Estimated resource usage per component
  - Implementation order (what to set up first)'
```

```bash
# Database migration strategy
o9p 'Design migration strategy for:
  - Current: SQLite in each service container
  - Target: Central PostgreSQL with connection pooling
  - Constraints: zero-downtime, rollback possible, 5 services to migrate
  - Risk: data loss, connection leaks, performance regression

  Output step-by-step migration plan with verification at each step'
```

### Pro Tip

Use plan mode for **postmortem action items** too:

```bash
o9p "Based on this postmortem, design a prevention system:
  - What monitoring should have caught this earlier?
  - What architectural changes prevent recurrence?
  - What runbook entries are needed?
  - Priority order with effort estimates" -f postmortem.md
```

---

## 6. 📁 Per-Directory `.opencoderc`

Create a **`.opencoderc`** file in any project root to set default context for OpenCode sessions started in that directory.

### Example

**`~/projects/anjungan/.opencoderc`**:

```
# Provider endpoint (9Router)
LOCAL_ENDPOINT=http://localhost:20128/v1

# Default files to include in context
DEFAULT_FILES=src/,docker-compose.yml,.github/workflows/

# Always plan first for complex changes
AGENT_PLAN=true

# Custom instructions
INSTRUCTIONS=This is an Anjungan IDP project (Go + SvelteKit + Emerald). 
Use Docker Compose for local dev. Always check for existing patterns before 
creating new features.
```

### Benefits

- No need to specify `-f` or `--agent plan` every time
- OpenCode understands the project context automatically
- Different projects can have different defaults
- Works with shell aliases — `cd ~/projects/anjungan && o9` picks it up

---

## 7. 🚨 SRE Emergency Kit Commands

Commands designed for **incidents, handoffs, and post-deploy verification** — situations where every second counts.

### On-Call Handoff

**`oncall-handoff.md`**:

```markdown
# On-Call Handoff Summary
Prepare a complete on-call handoff report:

1. **Active Incidents**
   - What's currently ongoing?
   - What alerts fired during this shift?
   - Current status and mitigation steps taken

2. **Changes & Deploys**
   - What was deployed / changed during this shift?
   - Any pending rollbacks?
   - Maintenance windows scheduled?

3. **Watch Items**
   - What should the next on-call keep an eye on?
   - Known issues that aren't critical yet
   - Degraded but not alerting services

4. **Resources**
   - Links to relevant dashboards
   - Links to runbooks used
   - Escalation contacts
```

### Post-Deploy Verification

**`post-deploy-check.md`**:

```markdown
# Post-Deploy Verification $SERVICE
Verify that $SERVICE deployment was successful:

**Health**
- Health endpoint → 200 OK?
- All replicas started?
- Database migrations completed?

**Performance**
- Error rate: compare 5min before vs after deploy
- p50/p95/p99 latency: stable or regressed?
- CPU/Memory: within expected range?

**Logs**
- Any new error patterns?
- Warnings that weren't there before?
- Stack traces or panic logs?

**Rollback**
- Rollback plan ready?
- Rollback trigger criteria defined?
- Previous stable version still available?

**Result**: ✅ PASS or ❌ FAIL — with evidence for each check.
```

### Incident Timeline

**`incident-timeline.md`**:

```markdown
# Incident Timeline $INCIDENT_ID
Record the complete timeline for incident $INCIDENT_ID:

Format each entry as:
`[T+00:00] — Event description`

Key milestones to capture:
- Detection time and method (alert, user report, monitoring)
- Assessment start
- Root cause identified
- Mitigation started
- Service restored
- Monitoring verification period complete
- Incident declared resolved

For each entry note: who acted, what they did, what they observed.
```

---

## 8. 🔌 MCP Servers (Direct Tool Execution)

MCP (Model Context Protocol) servers give OpenCode **direct access** to tools — Docker, Kubernetes, databases, GitHub — so it can execute commands, not just suggest them.

### Configuration

Add to `~/.opencode.json`:

```json
{
  "mcpServers": {
    "docker": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-docker"
      ]
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-github"
      ]
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/mcp-server-postgres",
        "$DATABASE_URL"
      ]
    },
    "kubernetes": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "kubernetes-mcp-server"
      ]
    }
  }
}
```

### Recommended MCP Servers for Each Role

| MCP Server | Use Case | Role |
|------------|----------|------|
| `@anthropic/mcp-server-docker` | Manage containers, images, networks, volumes | DevOps / Infra |
| `@anthropic/mcp-server-github` | PRs, issues, repos, workflows | Developer / DevOps |
| `@modelcontextprotocol/mcp-server-postgres` | Query databases, run migrations, analyze schemas | Developer / SRE |
| `kubernetes-mcp-server` | `kubectl` operations — pods, services, deployments, logs | Cloud / SRE |
| `@anthropic/mcp-server-filesystem` | File operations, search, read/write with safety rules | All |
| `pulumi-mcp-server` | Infrastructure as Code with Pulumi | Cloud / Infra |
| `terraform-mcp-server` | Terraform plan, apply, destroy | Cloud / Infra |
| `grafana-mcp-server` | Query dashboards, alerts, incidents | SRE |
| `prometheus-mcp-server` | Query metrics, alert rules | SRE |

### What MCP Enables

**Without MCP** → OpenCode can only suggest: _"Run `docker ps` to check container status"_

**With Docker MCP** → OpenCode actually runs it:

```
Me: "Check why the API container keeps restarting"

OpenCode:
  → docker ps -a  → sees CrashLoopBackOff
  → docker logs api-container --tail 50 → sees OOMKilled
  → docker inspect api-container → sees memory limit 64MB
  → Suggests: increase memory limit to 128MB
  → docker compose up -d --force-recreate → fixes it
```

### Installation

Most MCP servers are available via npm:

```bash
# Docker MCP server
npx @anthropic/mcp-server-docker

# GitHub MCP server
npx @anthropic/mcp-server-github

# Postgres MCP server
npx @modelcontextprotocol/mcp-server-postgres

# Kubernetes MCP server
npx kubernetes-mcp-server
```

> Some MCP servers require authentication (GitHub token, database URL, kubeconfig). Configure these via environment variables in `~/.opencode.json`.

---

## 9. ⚡ One-Shot Shell Aliases Summary

These aliases let you skip the TUI entirely for recurring tasks.

```bash
# ── Log Analysis ──
alias o9watch-docker='docker logs -f --tail 50 "$1" 2>&1 | o9r "Analyze logs in real-time" -f -'
alias o9watch-app='journalctl -fu "$1" -n 50 | o9r "Monitor service logs" -f -'
alias o9watch-nginx='tail -f /var/log/nginx/error.log | o9r "Flag nginx anomalies" -f -'

# ── Remote Analysis ──
alias o9remote='ssh "$1" "df -h && free -h && uptime && docker ps && ss -tlnp" | o9r "Analyze server health" -f -'

# ── Deploy & Verify ──
alias o9deploy-check='o9r "Run post-deploy verification"'
alias o9incident-start='o9r "Log incident timeline and start response"'

# ── MCP shortcuts (if configured) ──
alias o9db='o9r "Query the database"'
alias o9k8s='o9r "Check Kubernetes cluster status"'
```

Add to `~/.zshrc`:

```bash
# Function for docker log watching with service name arg
o9watch() {
  local service=${1:-api}
  docker logs -f --tail 50 "$service" 2>&1 | o9r \
    "Monitor $service logs. Alert on errors, panics, and warnings" -f -
}

# Function for remote server analysis
o9ssh() {
  local host=$1
  [[ -z "$host" ]] && echo "Usage: o9ssh <host>" && return 1
  ssh "$host" "df -h && free -h && uptime && docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' && ss -tlnp && dmesg | tail -20" \
    | o9r "Full health analysis of $host" -f -
}
```

Usage:

```bash
o9watch api             # Tail docker logs for 'api' service
o9ssh bang-server       # SSH + health check + OpenCode analysis
```

---

## 10. 🔄 Workflow: Incident Response

End-to-end incident workflow using OpenCode.

### Step 1: Alert Fires

```bash
# Immediately capture context
o9 'Incident: API is returning 502 for all requests.
Snap current state: docker ps, docker logs api --tail 30, nginx error log tail.
Document what I see and suggest immediate triage steps.'
```

### Step 2: Investigate

```bash
# Deeper investigation with SSH + logs
o9ssh bang-server | o9r \
  "We have a 502 incident on the API service.
  Previous health check showed OOM issues.
  Check if containers are restarting, memory limits, and recent deploys."
```

### Step 3: Mitigate

```bash
o9r "API is down with 502. 
Based on investigation:
- Container keeps restarting (OOMKilled)
- Recent deploy added memory-heavy dependency
- Memory limit is 128MB

I need to:
1. Increase memory limit to 256MB
2. Restart the stack
3. Verify health returns
4. Identify the memory leak from recent changes

Do it step by step." -f docker-compose.yml
```

### Step 4: Postmortem

```bash
o9r "Generate a postmortem for today's API 502 outage.
Timeline: 14:02 alert → 14:10 identified OOM → 14:15 increased limit → 14:18 restored.
Root cause: New dependency added without memory budget review.
Impact: 16 minutes of 502s, ~2K failed requests.

Structure: Summary, Timeline, Root Cause, Action Items." | o9p
```

---

## 11. 🔄 Workflow: New Server Onboarding

OpenCode as your provisioning checklist.

```bash
o9 'I am provisioning a new Ubuntu 24.04 server at 203.0.113.50.
Generate the complete setup script:

1. Initial hardening:
   - Update all packages
   - Set hostname to "worker-01"
   - Configure timezone UTC + NTP
   - SSH hardening (key-only, disable root, custom port, fail2ban)
   - UFW: allow SSH, HTTP, HTTPS only

2. Docker installation (official repo, not Ubuntu apt)
3. Docker daemon config: log rotation, metrics, live-restore
4. Monitoring: node_exporter as systemd service
5. Security: unattended-upgrades, auditd, rkhunter

Output as a single bash script with echo statements for each step
and error handling (set -e, trap).
'
```

---

## 12. 🔄 Workflow: Zero-Downtime Deploy

```bash
o9p "Design a zero-downtime deployment workflow for a Docker Compose stack:

Services:
- api (Go) — 3 replicas behind Traefik
- web (SvelteKit) — static files served by nginx
- postgres (managed externally, not in compose)

Requirements:
- No dropped requests during deploy
- Health check before routing traffic
- Rollback in under 2 minutes if health check fails
- Graceful shutdown (SIGTERM, drain connections)
- Deploy via GitHub Actions triggered by git tag

Output: step-by-step workflow with actual compose config,
Traefik labels, health check endpoints, and GitHub Actions YAML"
```

---

## 💡 Final Tips

| Pattern | Why It Works |
|---------|-------------|
| **Plan first, code second** | `o9p` prevents costly wrong turns in architecture decisions |
| **Pipe live data** | OpenCode analyzes real output, not assumptions |
| **Per-project commands** | Context automatically matches the project |
| **SSH + OpenCode** | Diagnosis without leaving your terminal |
| **MCP servers** | OpenCode executes, not just suggests |
| **Emergency kit commands** | No thinking during incidents — just run the command |
| **Function aliases** | `o9ssh host` beats SSH → copy → paste → type |

---

*Last updated: June 2026*
