# OpenCode — Daily Use Cases for Developer & DevOps

**OpenCode** is a provider-agnostic AI coding agent CLI. This guide covers real-world daily use cases for developers and devops engineers.


## Table of Contents

- [Alias Setup](#alias-setup)
- [👨‍💻 Developer Daily](#developer-daily)
  - [Writing Code (Core Features)](#writing-code-core-features)
  - [Debugging](#debugging)
  - [Refactoring](#refactoring)
  - [Unit Tests](#unit-tests)
  - [Database](#database)
  - [Code Review](#code-review)
  - [Documentation](#documentation)
  - [Git](#git)
- [🐳 DevOps Daily](#devops-daily)
  - [Docker](#docker)
  - [Server Management](#server-management)
  - [CI/CD](#cicd)
  - [Security](#security)
  - [Deployment](#deployment)
  - [Config Review](#config-review)
  - [Network/DNS Debugging](#networkdns-debugging)
  - [Log Analysis](#log-analysis)
- [⚙️ Config File Reference](#config-file-reference)
- [🎯 How to Run Custom Commands](#how-to-run-custom-commands)
  - [Via Command Palette (Ctrl+P)](#via-command-palette-ctrlp)
  - [Quick Examples](#quick-examples)
  - [Shell Aliases (One-Shot)](#shell-aliases-one-shot)
- [💡 Tips](#tips)

Docs: [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode) · Install: `npm i -g opencode-ai`

> This guide assumes OpenCode is configured with a provider via 9Router or direct API key.

---

## Alias Setup

Add to `~/.zshrc` or `~/.bashrc`:

```bash
alias o9='LOCAL_ENDPOINT=http://localhost:20128/v1 opencode'
alias o9r='LOCAL_ENDPOINT=http://localhost:20128/v1 opencode run'
alias o9p='LOCAL_ENDPOINT=http://localhost:20128/v1 opencode run --agent plan'
```

Then use `o9`, `o9r`, or `o9p` for daily tasks.

---

## 👨‍💻 Developer Daily

### Writing Code (Core Features)

```bash
# Build an API endpoint
o9r 'Create GET /api/users/{id} endpoint with proper error handling' \
  -f src/api/router.ts -f src/db/users.ts

# Build a component
o9r 'Create React UserProfileCard component with loading and empty states' \
  -f src/components/ -f src/types/user.ts

# Implement a service
o9r 'Implement email notification service with retry logic' \
  -f src/services/
```

### Debugging

```bash
# Debug errors
o9r 'Debug this error: identify root cause and suggest fix' \
  -f src/auth/login.ts -f src/utils/validation.ts -f error.log

# Debug failing tests
o9r 'Why is this test failing? Fix the implementation code' \
  -f tests/auth.test.ts -f src/auth/login.ts

# Debug performance
o9r 'Identify N+1 queries and performance bottlenecks in these files' \
  -f src/repositories/userRepo.ts -f src/controllers/userController.ts
```

### Refactoring

```bash
# Split large file
o9r 'Refactor this file into smaller focused modules' \
  -f src/utils/helpers.ts --agent plan

# Migrate patterns
o9r 'Migrate callback style to async/await in this directory' \
  -f 'src/legacy/**/*.ts'

# Extract constants
o9r 'Extract magic strings and numbers into a constants file' \
  -f src/services/paymentService.ts -f src/constants.ts
```

### Unit Tests

```bash
# Write from scratch
o9r 'Write comprehensive unit tests for all exported functions' \
  -f src/services/userService.ts

# Add edge cases
o9r 'Add test cases for: success, validation error, not found, server error, empty state' \
  -f src/services/userService.ts -f tests/userService.test.ts
```

### Database

```bash
# Create migration
o9r 'Create SQL migration to add phone_number column to users table with index'

# Write queries
o9r 'Write SQL query: top 10 users by total order value this month with their details'

# Design schema
o9r 'Design database schema for a notification system with templates, channels, and delivery status' \
  --agent plan
```

### Code Review

```bash
# Review a file
o9r 'Review this code for bugs, security issues, and improvements' \
  -f src/payments/handler.ts

# Review a PR diff
o9r 'Summarize and review the changes: what changed, risks, suggestions' \
  -f <(git diff main...feature-branch)
```

### Documentation

```bash
# Project README
o9r 'Create README.md: installation, usage, API reference, env vars, deployment'

# API docs
o9r 'Generate API docs from route handler files' \
  -f 'src/api/**/*.ts' --agent plan

# Architecture docs
o9r 'Document project architecture: folder structure, data flow, key decisions' \
  --agent plan
```

### Git

```bash
# Generate commit message
o9r 'Generate a concise commit message from this diff' \
  -f <(git diff --cached)

# Generate changelog
o9r 'Generate changelog from recent commits in conventional commit format' \
  -f <(git log --oneline --no-decorate -30)

# Write .gitignore
o9r 'Generate .gitignore for a SvelteKit + Go project'
```

---

## 🐳 DevOps Daily

### Docker

```bash
# Create Dockerfile
o9r 'Create multi-stage Dockerfile: frontend build, Go backend, small final image' \
  --agent plan

# Optimize image
o9r 'Review Dockerfile for size optimization, caching, and security' \
  -f Dockerfile

# Debug container
o9r 'Analyze these container logs — what went wrong and how to fix?' \
  -f app.log

# Create Docker Compose
o9r 'Create docker-compose.yml: app, postgres, redis, nginx with health checks'
```

### Server Management

```bash
# Analyze server health
o9r 'Analyze server health: flag issues and suggest fixes' \
  -f <(df -h) -f <(free -h) -f <(uptime) -f <(ps aux --sort=-%mem | head -15)

# Debug crashes
o9r 'Find why service keeps crashing from these logs' \
  -f /var/log/syslog

# Disk cleanup
o9r 'Analyze disk usage and suggest cleanup targets' \
  -f <(du -sh /* 2>/dev/null | sort -rh | head -20)
```

### CI/CD

```bash
# Create workflow
o9r 'Create GitHub Actions workflow: lint, test, build, publish Docker to GHCR' \
  --agent plan

# Debug pipeline
o9r 'Analyze CI failure: what broke and how to fix?' \
  -f .github/workflows/deploy.yml -f ci_logs.txt
```

### Security

```bash
# Audit nginx
o9r 'Security audit nginx config: check TLS versions, headers, rate limiting' \
  -f nginx.conf

# Audit SSH
o9r 'Review SSH config for security best practices' \
  -f /etc/ssh/sshd_config

# Check Docker security
o9r 'Review docker-compose.yml for security issues' \
  -f docker-compose.yml
```

### Deployment

```bash
# Create deploy script
o9r 'Create deploy.sh: git pull, build, restart service, health check, rollback on fail'

# Setup reverse proxy
o9r 'Generate nginx reverse proxy config: SSL termination, caching, WebSocket' \
  --agent plan

# Create rollback
o9r 'Create rollback script: revert to previous Docker image tag and verify health'
```

### Config Review

```bash
# Review YAML/JSON config
o9r 'Review this config: find misconfigurations and suggest improvements' \
  -f config.yaml -f config.production.yaml

# Generate env template
o9r 'Generate .env.example from actual .env with documentation for each variable' \
  -f .env
```

### Network/DNS Debugging

```bash
# DNS analysis
o9r 'Analyze these DNS records: is everything configured correctly?' \
  -f <(dig +short example.com) -f <(dig +short www.example.com) -f <(dig MX example.com)

# Nginx debug
o9r 'Why is nginx returning 502? Analyze config and error logs' \
  -f nginx.conf -f /var/log/nginx/error.log
```

### Log Analysis

```bash
# Error patterns
o9r 'Scan these logs, group errors by type, and suggest fixes' \
  -f production.log

# Rate limit analysis
o9r 'Analyze request patterns: are we hitting rate limits? Suggest improvements' \
  -f access.log
```

---

## ⚙️ Config File Reference

`~/.opencode.json`:

```json
{
  "agents": {
    "coder": {
      "model": "local.kr/claude-sonnet-4.5"
    }
  },
  "autoCompact": true,
  "customCommands": [
    {
      "name": "test",
      "prompt": "Write comprehensive unit tests for {{file}} covering success, error, and edge cases",
      "args": ["file"]
    },
    {
      "name": "review",
      "prompt": "Review {{file}} for bugs, security vulnerabilities, and performance issues",
      "args": ["file"]
    },
    {
      "name": "refactor",
      "prompt": "Refactor {{file}} for better maintainability and performance",
      "args": ["file"]
    },
    {
      "name": "docker",
      "prompt": "Create production-grade Dockerfile and docker-compose.yml for {{project}}",
      "args": ["project"]
    },
    {
      "name": "deploy",
      "prompt": "Create deployment config: Dockerfile, GitHub Actions workflow, and reverse proxy setup for {{project}}",
      "args": ["project"]
    },
    {
      "name": "doc",
      "prompt": "Write documentation for {{file}} covering what it does, parameters, and usage examples",
      "args": ["file"]
    }
  ]
}
```

---

## 🎯 How to Run Custom Commands

Once you've defined custom commands in `~/.opencode.json`, call them from the **OpenCode TUI**:

### Via Command Palette (Ctrl+P)

```
o9              # Start TUI first
```

Then press **`Ctrl+P`** → command palette opens → start typing the command name:
1. Type `test` → Enter
2. Enter the `file` parameter (path to the file you want to test) → Enter
3. Runs automatically

### Quick Examples

| Goal | Action |
|------|--------|
| Write unit tests | `Ctrl+P` → `test` → enter `src/services/user.ts` → Enter |
| Review code | `Ctrl+P` → `review` → enter `src/auth/login.ts` → Enter |
| Create Docker setup | `Ctrl+P` → `docker` → enter project name → Enter |
| Write documentation | `Ctrl+P` → `doc` → enter `src/utils/helpers.ts` → Enter |

No need to type long prompts — just 2-3 steps from the command palette.

### Shell Aliases (One-Shot)

For tasks that always target the same file, create aliases in `~/.zshrc`:

```bash
# Recurring tasks with fixed files
alias o9test-auth='o9r test -f src/services/authService.ts'
alias o9review-api='o9r review -f src/api/routes.ts'
alias o9fix-latest='o9r "Fix bugs and errors in this project"'
alias o9commit='o9r "Generate commit message" -f <(git diff --cached)'
```

Reload: `source ~/.zshrc`

Then just:
```bash
o9test-auth      # Run auth tests
o9commit         # Generate commit message
```

---

## 💡 Tips

- **Plan first** for complex tasks: `--agent plan` makes OpenCode design before coding
- **One session per task**: exit TUI (`Ctrl+C`) and start fresh for each task
- **Commit before asking**: `git add -A && git commit -m "snapshot"` before any refactor
- **Attach context**: always use `-f` to give relevant files so OpenCode understands the codebase
- **Match reasoning effort**: `--variant minimal` for simple tasks, `--variant max` for architecture decisions
- **9Router users**: combine with free tier (Kiro AI) for unlimited coding at $0/month

---

*Last updated: June 2026*
