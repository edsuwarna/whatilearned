# Dagger — A Better Way to Ship

> **Last updated:** 2026-06-07
> **Version:** v0.21.4
> **Repo:** [dagger/dagger](https://github.com/dagger/dagger)
> **Docs:** https://docs.dagger.io
> **License:** Apache 2.0

## Table of Contents

- [Overview](#overview)
  - [What is Dagger?](#what-is-dagger)
  - [How It Works](#how-it-works)
  - [Why Dagger?](#why-dagger)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [macOS (Homebrew)](#macos-homebrew)
  - [Linux](#linux)
  - [Windows](#windows)
  - [Verify Installation](#verify-installation)
  - [Update](#update)
- [CLI Reference](#cli-reference)
  - [Core Commands](#core-commands)
  - [Module Commands](#module-commands)
  - [Toolchain Commands](#toolchain-commands)
  - [Global Flags](#global-flags)
- [Core Concepts](#core-concepts)
  - [Dagger Engine](#dagger-engine)
  - [Dagger SDK](#dagger-sdk)
  - [Modules](#modules)
  - [Functions](#functions)
  - [Toolchains](#toolchains)
  - [Checks](#checks)
  - [Core Types](#core-types)
- [SDK Quickstarts](#sdk-quickstarts)
  - [Go](#go)
  - [Python](#python)
  - [TypeScript](#typescript)
- [Features](#features)
  - [System API](#system-api)
  - [Incremental Execution & Caching](#incremental-execution--caching)
  - [Content-Addressable Types](#content-addressable-types)
  - [Built-in Observability](#built-in-observability)
  - [Multi-Language SDKs](#multi-language-sdks)
- [Practical Examples](#practical-examples)
  - [Go Build Pipeline](#go-build-pipeline-python-sdk)
  - [Multi-Arch Docker Build](#multi-arch-docker-build-go-sdk)
  - [CI/CD Pipeline](#cicd-pipeline-typescript-sdk)
  - [Dagger Cloud](#dagger-cloud)
- [Comparison with Other Tools](#comparison-with-other-tools)
  - [Dagger vs act](#dagger-vs-act)
  - [Dagger vs Taskfile](#dagger-vs-taskfile)
  - [Dagger vs Earthly](#dagger-vs-earthly)
  - [When to Use Dagger](#when-to-use-dagger)
- [Known Limitations](#known-limitations)
- [Summary](#summary)

---

## Overview

### What is Dagger?

Dagger is a programmable platform for automating software delivery — building, testing, and shipping applications reliably and at scale. It runs locally, in your CI server, or directly in Dagger Cloud.

Unlike traditional CI/CD tools that rely on shell scripts or proprietary YAML, Dagger provides a **complete execution engine with a system API**, **SDKs in 8 programming languages**, and a **rich ecosystem of reusable modules**.

### How It Works

```
Developer writes pipeline code (Go/Python/TS/etc.)
                    ↓
          Dagger CLI compiles & executes
                    ↓
         Dagger Engine orchestrates containers
                    ↓
        Everything runs in isolated containers
                    ↓
       Built-in caching → incremental execution
                    ↓
         Full OpenTelemetry tracing (TUI/export)
```

The Dagger Engine runs as a background daemon (via Docker), executing pipelines defined in any of the supported SDK languages. Each step runs in a container, artifacts are content-addressed, and caching is automatic.

### Why Dagger?

- **Programmable** — Full programming language power, not YAML templates. SDKs for Go, Python, TypeScript, Rust, Java, .NET, PHP, Elixir
- **Local-first** — Same pipeline runs identically on laptop, CI, or cloud
- **Repeatable** — Everything runs in containers, host dependencies are explicit and typed
- **Observable** — Every operation emits full OpenTelemetry traces with terminal TUI
- **Incremental** — Content-addressed caching; change one file, only affected ops re-run

---

## Installation

### Prerequisites

- A container runtime: Docker Desktop, Docker Engine, or compatible (Lima, Rancher Desktop, etc.)
- Linux: native container runtime
- macOS/Windows: Docker Desktop or equivalent

### macOS (Homebrew)

```bash
brew install dagger/tap/dagger
```

### Linux

```bash
curl -L https://dl.dagger.io/dagger/install.sh | sh
```

For a specific version:

```bash
curl -L https://dl.dagger.io/dagger/install.sh | DAGGER_VERSION=0.21.4 sh
```

With sudo to install to `/usr/local`:

```bash
curl -L https://dl.dagger.io/dagger/install.sh | sudo -E sh
```

### Windows

```bash
# PowerShell (as admin)
winget install Dagger.Dagger
```

Or via install script:

```powershell
curl -L https://dl.dagger.io/dagger/install.ps1 -o install.ps1
.\install.ps1
```

### Verify Installation

```bash
dagger version
# Expected: dagger v0.21.4 (registry.dagger.io/engine:v0.21.4) linux/amd64
```

### Update

```bash
brew upgrade dagger/tap/dagger      # Homebrew
dagger update                       # Self-update
```

---

## CLI Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `dagger` | Run a Dagger module / call SDK functions |
| `dagger version` | Show version info |
| `dagger login` | Authenticate to Dagger Cloud or registry |
| `dagger logout` | Clear authentication |

### Module Commands

| Command | Description |
|---------|-------------|
| `dagger develop` | Generate module SDK code and `dagger.json` config |
| `dagger install <module>` | Install a module dependency |
| `dagger uninstall <module>` | Remove a module dependency |
| `dagger init` | Initialize a new Dagger module |
| `dagger publish` | Publish a module to the Dagger registry |

### Toolchain Commands

| Command | Description |
|---------|-------------|
| `dagger toolchain install <name>` | Install a pre-built toolchain module |
| `dagger toolchain list` | List installed toolchains |

### Global Flags

| Flag | Description |
|------|-------------|
| `--debug` | Enable debug logging |
| `--progress` | Output mode: `auto`, `plain`, `tty` |
| `--help` | Show help |
| `-C <dir>` | Change working directory |

---

## Core Concepts

### Dagger Engine

The Dagger Engine is a background service that runs pipeline code. It:

- Starts automatically when you run `dagger` commands
- Runs as a Docker container (`registry.dagger.io/engine`)
- Orchestrates all pipeline containers
- Manages caching and content-addressed storage
- Supports concurrent pipeline execution

### Dagger SDK

SDKs let you write pipelines in your language of choice. Each SDK is generated from the Dagger API schema, providing full type safety and IDE support.

**Supported languages:**

| SDK | Package | Status |
|-----|---------|--------|
| **Go** | `dagger.io/dagger` | Stable |
| **Python** | `dagger` | Stable |
| **TypeScript** | `@dagger.io/dagger` | Stable |
| **Rust** | `dagger-sdk` | Beta |
| **Java** | `io.dagger.sdk` | Beta |
| **PHP** | `dagger/sdk` | Beta |
| **.NET** | `Dagger.SDK` | Beta |
| **Elixir** | `dagger` | Experimental |

### Modules

Modules are reusable, versioned packages of Dagger functions. They:

- Have a `dagger.json` manifest with metadata and dependencies
- Expose typed functions that can be called from other modules
- Can be published to and installed from the Dagger registry
- Support semantic versioning

```bash
dagger init                        # Create a new module
dagger install github.com/foo/bar  # Install a dependency
dagger publish                     # Publish to registry
```

### Functions

Functions are the building blocks of Dagger pipelines. A function:

- Takes typed inputs (strings, files, containers, secrets, etc.)
- Returns typed outputs
- Runs in a container
- Can call other functions
- Is automatically cached by its inputs

Functions compose naturally — the output of one function feeds into the next, and Dagger handles the container orchestration.

### Toolchains

Toolchains are pre-built modules for common development tools:

```bash
dagger toolchain install go       # Install Go toolchain
dagger toolchain install node     # Install Node.js toolchain
dagger toolchain install python   # Install Python toolchain
dagger toolchain install rust     # Install Rust toolchain
dagger toolchain list             # List installed
```

Toolchains provide ready-to-use functions like `go build`, `node test`, etc.

### Checks

Checks are declarative quality gates that validate your pipeline:

```yaml
# dagger.json
checks:
  lint:
    function: lint
    description: Run linter
  test:
    function: test
    description: Run tests
    depends_on: [lint]
```

Run all checks: `dagger check`

### Core Types

Dagger provides fundamental types that map to CI/CD primitives:

| Type | Description |
|------|-------------|
| `Container` | A container image with filesystem, entrypoint, env vars |
| `Directory` | A content-addressed filesystem directory |
| `File` | A single content-addressed file |
| `Secret` | An encrypted secret value (never logged) |
| `Service` | A network service that can be tunneled |
| `Socket` | A Unix or TCP socket |
| `GitRepository` | A git remote |
| `Module` | A Dagger module reference |

---

## SDK Quickstarts

### Go

```go
package main

import (
    "context"
    "dagger.io/dagger"
)

func main() {
    ctx := context.Background()
    client, _ := dagger.Connect(ctx)
    defer client.Close()

    // Build a Go project
    src := client.Host().Directory(".")
    build := client.Container().
        From("golang:1.22").
        WithDirectory("/src", src).
        WithWorkdir("/src").
        WithExec([]string{"go", "build", "-o", "app", "."})

    // Write binary to host
    build.File("/src/app").Export(ctx, "./app")
}
```

### Python

```python
import dagger

async def build():
    async with dagger.Connection() as client:
        src = client.host().directory(".")
        
        # Build
        build_container = (
            client.container()
            .from_("golang:1.22")
            .with_directory("/src", src)
            .with_workdir("/src")
            .with_exec(["go", "build", "-o", "app", "."])
        )

        # Export binary
        await build_container.file("/src/app").export("./app")

import asyncio
asyncio.run(build())
```

### TypeScript

```typescript
import { connect } from "@dagger.io/dagger"

async function build() {
    const client = await connect()
    
    const src = client.host().directory(".")
    const build = client
        .container()
        .from("golang:1.22")
        .withDirectory("/src", src)
        .withWorkdir("/src")
        .withExec(["go", "build", "-o", "app", "."])

    await build.file("/src/app").export("./app")
    client.close()
}

build()
```

---

## Features

### System API

The Dagger System API provides a cross-language interface for orchestrating:

- **Containers** — Build, run, compose, publish
- **Filesystems** — Directory/file operations with content-addressing
- **Secrets** — Secure handling of tokens, keys, passwords
- **Git** — Clone repositories, checkout branches
- **Networking** — Service tunnels, port forwarding
- **HTTP** — Fetch URLs, API calls

Every API operation is typed and composable — the output of one call feeds into the next.

### Incremental Execution & Caching

Dagger's caching is content-addressed:

- Every operation is keyed by a hash of all its inputs
- If nothing changed, the cached result is reused
- Caching works across local runs and CI — no shared volume needed
- Cache is stored in the Dagger Engine's content store

```python
# This cached step won't re-run if requirements.txt hasn't changed
python = (
    client.container()
    .from_("python:3.12")
    .with_directory("/src", src)
    .with_exec(["pip", "install", "-r", "/src/requirements.txt"])
)
```

### Content-Addressable Types

Artifacts are identified by their content hash:

- `Directory` and `File` types use content-addressable storage
- Same content = same hash = cached result
- Types can be passed across SDK boundaries without serialization
- No need to manage artifact storage manually

### Built-in Observability

Every Dagger operation emits OpenTelemetry spans:

```
dagger build
  ✓ Connect to engine         0.02s
  ✓ Resolve module            0.15s
  ✓ Build Go binary          12.34s
    │ compile main.go        8.21s
    │ link binary             4.13s
  ✓ Export artifact           0.05s
```

- Live TUI in terminal during execution
- Export to Jaeger, Honeycomb, or any OTel backend
- Granular spans per operation
- Logs and metrics per span

### Multi-Language SDKs

All SDKs are generated from the same API schema:

- Full type safety with native language types
- IDE autocomplete and documentation
- Consistent API across languages
- Same pipeline, different language

---

## Practical Examples

### Go Build Pipeline (Python SDK)

```python
import dagger

async def pipeline():
    async with dagger.Connection() as client:
        src = client.host().directory(".")
        
        # Lint
        lint = (
            client.container()
            .from_("golangci/golangci-lint:latest")
            .with_directory("/src", src)
            .with_workdir("/src")
            .with_exec(["golangci-lint", "run", "./..."])
        )
        
        # Test
        test = (
            client.container()
            .from_("golang:1.22")
            .with_directory("/src", src)
            .with_workdir("/src")
            .with_exec(["go", "test", "-race", "-cover", "./..."])
        )
        
        # Build
        build = (
            client.container()
            .from_("golang:1.22")
            .with_directory("/src", src)
            .with_workdir("/src")
            .with_env_variable("CGO_ENABLED", "0")
            .with_exec(["go", "build", "-o", "app", "."])
        )
        
        # Export
        await build.file("/src/app").export("./app")
        
        return "Pipeline complete"

import asyncio
asyncio.run(pipeline())
```

### Multi-Arch Docker Build (Go SDK)

```go
package main

import (
    "context"
    "dagger.io/dagger"
)

func main() {
    ctx := context.Background()
    client, _ := dagger.Connect(ctx)
    defer client.Close()

    src := client.Host().Directory(".")

    platforms := []dagger.Platform{
        "linux/amd64",
        "linux/arm64",
    }

    var imageRefs []string
    for _, platform := range platforms {
        build := client.Container(dagger.ContainerOpts{Platform: platform}).
            From("alpine:latest").
            WithDirectory("/src", src).
            WithWorkdir("/src").
            WithExec([]string{"go", "build", "-o", "app", "."})

        addr, _ := build.Publish(ctx, "ghcr.io/myorg/myapp:latest")
        imageRefs = append(imageRefs, addr)
    }
}
```

### CI/CD Pipeline (TypeScript SDK)

```typescript
import { connect } from "@dagger.io/dagger"

async function cicd() {
    const client = await connect()
    const src = client.host().directory(".")

    // Build
    const builder = client
        .container()
        .from("node:20-alpine")
        .withDirectory("/src", src)
        .withWorkdir("/src")
        .withExec(["npm", "ci"])
        .withExec(["npm", "run", "build"])

    // Test
    const tester = client
        .container()
        .from("node:20-alpine")
        .withDirectory("/src", src)
        .withWorkdir("/src")
        .withExec(["npm", "ci"])
        .withExec(["npm", "test"])

    // Run both
    await tester.stdout()
    await builder.directory("dist").export("./dist")
    
    client.close()
}

cicd()
```

### Dagger Cloud

Dagger Cloud runs your pipelines on Dagger's infrastructure:

- **No CI setup** — your `dagger` pipelines work as-is
- **Shared cache** — cache persists across CI runs globally
- **Traces** — Full pipeline traces in web UI
- **Team features** — secrets management, audit logs

```bash
dagger login           # Authenticate
dagger ...              # Pipelines can now run on Dagger Cloud
```

---

## Comparison with Other Tools

### Dagger vs act

| Aspect | Dagger | act (nektos/act) |
|--------|--------|-------------------|
| **Purpose** | Universal CI/CD platform | Run GitHub Actions locally |
| **Pipeline format** | Code (Go/Python/TS/etc.) | YAML workflows |
| **Scope** | Build, test, deploy anything | GitHub Actions workflow testing |
| **CI integration** | Runs in any CI or standalone | GitHub Actions only |
| **Learning curve** | Steep (SDK, concepts) | Low (YAML) |
| **Reusability** | Modules, types, functions | Actions |
| **Observability** | Full OTel traces + TUI | Verbose logs |
| **When to use** | Full CI/CD platform need | Quick local testing of GH Actions |

### Dagger vs Taskfile

| Aspect | Dagger | Task (go-task/task) |
|--------|--------|---------------------|
| **Purpose** | CI/CD orchestration | Local task runner |
| **Language** | Go/Python/TS code | YAML |
| **Runtime** | Containers (Docker) | Shell (host) |
| **Caching** | Content-addressed, distributed | Local checksum/timestamp |
| **Remote execution** | Built-in (Dagger Cloud) | No |
| **Complexity** | High (needs SDK knowledge) | Low (YAML only) |
| **Best for** | Full pipeline automation | Replacing Makefile / task automation |

### Dagger vs Earthly

| Aspect | Dagger | Earthly |
|--------|--------|---------|
| **Language** | General-purpose SDKs | Earthfile (Dockerfile-like) |
| **Philosophy** | Programmable platform | Build tool with Makefile DX |
| **Caching** | Content-addressed + distributed | Layer caching + distributed |
| **Target audience** | Platform engineers, DevOps | Developers familiar with Docker |
| **Maturity** | Newer (v0.x) | More mature |

### When to Use Dagger

- **Complex multi-stage pipelines** that need real programming language features
- **Multi-language monorepos** — each service can use its own SDK/language
- **CI/CD portability** — same pipeline on laptop, CI, or cloud
- **Need observability** — full traces, not just log scraping
- **Team platform** — reusable modules, shared caching, typed contracts
- **Already using containers** — natural fit for containerized workflows

---

## Known Limitations

1. **Steep learning curve** — Understanding the SDK, engine, modules, and type system takes time
2. **Docker dependency** — Requires a container runtime; no native host execution
3. **SDKs not all stable** — Go, Python, TypeScript are stable; others (Rust, Java, .NET, PHP) are still beta
4. **Young ecosystem** — Fewer modules and community resources than mature tools
5. **Dagger Cloud cost** — Free tier available, but advanced features require payment
6. **Debugging complexity** — Containerized execution adds indirection compared to direct shell commands
7. **Engine overhead** — Engine startup time adds a few seconds, noticeable for very short pipelines
8. **No direct GitHub Actions testing** — Unlike `act`, you can't drop-in test `.github/workflows/`

---

## Summary

Dagger is best suited when you need a **programmable, portable, observable CI/CD platform** that scales from local development to production CI. It's overkill if you just want to test GitHub Actions locally (use `act`) or replace a Makefile (use `Taskfile`). But for complex pipelines that need real programming language power, cross-platform portability, and built-in observability, Dagger is a compelling choice.

### Quick Decision Guide

```
Just test GitHub Actions locally? → act
Replace Makefile / task runner?  → Taskfile / Just
Full CI/CD pipeline platform?    → Dagger / Earthly
Need portable, observable CI?    → Dagger
Need Dockerfile-like simplicity? → Earthly
```

---

## Related

- [nektos/act — Run GitHub Actions Locally](act.md) — Local GitHub Actions testing
- [Taskfile.dev — Modern Task Runner](taskfile.md) — YAML-based task runner
- [Dagger Documentation](https://docs.dagger.io)
- [Dagger GitHub](https://github.com/dagger/dagger)
- [Dagger Cloud](https://dagger.io/cloud)
