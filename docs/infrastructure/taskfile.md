---
title: Taskfile.dev — Modern Task Runner
description: - [Overview](#overview)
---

# Taskfile.dev — Modern Task Runner

> **Last updated:** 2026-06-07
> **Version:** v3.50.0+
> **Repo:** [go-task/task](https://github.com/go-task/task)
> **Docs:** https://taskfile.dev
> **License:** MIT

## Table of Contents

- [Overview](#overview)
  - [What is Task?](#what-is-task)
  - [How It Works](#how-it-works)
  - [Why Task Instead of Make?](#why-task-instead-of-make)
- [Installation](#installation)
  - [Package Managers](#package-managers)
  - [Install Script](#install-script)
  - [Build from Source](#build-from-source)
  - [GitHub Actions](#github-actions)
- [Taskfile.yml Syntax](#taskfileyml-syntax)
  - [Root Schema](#root-schema)
  - [Supported File Names](#supported-file-names)
  - [Minimal Example](#minimal-example)
- [Commands & CLI](#commands--cli)
  - [Usage](#usage)
  - [Commands](#commands)
  - [Key CLI Flags](#key-cli-flags)
  - [Exit Codes](#exit-codes)
- [Core Features](#core-features)
  - [Dependencies](#dependencies)
  - [Variables](#variables)
  - [Templates](#templates)
  - [Platform-Specific Commands](#platform-specific-commands)
  - [Aliases](#aliases)
- [Advanced Features](#advanced-features)
  - [Includes](#includes)
  - [Deferred Commands](#deferred-commands)
  - [Pre-conditions](#pre-conditions)
  - [Conditional Execution (if)](#conditional-execution-if)
  - [Loops](#loops)
  - [Up-to-Date / Caching](#up-to-date--caching)
  - [Watch Mode](#watch-mode)
  - [Internal Tasks](#internal-tasks)
  - [Task Directory](#task-directory)
  - [Calling Tasks Serially](#calling-tasks-serially)
  - [Warning Prompts](#warning-prompts)
  - [Forwarding CLI Arguments](#forwarding-cli-arguments)
  - [Wildcard Arguments](#wildcard-arguments)
  - [Output Modes](#output-modes)
  - [Environment & .env Files](#environment--env-files)
  - [Short Task Syntax](#short-task-syntax)
- [Practical Examples](#practical-examples)
  - [Go Build Pipeline](#go-build-pipeline)
  - [Monorepo Service Management](#monorepo-service-management)
  - [Multi-Arch Docker Build](#multi-arch-docker-build)
  - [Code Generation Workflow](#code-generation-workflow)
  - [Multi-Environment Deploy](#multi-environment-deploy)
  - [CI Pipeline Integration](#ci-pipeline-integration)
- [Comparison with Other Tools](#comparison-with-other-tools)
  - [Task vs Make](#task-vs-make)
  - [Task vs Just](#task-vs-just)
  - [When to Choose Task](#when-to-choose-task)
- [Known Limitations](#known-limitations)
- [Quick Reference](#quick-reference)
- [Summary](#summary)

---

## Overview

### What is Task?

**Task** (go-task/task) is a fast, cross-platform task runner / build tool written in Go. It uses a YAML file (`Taskfile.yml`) to define tasks, dependencies, and commands — designed as a modern replacement for GNU Make.

### How It Works

```
Taskfile.yml → Task reads YAML → resolves dependencies (parallel)
→ evaluates Go templates in variables → executes shell commands
→ checks up-to-date status (checksum/timestamp) → caches in .task/
```

1. Task reads `Taskfile.yml` from current directory (walking up like git)
2. Parses YAML into task definitions with dependencies, variables, commands
3. When you run `task <name>`, it resolves dependencies (in parallel), evaluates templates, executes shell commands
4. Caches checksum fingerprints in `.task/` directory

### Why Task Instead of Make?

| Pain Point with Make | How Task Solves It |
|----------------------|--------------------|
| Tab-sensitive syntax | Clean YAML |
| `/bin/sh` only on Unix | Built-in Go `sh` interpreter — works on Windows |
| Serial dependencies by default | Parallel dependency execution |
| No built-in caching | Checksum/timestamp up-to-date checking |
| Arcane variable expansion | Go templates with 200+ functions |
| No includes with namespacing | Namespaced, aliasable includes |
| No watch mode | Built-in `--watch` |
| Cryptic errors | Clear errors with fuzzy task matching |

---

## Installation

### Package Managers

| Platform | Command |
|----------|---------|
| **Homebrew** (macOS/Linux) | `brew install go-task` |
| **Snap** (Linux) | `sudo snap install task` |
| **npm** (Node.js) | `npm install -g @go-task/cli` |
| **WinGet** (Windows) | `winget install Task.Task` |
| **Fedora/RHEL** | `sudo dnf install task` |
| **Arch Linux** | `sudo pacman -S go-task` |
| **Nix/NixOS** | `nix-env -iA nixpkgs.go-task` |
| **Chocolatey** (Windows) | `choco install task` |
| **Scoop** (Windows) | `scoop install task` |
| **MacPorts** | `sudo port install task` |

### Install Script

```bash
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
```

### Build from Source

```bash
go install github.com/go-task/task/v3/cmd/task@latest
```

### GitHub Actions

```yaml
- uses: arduino/setup-task@v2
```

---

## Taskfile.yml Syntax

### Root Schema

```yaml
version: '3'           # Required — schema version

# Global settings
output: interleaved    # interleaved | group | prefixed
method: checksum       # checksum | timestamp | none
silent: false          # suppress command echoing
run: always            # always | once | when_changed
interval: 100ms        # watch interval
dotenv: ['.env']       # .env files to load

# Shell options
set: [errexit, nounset, pipefail]
shopt: [globstar]

# Global variables
vars:
  APP_NAME: myapp
  VERSION:
    sh: git describe --tags --always

# Global environment variables
env:
  NODE_ENV: production

# Include other Taskfiles
includes:
  docker: ./DockerTasks.yml

# Task definitions
tasks:
  build:
    cmds:
      - go build -o {{.APP_NAME}} .
```

### Supported File Names

Priority order (first found wins):

1. `Taskfile.yml`
2. `taskfile.yml`
3. `Taskfile.yaml`
4. `taskfile.yaml`
5. `Taskfile.dist.yml` / `taskfile.dist.yml` (committed template, user can override locally)
6. `Taskfile.dist.yaml` / `taskfile.dist.yaml`

### Minimal Example

```yaml
version: '3'

tasks:
  default:
    cmds:
      - echo "Hello, Task!"
```

```bash
task
# Hello, Task!
```

---

## Commands & CLI

### Usage

```bash
task [options] [tasks...] [-- CLI_ARGS...]
```

### Commands

| Command | Description |
|---------|-------------|
| `task` / `task default` | Run the default task |
| `task build` | Run a specific task |
| `task build test lint` | Run multiple tasks (serial default) |
| `task --list` / `task -l` | List tasks with descriptions |
| `task --list-all` / `task -a` | List all tasks (including hidden) |
| `task --init` / `task -i` | Scaffold a new Taskfile.yml |
| `task --summary <task>` | Show detailed info about a task |
| `task --status <task>` | Check if task is up-to-date (exit code) |

### Key CLI Flags

| Flag | Description |
|------|-------------|
| `-l, --list` | List tasks with descriptions |
| `-a, --list-all` | List all tasks |
| `-f, --force` | Force run even if up-to-date |
| `-p, --parallel` | Run tasks in parallel |
| `-n, --dry` | Dry run (print commands, don't execute) |
| `-s, --silent` | Suppress command echoing |
| `-v, --verbose` | Verbose output |
| `-w, --watch` | Watch files and re-run on changes |
| `-F, --failfast` | Stop on first dependency failure |
| `-C, --concurrency <n>` | Limit concurrent parallel tasks |
| `-d, --dir <path>` | Working directory for Taskfile lookup |
| `-t, --taskfile <file>` | Use a specific Taskfile |
| `-g, --global` | Use `$HOME/Taskfile.yml` |
| `-o, --output <mode>` | Output mode (interleaved/group/prefixed) |
| `-c, --color` | Enable/disable color output |
| `-I, --interval <dur>` | Watch interval (e.g. `500ms`) |
| `-x, --exit-code` | Pass through command exit codes |
| `-y, --yes` | Auto-confirm prompts |
| `--interactive` | Enable prompts for missing variables |
| `--json` | JSON output for `--list` |
| `--disable-fuzzy` | Disable fuzzy task name matching |
| `--version` | Show version |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Unknown error |
| 100 | No Taskfile found |
| 101 | Taskfile already exists (`--init`) |
| 102 | Invalid/unparseable Taskfile |
| 107 | No schema version defined |
| 200 | Task not found |
| 201 | Command execution error |
| 202 | Attempted to run internal task |
| 203 | Multiple tasks with same name |
| 204 | Recursion limit reached |
| 205 | Task cancelled by user |
| 206 | Missing required variables |
| 207 | Variable has incorrect value |

---

## Core Features

### Dependencies

Dependencies run **in parallel** by default:

```yaml
tasks:
  build:
    deps: [js, css]    # js and css run simultaneously
    cmds:
      - go build -o app .
```

Dependencies with variables:

```yaml
tasks:
  default:
    deps:
      - task: echo_sth
        vars: { TEXT: 'before 1' }
      - task: echo_sth
        vars: { TEXT: 'before 2' }
        silent: true
    cmds:
      - echo "after"
```

**Fail-fast:** `--failfast` CLI flag or `failfast: true` in `.taskrc.yml`.

### Variables

**Types:** string, bool, int, float, array, map

```yaml
vars:
  STRING: 'Hello, World!'
  BOOL: true
  INT: 42
  ARRAY: [1, 2, 3]
  MAP: { A: 1, B: 2, C: 3 }
```

**Precedence** (highest to lowest):
1. Task-level variables
2. Variables passed when calling a task
3. Variables of the included Taskfile
4. Variables of the inclusion definition
5. Global variables
6. Environment variables

**Dynamic variables** (from shell commands):

```yaml
vars:
  GIT_COMMIT:
    sh: git log -n 1 --format=%h
```

**Variable references** (preserve type, avoid string coercion):

```yaml
vars:
  FOO: [A, B, C]
  BAR:
    ref: .FOO    # BAR keeps array type
```

**Required variables with validation:**

```yaml
tasks:
  deploy:
    requires:
      vars:
        - name: ENVIRONMENT
          enum: [dev, staging, prod]
        - API_KEY
    cmds:
      - ./deploy.sh
```

### Templates

Task uses Go's `text/template` with the **slim-sprig** function library.

**Syntax:** `{{.VARIABLE_NAME}}`, `{{function arg1 arg2}}`, `{{.VAR | function}}`

**Special variables:**

| Variable | Type | Description |
|----------|------|-------------|
| `{{.TASK}}` | string | Current task name |
| `{{.CLI_ARGS}}` | string | Args after `--` in CLI |
| `{{.ROOT_DIR}}` | string | Root Taskfile directory |
| `{{.TASKFILE_DIR}}` | string | Current Taskfile directory |
| `{{.USER_WORKING_DIR}}` | string | Dir where `task` was called |
| `{{.CHECKSUM}}` | string | Checksum of source files |
| `{{.TIMESTAMP}}` | time.Time | Greatest source file timestamp |
| `{{.ITEM}}` | any | Current loop iteration value |
| `{{.EXIT_CODE}}` | int | Exit code in defer |
| `{{OS}}` | string | OS name (linux/darwin/windows) |
| `{{ARCH}}` | string | Architecture (amd64/arm64) |

**Key template functions:**

| Category | Functions |
|----------|-----------|
| Logic | `and`, `or`, `not`, `eq`, `ne`, `lt`, `gt`, `default`, `empty` |
| Strings | `upper`, `lower`, `trim`, `quote`, `shellQuote`/`q`, `contains`, `replace`, `regexMatch`, `regexReplaceAll`, `splitList`, `join` |
| Math | `add`, `sub`, `mul`, `div`, `mod`, `max`, `min` |
| Lists | `first`, `last`, `len`, `slice`, `uniq`, `sortAlpha`, `append`, `has` |
| Encoding | `toJson`, `fromJson`, `toYaml`, `fromYaml`, `b64enc`, `b64dec` |
| System | `OS`, `ARCH`, `numCPU`, `env`, `lookupEnv`, `exeExt`, `uuid`, `spew` |
| Date | `now`, `date`, `toDate`, `unixEpoch`, `ago` |
| Dict | `dict`, `get`, `keys`, `hasKey`, `merge` |

### Platform-Specific Commands

```yaml
tasks:
  build:
    platforms: [linux, darwin]    # Task only runs on these OSes
    cmds:
      - go build -o app .

  deploy:
    cmds:
      - cmd: echo "Windows-specific"
        platforms: [windows/amd64]
      - cmd: echo "Runs everywhere"
```

### Aliases

```yaml
tasks:
  generate:
    aliases: [gen, g]
    cmds:
      - go generate ./...
```

Namespace aliases for includes:

```yaml
includes:
  docker:
    taskfile: ./DockerTasks.yml
    aliases: [ctr]
```

Now callable as `task docker:build` or `task ctr:build`.

---

## Advanced Features

### Includes

Include other Taskfiles with namespace isolation:

```yaml
includes:
  docs: ./documentation              # looks for ./documentation/Taskfile.yml
  docker: ./DockerTasks.yml          # direct file
  backend:
    taskfile: ./backend               # directory with Taskfile.yml
    dir: ./backend                    # working directory
    optional: true                    # don't error if missing
    flatten: true                     # no namespace prefix
    internal: true                    # hide from --list
    aliases: [api]                    # namespace aliases
    excludes: [internal-task]         # exclude specific tasks
    vars:
      SERVICE_NAME: backend
```

Usage: `task docs:serve`, `task docker:build`

**OS-specific includes:**

```yaml
includes:
  build: ./Taskfile_{{OS}}.yml
```

### Deferred Commands

Run cleanup even on failure (like Go's `defer`):

```yaml
tasks:
  test:
    cmds:
      - mkdir -p tmpdir/
      - defer: rm -rf tmpdir/         # runs even if next commands fail
      - ./run-tests.sh
```

Deferred commands execute in reverse order.

### Pre-conditions

Conditions that **must** be met or the task fails:

```yaml
tasks:
  deploy:
    preconditions:
      - test -f .env
      - sh: test -n "$API_KEY"
        msg: "API_KEY environment variable is required"
    cmds:
      - ./deploy.sh
```

Unlike `status`, preconditions **fail the task**. Use `--force` to bypass.

### Conditional Execution (if)

Skip tasks or commands without failing:

```yaml
tasks:
  deploy:
    if: '[ "$CI" = "true" ]'           # Task-level skip
    cmds:
      - ./deploy.sh

  build:
    cmds:
      - cmd: echo "Production build"
        if: '[ "$ENV" = "production" ]' # Command-level skip
      - go build ./...
```

| | `if` | `preconditions` |
|---|---|---|
| On failure | Skips (silent) | Fails (stops) |
| Use case | "Run if possible" | "Must be true" |

### Loops

**Static list:**

```yaml
cmds:
  - for: ['foo.txt', 'bar.txt']
    cmd: cat {{ .ITEM }}
```

**Matrix (all permutations):**

```yaml
cmds:
  - for:
      matrix:
        OS: ['linux', 'windows', 'darwin']
        ARCH: ['amd64', 'arm64']
    cmd: echo "{{.ITEM.OS}}/{{.ITEM.ARCH}}"
```

**Over sources:**

```yaml
tasks:
  default:
    sources: ['*.txt']
    cmds:
      - for: sources
        cmd: cat {{ .ITEM }}
```

**Over variables (split):**

```yaml
cmds:
  - for: { var: MY_VAR, split: ',', as: FILE }
    cmd: cat {{.FILE}}
```

**Loop over tasks:**

```yaml
cmds:
  - for: [foo, bar]
    task: my-task
    vars:
      FILE: '{{.ITEM}}'
```

**Loop in dependencies:**

```yaml
deps:
  - for: [unit, integration, e2e]
    task: test
    vars:
      TYPE: '{{.ITEM}}'
```

### Up-to-Date / Caching

**By checksum (default):**

```yaml
tasks:
  build:
    sources:
      - 'src/**/*.go'
      - go.mod
    generates:
      - ./app
    cmds:
      - go build -o app .
```

**By timestamp:**

```yaml
tasks:
  build:
    method: timestamp
    sources:
      - '**/*.go'
    generates:
      - 'app{{exeExt}}'
    cmds:
      - go build -o app .
```

**By programmatic status:**

```yaml
tasks:
  generate:
    status:
      - test -f generated/output.txt
      - test -s generated/output.txt
    cmds:
      - ./generate.sh
```

**Exclude from sources:**

```yaml
sources:
  - 'src/**/*.css'
  - exclude: src/vendor/**/*
```

Schema: `{method: checksum|timestamp, sources: [...], generates: [...], status: [...]}`

### Watch Mode

```yaml
tasks:
  dev:
    watch: true
    sources:
      - '**/*.go'
    cmds:
      - go build ./... && ./app
```

Or CLI: `task build --watch`

### Internal Tasks

Hidden from `--list`, cannot be called directly:

```yaml
tasks:
  build-image:
    internal: true
    cmds:
      - docker build -t myimage .
```

### Task Directory

```yaml
tasks:
  serve:
    dir: public/www
    cmds:
      - caddy
```

If the directory doesn't exist, Task creates it.

### Calling Tasks Serially

Unlike `deps` (parallel), `task:` calls are serial:

```yaml
tasks:
  main:
    cmds:
      - task: build-linux
      - task: build-darwin
      - echo "Both done"
```

With variable passing:

```yaml
cmds:
  - task: greet
    vars: { RECIPIENT: 'World' }
    silent: true
```

### Warning Prompts

```yaml
tasks:
  dangerous:
    prompt: "This will delete everything. Continue?"
    cmds:
      - rm -rf /tmp/data
```

Use `-y` / `--yes` to auto-confirm.

### Forwarding CLI Arguments

```bash
task yarn -- install
```

```yaml
tasks:
  yarn:
    cmds:
      - yarn {{.CLI_ARGS}}
```

### Wildcard Arguments

```yaml
tasks:
  start:*:
    vars:
      SERVICE: '{{index .MATCH 0}}'
    cmds:
      - echo "Starting {{.SERVICE}}"
```

Usage: `task start:api`, `task start:web`

### Output Modes

```yaml
output: interleaved   # Default: real-time mixed output
output: group         # Print output after command finishes
output: prefixed      # Prefix each line with [task-name]
```

Advanced group (CI-friendly):

```yaml
output:
  group:
    begin: '::group::{{.TASK}}'
    end: '::endgroup::'
    error_only: true
```

### Environment & .env Files

```yaml
env:
  NODE_ENV: production
  DATABASE_URL:
    sh: echo $DATABASE_URL

dotenv:
  - .env.local       # Highest priority
  - .env
```

### Short Task Syntax

```yaml
tasks:
  build: go build -o app .
  lint: golangci-lint run ./...
  test:
    - task: lint
    - go test ./...
```

---

## Practical Examples

### Go Build Pipeline

```yaml
version: '3'

vars:
  APP: myapp
  VERSION:
    sh: git describe --tags --always

tasks:
  default:
    deps: [lint, test, build]

  lint:
    cmds:
      - golangci-lint run ./...

  test:
    cmds:
      - go test -race -coverprofile=coverage.out ./...

  build:
    deps: [test]
    sources:
      - '**/*.go'
      - go.mod
      - go.sum
    generates:
      - '{{.APP}}'
    cmds:
      - CGO_ENABLED=0 go build -ldflags="-X main.version={{.VERSION}}" -o {{.APP}} .

  clean:
    cmds:
      - rm -f {{.APP}} coverage.out

  run:
    deps: [build]
    cmds:
      - ./{{.APP}}
```

### Monorepo Service Management

```yaml
version: '3'

tasks:
  up:
    dir: '{{.USER_WORKING_DIR}}'
    preconditions:
      - test -f docker-compose.yml
    cmds:
      - docker compose up -d

  down:
    dir: '{{.USER_WORKING_DIR}}'
    preconditions:
      - test -f docker-compose.yml
    cmds:
      - docker compose down

  logs:
    dir: '{{.USER_WORKING_DIR}}'
    cmds:
      - docker compose logs -f

  ps:
    dir: '{{.USER_WORKING_DIR}}'
    cmds:
      - docker compose ps
```

Usage: `cd services/auth && task up`

### Multi-Arch Docker Build

```yaml
version: '3'

vars:
  IMAGE: ghcr.io/myorg/myapp

includes:
  docker:
    taskfile: ./docker-tasks.yml
    vars:
      REGISTRY: ghcr.io/myorg

tasks:
  build-all:
    deps:
      - for:
          matrix:
            ARCH: [amd64, arm64]
        task: docker:build
        vars:
          PLATFORM: 'linux/{{.ITEM.ARCH}}'
```

### Code Generation Workflow

```yaml
version: '3'

vars:
  PROTO_DIR: proto
  GEN_DIR: pkg/generated

tasks:
  generate:
    deps: [clean, proto, openapi]

  proto:
    sources:
      - '{{.PROTO_DIR}}/**/*.proto'
    generates:
      - '{{.GEN_DIR}}/proto/**/*.go'
    cmds:
      - protoc --go_out={{.GEN_DIR}} {{.PROTO_DIR}}/*.proto

  openapi:
    sources:
      - 'api/openapi.yaml'
    generates:
      - '{{.GEN_DIR}}/api/**/*.go'
    cmds:
      - oapi-codegen -package api api/openapi.yaml > {{.GEN_DIR}}/api/api.gen.go

  clean:
    cmds:
      - rm -rf {{.GEN_DIR}}
```

### Multi-Environment Deploy

```yaml
version: '3'

tasks:
  deploy:
    desc: Deploy service to environment
    requires:
      vars:
        - name: ENV
          enum: [dev, staging, prod]
    prompt: 'Deploy to {{.ENV}}? Are you sure?'
    cmds:
      - task: build
      - task: push-image
      - task: update-k8s

  build:
    cmds:
      - docker build -t myapp:{{.ENV}} .

  push-image:
    preconditions:
      - sh: test -n "$DOCKER_REGISTRY"
        msg: "DOCKER_REGISTRY not set"
    cmds:
      - docker push myapp:{{.ENV}}

  update-k8s:
    dir: k8s/{{.ENV}}
    cmds:
      - kubectl apply -f deployment.yaml
```

### CI Pipeline Integration

```yaml
version: '3'

output:
  group:
    begin: '::group::{{.TASK}}'
    end: '::endgroup::'
    error_only: true

tasks:
  ci:
    deps: [lint, test, build]
    cmds:
      - echo "CI pipeline complete"

  lint: golangci-lint run ./...

  test: gotestsum --format standard-verbose ./...

  build: go build ./...
```

---

## Comparison with Other Tools

### Task vs Make

| Aspect | Task | GNU Make |
|--------|------|----------|
| **Syntax** | Clean YAML | Tab-sensitive Makefile |
| **Cross-platform** | Native Go (same everywhere) | Unix-focused |
| **Shell** | Built-in Go `sh` (works on Windows) | `/bin/sh` only |
| **Dependencies** | Parallel by default | Serial by default |
| **Caching** | Built-in checksum/timestamp | Manual (phony targets) |
| **Templates** | 200+ Go template functions | Limited string substitution |
| **Includes** | Namespaced, aliased, optional | Flat `include` directive |
| **Watch mode** | Built-in | External tools needed |
| **JSON output** | Native `--json` | No |
| **Error messages** | Clear with suggestions | Often cryptic |

### Task vs Just

| Aspect | Task | Just (just) |
|--------|------|-------------|
| **Language** | YAML + templates | YAML |
| **Plugin ecosystem** | Includes + vars pattern | Recipes only |
| **Caching** | Built-in | Manual |
| **Watch mode** | Built-in | Not built-in |
| **Templates** | 200+ functions | Minimal |
| **GitHub stars** | 30k+ | 20k+ |

### When to Choose Task

- You need **cross-platform builds** (especially Windows)
- You want **readable, maintainable build files** — YAML over Makefile
- You need **smart caching** — skip rebuilds automatically
- You want **parallel dependency execution** out of the box
- You work with **monorepos** — includes, namespace aliases, dir support
- You want **CI-friendly output** — group mode, JSON, error annotations
- You need **template-driven taskfiles** — powerful variable interpolation

---

## Known Limitations

1. **Cannot modify parent shell** — `cd` / `export` don't affect calling shell
2. **Each command is a separate shell** — state lost between commands; use multi-line `|` for chaining
3. **No Makefile compatibility** — must rewrite in YAML
4. **Watch mode quirks** — child process management issues with long-running servers
5. **No SSH/remote execution** — local only
6. **dotenv not inherited in includes** — included Taskfiles can't have `dotenv`
7. **Template output is always string** — use `ref:` to preserve types
8. **No YAML anchors** — YAML merge keys (`<<:`) don't work reliably
9. **Map iteration is unordered** — random order
10. **Breaking changes possible** — check experiments (`TASK_X_*`) on upgrade
11. **Volunteer-maintained** — no guaranteed release schedule

---

## Quick Reference

### Most Common Commands

```bash
task                    # Run default task
task build              # Run named task
task build test         # Run multiple tasks
task -p test lint       # Run in parallel
task --list             # List available tasks
task --init             # Create Taskfile.yml
task build --force      # Skip cache
task build --watch      # Auto-rebuild on changes
task build --dry        # Print only, don't execute
task deploy --yes       # Auto-confirm prompts
task --summary deploy   # Show task details
task --json --list      # Machine-readable output
```

### Minimal Taskfile Template

```yaml
version: '3'

tasks:
  default:
    cmds:
      - echo "Hello, Task!"
```

### Full-Featured Template

```yaml
version: '3'

output: group
method: checksum
dotenv: ['.env']
set: [pipefail]
shopt: [globstar]

vars:
  APP: myapp

env:
  NODE_ENV: production

includes:
  utils: ./taskfiles/utils.yml

tasks:
  default:
    deps: [build]

  build:
    deps: [lint, test]
    sources: ['**/*.go']
    generates: ['./{{.APP}}']
    cmds:
      - go build -o {{.APP}} .

  lint: golangci-lint run ./...
  test: go test ./...
  clean: rm -f {{.APP}}
```

---

## Summary

Task is the ideal replacement for Makefiles in modern development workflows. It's particularly well-suited for:

- **Go projects** — the two Go tools complement each other perfectly
- **Cross-platform teams** — Windows, macOS, Linux without friction
- **Monorepos** — dependency management, includes, and parallel execution
- **CI-integrated workflows** — group output, caching, JSON

If you're still using Make and find yourself fighting with tab sensitivity or cross-platform issues, Task is a drop-in quality-of-life upgrade.

---

## Related

- [nektos/act — Run GitHub Actions Locally](act.md) — Local CI testing
- [Dagger — A Better Way to Ship](dagger.md) — Programmable CI/CD platform
- [Taskfile.dev Documentation](https://taskfile.dev)
- [go-task/task on GitHub](https://github.com/go-task/task)
