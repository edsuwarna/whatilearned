# OpenCode Commands by Role

**OpenCode** supports **Custom Commands** — reusable `.md` prompt files stored in `~/.config/opencode/commands/` (global) or `<project>/.opencode/commands/` (per-project). Accessed via **Ctrl+K** in the TUI.

This reference collects battle-tested commands organized by engineering role. Each command is a ready-to-save `.md` file.

> **Setup**: Create any of these files under `~/.config/opencode/commands/` to make them available across all projects. Or put them in `<project>/.opencode/commands/` for project-specific commands.

---

## 📋 Table of Contents

- [Developer](#developer)
- [DevOps Engineer](#devops-engineer)
- [SRE](#sre)
- [Cloud Engineer](#cloud-engineer)
- [Infrastructure Engineer](#infrastructure-engineer)
- [Cross-Role Utilities](#cross-role-utilities)
- [Shell Aliases for Quick Access](#shell-aliases-for-quick-access)

---

## 👨‍💻 Developer

### `generate-api-endpoint.md`

```markdown
# Generate API Endpoint $NAME
Generate a complete REST API endpoint for $NAME following the project's patterns.
Include:
- Route/handler definition
- Request validation (zod / Joi / Pydantic)
- Service layer with business logic
- Repository/data access layer
- Error handling (400, 404, 500)
- Unit tests for success and error cases
- OpenAPI/Swagger docs if applicable

Check existing endpoints in the project to match conventions.
```

### `debug-error.md`

```markdown
# Debug Error
I'm seeing this error. Find the root cause and suggest a fix:
- What is the exact failure point?
- What assumptions led to the bug?
- What's the minimal fix?
- Are there related patterns in the codebase that could have the same bug?

Fix the code if the solution is clear and contained.
```

### `refactor-file.md`

```markdown
# Refactor $FILE
Refactor $FILE for better maintainability:
- Split into smaller focused modules if >200 lines
- Extract reusable functions
- Remove dead code and unused imports
- Simplify complex conditionals
- Add TypeScript/Python type hints
- Name magic numbers and strings as constants
- Keep the same public API contract

Use --agent plan for large refactors.
```

### `write-tests.md`

```markdown
# Write Tests for $FILE
Write comprehensive tests for $FILE covering:
- Success path (happy case)
- Validation errors (bad input, missing fields)
- Edge cases (empty state, boundary values)
- Error states (not found, server error, timeout)
- If async: loading states, race conditions

Follow the existing test framework and patterns in the project.
Generate the test file at the corresponding test path.
```

### `database-migration.md`

```markdown
# Database Migration $NAME
Create a database migration for: $NAME
Include:
- Up and down migrations
- Appropriate indexes for query patterns
- Foreign key constraints with ON DELETE behavior
- NOT NULL / DEFAULT considerations
- Type mapping (migrate existing data if column changed)

Name the file following the project's migration naming convention.
```

### `code-review.md`

```markdown
# Code Review $FILE
Review this file for:
- Logic bugs and off-by-one errors
- Security vulnerabilities (injection, XSS, auth bypass)
- Performance issues (N+1 queries, memory leaks)
- Error handling gaps (uncaught exceptions, swallowed errors)
- Type safety (any, type casting, missing null checks)
- Code style drift from project conventions
- Test coverage gaps

Rate each finding: critical / major / minor.
```

### `generate-commit-message.md`

```markdown
# Generate Commit Message
Generate a concise conventional commit message from this diff.
Format: type(scope): description

Types: feat, fix, refactor, chore, docs, test, perf, security
Keep the subject line under 72 characters.
Include a body with rationale if the change is non-trivial.
```

### `generate-docs.md`

```markdown
# Generate Documentation for $FILE
Generate documentation for $FILE covering:
- What this module/component does (purpose, not implementation)
- Public API surface (exports, props, params, return types)
- Key design decisions and trade-offs
- Usage examples
- Dependencies and side effects
- Related files

Output in project-standard markdown format.
```

---

## 🐳 DevOps Engineer

### `create-dockerfile.md`

```markdown
# Create Dockerfile for $LANGUAGE
Create a production-grade Dockerfile for a $LANGUAGE project:
- Multi-stage build (builder + runtime)
- Minimal final image (distroless or alpine)
- Proper layer caching (dependencies before source)
- Non-root user
- HEALTHCHECK instruction
- .dockerignore reference
- Security scanning labels

Add docker-compose.yml with postgres/redis if needed.
```

### `optimize-dockerfile.md`

```markdown
# Optimize Dockerfile
Review this Dockerfile for:
- Layer count and caching efficiency
- Image size reduction opportunities
- Security concerns (root user, exposed secrets, CVEs in base image)
- Build time optimization
- Multi-stage opportunities
- Using pinned base image tags

Suggest specific changes with before/after comparison.
```

### `create-github-actions.md`

```markdown
# Create GitHub Actions Workflow $NAME
Create a GitHub Actions workflow for: $NAME
Choose the right trigger (push, PR, schedule, manual dispatch).

Include appropriate jobs:
- Lint (ESLint, golangci-lint, ruff)
- Test (unit + integration)
- Build (Docker image or artifact)
- Scan (trivy, Snyk, CodeQL)
- Publish (GHCR, Docker Hub, npm)
- Deploy (SSH, Cloudflare, Kubernetes)

Use matrix builds for multi-version or multi-arch.
Pin action versions by SHA.
```

### `docker-compose-stack.md`

```markdown
# Docker Compose Stack $NAME
Create docker-compose.yml for: $NAME

Include:
- Service definitions with health checks
- Network configuration (internal/external)
- Volume mounts with proper permissions
- Environment variable management (.env)
- Resource limits (CPU, memory)
- Restart policies
- Traefik/Caddy reverse proxy labels if needed

Add a .env.example with documented variables.
```

### `security-audit-config.md`

```markdown
# Security Audit Config $FILE
Audit this config file for security issues:
- Exposed secrets, tokens, passwords
- Weak TLS/crypto settings
- Missing security headers
- Permissive CORS
- Rate limiting gaps
- Authentication bypass vectors
- Privilege escalation paths

For each finding: severity, impact, fix suggestion.
```

### `deploy-script.md`

```markdown
# Create Deploy Script
Create a deploy.sh script that:
1. Pulls latest code
2. Installs dependencies
3. Runs database migrations
4. Builds artifacts / Docker images
5. Restarts services (graceful, zero-downtime)
6. Health check after deploy
7. Rollback on failure (restore previous version)
8. Notifies on success/failure

Handle: locking (prevent concurrent deploys), logging, cleanup.
```

### `ci-debug.md`

```markdown
# Debug CI Failure
Analyze this CI/CD pipeline failure:
- At which step did it fail?
- Is it a code issue, config issue, or infrastructure issue?
- Flaky test or real regression?
- Environment difference from local?

Examine the log and config together to pinpoint root cause.
Suggest a minimal fix and a preventative measure.
```

---

## 🚨 SRE

### `incident-response.md`

```markdown
# Incident Response: $ALERT
An alert fired: $ALERT

Analyze the situation:
1. What's the blast radius? (users, services, data)
2. Is this a degradation or outage?
3. What changed recently? (deploys, config changes, traffic spikes)
4. Run checklist for this alert type:
   - Check metrics dashboard
   - Check logs for error spikes
   - Check upstream dependencies
   - Check recent deployments
5. Mitigation steps in order of reversibility
6. Escalation criteria

Document findings for postmortem.
```

### `sli-slo-review.md`

```markdown
# SLO Review: $SERVICE
Review the SLI/SLO data for $SERVICE:
- Current burn rate vs budget
- Error budget remaining
- Which indicators are approaching threshold?
- Correlate with recent changes (deploys, configs)
- Suggest SLO adjustments if consistently overshot or undershot
- Recommend reliability investments based on gap analysis

Include: latency SLIs, error rate SLIs, availability SLIs.
```

### `postmortem-draft.md`

```markdown
# Postmortem Draft: $INCIDENT
Draft a postmortem for the $INCIDENT incident:

Structure:
- **Summary**: what happened, impact, duration
- **Timeline**: detection → response → mitigation → resolution
- **Root Cause**: technical explanation
- **Contributing Factors**: why it wasn't caught earlier
- **Detection**: how was it found? How could it be faster?
- **Response**: what went well, what didn't
- **Action Items**: owner, type (mitigate/prevent/detect), timeline
- **Lessons Learned**: systemic improvements

Blame-free, factual tone. Focus on process not people.
```

### `runbook-generate.md`

```markdown
# Generate Runbook: $SERVICE
Write a runbook for $SERVICE covering:

1. **Service Overview**: purpose, architecture, dependencies
2. **Critical Metrics**: what to watch, dashboards
3. **Common Alerts**: alert meaning, likely causes, first steps
4. **Diagnosis Steps**: logs to check, commands to run
5. **Recovery Procedures**: step-by-step with rollback
6. **Escalation Path**: who to contact, when
7. **Maintenance**: restarts, upgrades, migrations
8. **Disaster Recovery**: worst case scenario recovery plan

Keep it actionable — someone waking up at 3am should be able to follow it.
```

### `capacity-planning.md`

```markdown
# Capacity Review: $SERVICE
Analyze capacity for $SERVICE:

1. **Current usage**: CPU, memory, disk, network, connections
2. **Growth trend**: 7-day, 30-day, 90-day trajectory
3. **Peak analysis**: daily/weekly/seasonal patterns
4. **Headroom**: how much runway before saturation?
5. **Bottlenecks**: which resource hits limit first?
6. **Cost impact**: current spend, projected spend
7. **Recommendations**: scale up/down/out, reservations, vertical/horizontal

Use data from monitoring system; flag any missing metrics.
```

### `chaos-run.md`

```markdown
# Chaos Experiment: $EXPERIMENT
Design a chaos engineering experiment for: $EXPERIMENT

Plan:
- **Hypothesis**: the system will (still work / degrade gracefully / fail in X way)
- **Blast radius**: what services/users are affected
- **Experiment type**: (network partition / pod kill / latency injection / resource exhaustion / DNS failure)
- **Steady state**: how to verify system is healthy before experiment
- **Run**: specific steps to inject fault
- **Rollback**: how to restore immediately
- **Observability**: which metrics and logs to watch during experiment
- **Success criteria**: what "passed" means

Start small and expand — game day over production blast.
```

### `performance-analysis.md`

```markdown
# Performance Analysis: $SCOPE
Analyze performance data for $SCOPE:

1. **Latency**: p50, p95, p99, p999 — trends and spikes
2. **Throughput**: requests per second, concurrent connections
3. **Error rate**: 4xx/5xx trends, correlation with latency
4. **Resource usage**: CPU, memory, disk I/O, network
5. **Hotspots**: which endpoint/query/service is slowest?
6. **Bottlenecks**: database, lock contention, GC, TLS handshake

Compare against SLO targets. Flag regressions with before/after data.
```

---

## ☁️ Cloud Engineer

### `terraform-module.md`

```markdown
# Create Terraform Module $NAME
Create a Terraform module for: $NAME

Follow best practices:
- Input variables with descriptions, types, and defaults
- Outputs for all useful attributes
- Tags propagated to all resources
- Remote state locking (DynamoDB / GCS / Azure Storage)
- Provider version pinning
- Resource naming convention consistent with project
- Sensitive outputs marked as sensitive
- locals for computed values
- data sources for existing infrastructure

Include examples/ directory with usage.
```

### `terraform-plan-review.md`

```markdown
# Review Terraform Plan $NAME
Review this Terraform plan/output for $NAME:

Check for:
- Resource destruction that looks accidental
- IAM permission changes (overly permissive)
- Security group / firewall rule changes
- State lock / migration issues
- Variable interpolation errors
- Missing tags
- Provider compatibility
- Drift from expected state

Flag anything that could cause downtime or security exposure.
```

### `kubernetes-manifest.md`

```markdown
# Create Kubernetes Manifest $NAME
Create a Kubernetes manifest for: $NAME

Include:
- Deployment with resource requests/limits
- Service (ClusterIP / NodePort / LoadBalancer)
- ConfigMap for non-sensitive config
- Secret for sensitive data
- Ingress with TLS
- HorizontalPodAutoscaler
- PodDisruptionBudget
- NetworkPolicy
- liveness, readiness, startup probes
- ServiceAccount with minimal RBAC
- Labels and annotations for observability

Use apps/v1 API versions. Pin container image tags (not latest).
```

### `k8s-debug.md`

```markdown
# Debug Kubernetes Issue: $NAMESPACE/$POD
Debug this Kubernetes issue in namespace $NAMESPACE:

Run diagnostics:
1. Pod status and events: `kubectl describe pod $POD -n $NAMESPACE`
2. Container logs: `kubectl logs $POD -n $NAMESPACE --tail=100`
3. Previous instance logs (if restarted): `kubectl logs $POD -n $NAMESPACE -p --tail=50`
4. Node resources: `kubectl top pod $POD -n $NAMESPACE`
5. Service endpoints: `kubectl get endpoints -n $NAMESPACE`

Common issues to check:
- ImagePullBackOff / CrashLoopBackOff / OOMKilled
- Readiness probe failures
- Resource limits too low
- ConfigMap/Secret not mounted
- Network policy blocking traffic
- PVC not bound
```

### `iam-policy-review.md`

```markdown
# Review IAM Policy $NAME
Review this IAM policy for security best practices:

Check for:
- Wildcard actions (s3:*, ec2:*, etc.)
- Wildcard resources ('*')
- Overly permissive trust relationships (Principal: '*')
- Unused or deprecated actions
- Missing condition keys (source IP, MFA, encryption)
- Privilege escalation risks (iam:PassRole + ec2:RunInstances)
- Least privilege violations

Suggest specific policy refinements.
```

### `cloud-cost-analyze.md`

```markdown
# Cloud Cost Analysis: $SERVICE
Analyze cloud costs for $SERVICE:

1. **Top spenders**: which resources cost the most?
2. **Idle resources**: unattached IPs, unused volumes, idle instances
3. **Reservation coverage**: RI/SP utilization
4. **Right-sizing**: over-provisioned instances
5. **Storage optimization**: lifecycle policies, object tiers
6. **Data transfer costs**: inter-region, egress
7. **Recommendations**: savings estimate for each

Flag: resources without tags (cost allocation gaps).
```

### `vpc-network-review.md`

```markdown
# Review VPC/Network Config: $NAME
Review this network configuration for $NAME:

- Subnet sizing and AZ distribution
- Route tables (is there a default route? to NATGW or IGW?)
- NACL rules (ephemeral ports?)
- Security group rules (too permissive IP ranges?)
- VPC endpoints for S3/ECR (avoid NAT costs)
- Flow logs enabled?
- Transit Gateway / VPC peering connectivity
- DNS resolution and Private Hosted Zones

Flag overly permissive 0.0.0.0/0 rules, cross-subnet traffic gaps.
```

---

## 🏗️ Infrastructure Engineer

### `server-provision.md`

```markdown
# Server Provisioning Checklist: $HOST
Provision $HOST. Run this checklist:

**Initial Setup**
- [ ] OS update & security patches
- [ ] Hostname set
- [ ] Timezone configured (UTC)
- [ ] NTP configured (chrony/systemd-timesyncd)
- [ ] SSH: key-only, disable root login, custom port, fail2ban
- [ ] Firewall: UFW/nftables with minimal rules
- [ ] Swap configured (or disabled for K8s)
- [ ] Kernel parameters (net.core.somaxconn, vm.swappiness, etc.)

**Monitoring**
- [ ] Node exporter installed
- [ ] Prometheus metrics endpoint enabled
- [ ] Log shipping to central system
- [ ] Disk alert thresholds set

**Security**
- [ ] Automatic security updates enabled
- [ ] Auditd installed and configured
- [ ] AIDE / Tripwire integrity checking
- [ ] Docker daemon config (if applicable)
- [ ] CloudWatch / OpsAgent / Telegraf installed
```

### `dns-debug.md`

```markdown
# DNS Troubleshooting: $DOMAIN
Troubleshoot DNS for $DOMAIN:

1. **Resolution check**: `dig +short $DOMAIN`, `dig +short www.$DOMAIN`
2. **Record types**: `dig $DOMAIN A`, `dig $DOMAIN AAAA`, `dig $DOMAIN MX`, `dig $DOMAIN TXT`
3. **NS delegation**: `dig $DOMAIN NS +short` — are all nameservers responding?
4. **Propagation**: check multiple resolvers (Cloudflare 1.1.1.1, Google 8.8.8.8, local)
5. **TTL**: how long until changes propagate?
6. **DNSSEC**: `dig $DOMAIN DNSKEY` — is validation passing?
7. **Reverse DNS**: `dig -x <IP>`
8. **CAA records**: `dig $DOMAIN CAA` (which CAs can issue certs?)

Common issues: stale glue records, missing SPF/DKIM/DMARC, split-brain DNS.
```

### `nginx-tls-setup.md`

```markdown
# Nginx + TLS Setup: $DOMAIN
Generate an Nginx config for $DOMAIN with:

- TLS 1.3 only (or TLS 1.2+)
- Strong ciphers (Mozilla intermediate/modern profile)
- HTTP → HTTPS redirect
- HSTS (includeSubDomains, preload)
- Security headers: X-Content-Type-Options, X-Frame-Options, CSP, Referrer-Policy
- OCSP Stapling
- Let's Encrypt auto-renewal (certbot / acme.sh)
- Rate limiting (limit_req_zone)
- Client body size limits
- Access log with reasonable format
- gzip/brotli compression
- WebSocket support if needed

Use to check the config: `nginx -t`
```

### `backup-strategy.md`

```markdown
# Backup Strategy: $SCOPE
Design a backup strategy for $SCOPE:

1. **What to back up**: databases, configs, files, volumes
2. **Backup types**: full vs incremental, snapshot vs logical
3. **Schedule**: frequency per data type (critical > semi-critical > ephemeral)
4. **Retention**: daily (7d), weekly (4w), monthly (12m), yearly
5. **Storage**: local, off-site, cloud, object storage
6. **Encryption**: at rest and in transit
7. **Testing**: how to verify backups are restorable (and how often)
8. **RPO/RTO**: target recovery point and time
9. **Disaster recovery**: cross-region failover plan

Include actual backup script / tool commands (restic, borg, pg_dump, rsync).
```

### `monitoring-stack-setup.md`

```markdown
# Monitoring Stack Setup: $TYPE
Design a monitoring stack for $TYPE scope:

**Recommended stack**: Prometheus + Grafana + Alertmanager + Loki (logs) + Tempo (traces)

**Service endpoints to monitor**:
- Application: /health, /metrics, /ready
- Infrastructure: node_exporter, cAdvisor, blackbox_exporter
- Database: postgres_exporter, redis_exporter, mysqld_exporter

**Critical dashboards**:
- RED metrics (Rate, Errors, Duration) per service
- Node overview (CPU, MEM, DISK, NET)
- Kubernetes cluster overview (if applicable)
- Database performance

**Alerts to configure**:
- Service down (5xx > threshold for 5min)
- High latency (p99 > SLO for 10min)
- Disk usage > 80%
- Certificate expiry < 30 days
- OOM / container restarts
```

### `log-pipeline-setup.md`

```markdown
# Log Pipeline: $SOURCE
Design a log pipeline for $SOURCE:

**Ingestion**: Vector / Fluentd / Fluent Bit / Logstash → collect from files, journald, Docker, TCP/UDP

**Processing**: 
- Parse structured logs (JSON)
- Parse unstructured logs (grok patterns)
- Enrich (add hostname, service, environment tags)
- Filter (drop health check noise, deduplicate)
- Transform to structured schema

**Storage / Query**:
- Loki (cloud-native, Grafana integration) — for operational logs
- Elasticsearch (full-text search) — for deep investigation
- S3/GCS (cold archive, compliance) — for long-term retention

**Alerting**:
- Error rate spikes
- Specific error patterns (connection refused, OOM, segfault)
- Missing logs from a host (stale heartbeat)
```

### `ssl-cert-check.md`

```markdown
# SSL/TLS Certificate Check: $DOMAIN
Audit SSL/TLS certificate for $DOMAIN:

- **Expiry**: openssl s_client -connect $DOMAIN:443 -servername $DOMAIN 2>/dev/null | openssl x509 -noout -dates
- **Issuer**: who signed it
- **SANs**: does the cert cover all required domains?
- **Chain**: complete? (missing intermediate → mobile/old clients fail)
- **Protocols**: TLS 1.0/1.1 still enabled? (should be disabled)
- **Ciphers**: weak ciphers (RC4, 3DES, CBC)?
- **HSTS**: headers present and valid?
- **OCSP Must-Staple**: enabled?
- **CT (Certificate Transparency)**: SCTs present?

Run: `sslscan $DOMAIN`, `testssl.sh $DOMAIN`, or check via ssllabs.com
```

---

## 🧰 Cross-Role Utilities

These commands are useful regardless of role.

### `project-onboard.md`

```markdown
# Project Onboarding
I'm new to this project. Help me understand it:

1. What does this project do? (one-paragraph summary)
2. What's the architecture? (diagram in words)
3. Folder structure overview
4. Tech stack (language, framework, database, infra)
5. How to run locally
6. How to run tests
7. How to deploy
8. Key env vars and configs
9. Where is the documentation?
10. Who are the key contacts / teams?
```

### `config-review.md`

```markdown
# Config Review: $FILE
Review this config file for:
- Syntax errors and validation issues
- Deprecated or removed options
- Security concerns (hardcoded secrets, permissive defaults)
- Performance implications
- Environment-specific overrides needed
- Missing required fields

Check against official documentation for the tool.
```

### `shell-script-audit.md`

```markdown
# Shell Script Audit: $FILE
Audit this shell script for common pitfalls:
- Unquoted variables (word splitting, glob expansion)
- set -e / set -o pipefail missing
- Error handling (|| exit, trap)
- Temporary file handling (mktemp, cleanup traps)
- Input validation (missing args, empty strings)
- Race conditions (mkdir -p, temp files)
- Portability issues (bashism in /bin/sh scripts)
- Secret leakage (echo $PASSWORD, ps exposure)

Suggest fixes for each issue found.
```

### `readme-generator.md`

```markdown
# Generate README
Generate a comprehensive README.md for this project:
- Project name and one-liner
- Features / what problem it solves
- Prerequisites (runtime, dependencies)
- Quick start (clone → install → run)
- Configuration (env vars, config files)
- Project structure (folder tree or diagram)
- API documentation (if applicable)
- Deployment instructions
- Contributing guidelines
- License
- Badges (CI, coverage, version)
```

---

## ⚡ Shell Aliases for Quick Access

Add to `~/.zshrc` for one-shot command execution without the TUI:

```bash
# ── Developer ──
alias o9router='o9r create-api -f src/api/router.ts'
alias o9model='o9r create-model -f src/models/'
alias o9test='o9r write-tests -f'
alias o9fix='o9r fix-bugs'
alias o9review='o9r code-review -f'
alias o9commit='o9r generate-commit-message -f <(git diff --cached)'
alias o9docs='o9r generate-docs -f'

# ── DevOps ──
alias o9docker='o9r create-dockerfile'
alias o9compose='o9r docker-compose-stack'
alias o9ci='o9r create-github-actions'
alias o9deploy='o9r create-deploy-script'
alias o9audit='o9r security-audit-config -f'

# ── SRE ──
alias o9incident='o9r incident-response'
alias o9runbook='o9r runbook-generate'
alias o9postmortem='o9r postmortem-draft'
alias o9perf='o9r performance-analysis'
alias o9capacity='o9r capacity-planning'

# ── Cloud ──
alias o9tf='o9r create-terraform-module'
alias o9k8s='o9r create-kubernetes-manifest'
alias o9iam='o9r iam-policy-review'
alias o9cost='o9r cloud-cost-analyze'

# ── Infra ──
alias o9nginx='o9r nginx-tls-setup'
alias o9backup='o9r backup-strategy'
alias o9dns='o9r dns-debug'
alias o9ssl='o9r ssl-cert-check'
alias o9mon='o9r monitoring-stack-setup'

# ── Cross ──
alias o9readme='o9r readme-generator'
alias o9onboard='o9r project-onboard'
alias o9shell='o9r shell-script-audit -f'
```

Then `source ~/.zshrc` and use e.g. `o9fix` to start a fix session.

---

## 💡 Tips

| Situation | Recommendation |
|-----------|---------------|
| Complex multi-file task | Use `--agent plan` first so OpenCode designs before coding |
| Simple one-shot question | TUI mode → Ctrl+K → type command → Enter — no need for shell aliases |
| Sensitive files (secrets, prod) | Never `-f` credential files; describe the problem abstractly |
| Working in a monorepo | Put per-project commands in `<project>/.opencode/commands/` for targeted context |
| OpenCode stuck/confused | `Ctrl+C` out and start fresh — don't fight a broken context |
| First time on a project | Run `o9onboard` or the `project-onboard` command to get oriented |

---

*Last updated: June 2026*
