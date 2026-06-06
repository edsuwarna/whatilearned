# nektos/act — Run GitHub Actions Locally

> **Last updated:** 2026-06-07
> **Version:** v0.2.89
> **Repo:** [nektos/act](https://github.com/nektos/act)
> **Docs:** https://nektosact.com
> **License:** MIT

## Overview

`act` lets you run [GitHub Actions](https://github.com/features/actions) workflows **locally** on your own machine using Docker containers. No more commit-push-wait cycles just to test a workflow change.

> *"Think globally, act locally"*

### Why Use It?

1. **Fast Feedback** — Test `.github/workflows/` changes immediately without pushing to GitHub
2. **Local Task Runner** — Replace `Makefile` with GitHub Actions workflows that double as CI pipelines
3. **Debugging** — Inspect container state, add debug steps, iterate rapidly
4. **CI Pre-flight** — Validate workflow syntax and execution before committing

### How It Works

```
act → reads .github/workflows/*.yml → pulls/builds Docker images →
determines execution path → runs each step in isolated containers →
all environment variables and filesystem mirror GitHub runners
```

---

## Installation

### Prerequisites

- **Docker** — installed and running (Engine API compatible)
- **OR** use `-self-hosted` platform suffix to run steps directly on the host (no Docker)

### Quick Install (Linux/macOS)

```bash
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash -s - -b /usr/local/bin
```

### Package Managers

| Manager | Command |
|---------|---------|
| **Homebrew** | `brew install act` |
| **Arch Linux** | `yay -S act` |
| **Chocolatey** (Windows) | `choco install act-cli` |
| **Scoop** (Windows) | `scoop install act` |
| **WinGet** (Windows) | `winget install nektos.act` |
| **GitHub CLI** | `gh extension install https://github.com/nektos/gh-act` |
| **Nix/NixOS** | `nix-env -iA nixpkgs.act` |
| **Fedora COPR** | `dnf copr enable rubenwardy/act && dnf install act` |
| **MacPorts** | `sudo port install act` |

### Build from Source

```bash
git clone git@github.com:nektos/act.git
cd act
make install    # requires Go 1.18+
```

### Verify

```bash
act --version
# act version 0.2.89
```

---

## Basic Usage

```bash
act [event name] [flags]
```

If no event name is given, defaults to `push`. If a workflow only handles one event type, that event is used automatically.

### Quick Examples

```bash
# Run ALL workflows (default event: push)
act

# Run workflows for a specific event
act pull_request
act push
act schedule
act workflow_dispatch

# List available workflows and their jobs
act -l
act -l pull_request

# Run a specific job
act -j test
act -j build

# Run a specific workflow file
act -W .github/workflows/ci.yml

# Validate workflow syntax (no containers)
act -n
act --dryrun
```

---

## Complete Flag Reference

### General

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--workflows` | `-W` | `./.github/workflows/` | Path to workflow file(s) or directory |
| `--directory` | `-C` | `.` | Working directory |
| `--actor` | `-a` | `nektos/act` | User that triggered the event |
| `--remote-name` | | `origin` | Git remote name for repo URL detection |
| `--github-instance` | | `github.com` | GitHub instance (use for GHES/self-hosted) |
| `--defaultbranch` | | | Main branch name |
| `--detect-event` | | `false` | Auto-detect event type from workflow |

### Execution Control

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--job` | `-j` | | Run a specific job ID |
| `--list` | `-l` | `false` | List workflows |
| `--graph` | `-g` | `false` | Draw workflow as visual dependency graph |
| `--watch` | `-w` | `false` | Watch files and re-run on changes |
| `--dryrun` | `-n` | `false` | Validate workflow without running containers |
| `--validate` | | `false` | Validate workflow schema |
| `--strict` | | `false` | Strict schema validation |
| `--concurrent-jobs` | | CPU count | Max parallel jobs |
| `--no-recurse` | | `false` | Don't scan subdirectories for workflows |

### Container & Docker

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--platform` | `-P` | | Custom Docker image per runner label |
| `--bind` | `-b` | `false` | Bind-mount working directory instead of copying |
| `--pull` | `-p` | `true` | Pull Docker images even if cached |
| `--rebuild` | | `true` | Rebuild local action Docker images |
| `--reuse` | `-r` | `false` | Keep containers between runs (maintain state) |
| `--rm` | | `false` | Auto-remove containers/volumes on failure |
| `--privileged` | | `false` | Run containers in privileged mode |
| `--userns` | | | User namespace to use |
| `--network` | | `host` | Docker network name |
| `--container-architecture` | | host arch | e.g. `linux/amd64` (requires Docker API 1.41+) |
| `--container-daemon-socket` | | default | Docker socket URI (`-` to disable) |
| `--container-options` | | | Extra Docker container options |
| `--container-cap-add` | | | Kernel capabilities to add (e.g. `SYS_PTRACE`) |
| `--container-cap-drop` | | | Kernel capabilities to remove |
| `--use-gitignore` | | `true` | Respect `.gitignore` when copying files |

### Secrets, Vars, Env & Inputs

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--secret` | `-s` | | Secret key=value (prompts if value omitted) |
| `--secret-file` | | `.secrets` | File to load secrets from |
| `--var` | | | Repository variable (e.g. `--var MYVAR=foo`) |
| `--var-file` | | `.vars` | File to load variables from |
| `--env` | | | Environment variable (e.g. `--env MYENV=foo`) |
| `--env-file` | | `.env` | File to load environment variables from |
| `--input` | | | Action input (e.g. `--input myinput=foo`) |
| `--input-file` | | `.input` | File to load action inputs from |
| `--insecure-secrets` | | `false` | **NOT RECOMMENDED** — show secrets in logs |

### Event & Matrix

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--eventpath` | `-e` | | Path to custom event JSON payload |
| `--matrix` | | | Filter matrix strategy (e.g. `--matrix node:18`) |

### Caching & Artifacts

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--artifact-server-path` | | | Enable artifacts with storage path |
| `--artifact-server-addr` | | outbound IP | Artifact server bind address |
| `--artifact-server-port` | | `34567` | Artifact server port |
| `--cache-server-path` | | `~/.cache/actcache` | Cache server storage |
| `--cache-server-addr` | | outbound IP | Cache server bind address |
| `--cache-server-port` | | `0` (random) | Cache server port |
| `--cache-server-external-url` | | | Cache server URL behind proxy |
| `--no-cache-server` | | `false` | Disable the cache server |
| `--action-cache-path` | | `~/.cache/act` | Path for cached actions |
| `--action-offline-mode` | | `false` | Don't re-download cached actions; work offline |
| `--use-new-action-cache` | | `false` | Enable new action cache system |

### Output

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--verbose` | `-v` | `false` | Verbose output |
| `--quiet` | `-q` | `false` | Disable step output logging |
| `--json` | | `false` | JSON-formatted logs |
| `--log-prefix-job-id` | | `false` | Use job ID prefix instead of full name |

### Miscellaneous

| Flag | Default | Description |
|------|---------|-------------|
| `--local-repository` | | Replace remote action with local folder |
| `--no-skip-checkout` | `false` | Use `actions/checkout` instead of local copy |
| `--bug-report` | `false` | Print system info for bug reports |
| `--man-page` | `false` | Print man page to stdout |
| `--list-options` | `false` | Print JSON of all compatible options |
| `--version` | | Print version |

---

## Configuration (.actrc)

`act` reads arguments from `.actrc` files in order (later overrides earlier):

1. **XDG path** — `~/.config/act/actrc`
2. **HOME** — `~/.actrc`
3. **Local** — `./.actrc` (per-project)
4. **CLI arguments** — highest priority

**Format:** One argument per line, no comments.

```bash
# ~/.actrc — global defaults
--container-architecture=linux/amd64
--action-offline-mode
--pull=false
-P ubuntu-latest=catthehacker/ubuntu:act-latest
```

---

## Runner Images

### Default Platform Mappings

`act` uses Docker images that simulate GitHub runner environments. Three tiers:

| GitHub Runner | Micro (minimal) | Medium (default) | Large (full) |
|---------------|----------------|-------------------|--------------|
| `ubuntu-latest` | `node:16-buster-slim` | `catthehacker/ubuntu:act-latest` | `catthehacker/ubuntu:full-latest` |
| `ubuntu-22.04` | `node:16-bullseye-slim` | `catthehacker/ubuntu:act-22.04` | `catthehacker/ubuntu:full-22.04` |
| `ubuntu-20.04` | `node:16-buster-slim` | `catthehacker/ubuntu:act-20.04` | `catthehacker/ubuntu:full-20.04` |
| `ubuntu-18.04` | `node:16-buster-slim` | `catthehacker/ubuntu:act-18.04` | `catthehacker/ubuntu:full-18.04` |

> **Note:** Micro images are minimal by design — they don't include all GitHub Actions runner tools. Medium is the default. Large images are full filesystem dumps of actual GitHub runners (~18GB for the `nektos/act-environments` variant).

### Custom Images

```bash
# Override per platform
act -P ubuntu-latest=ubuntu:latest
act -P ubuntu-22.04=my-custom-runner:22.04

# Multiple overrides
act -P ubuntu-18.04=nektos/act-environments-ubuntu:18.04 \
    -P ubuntu-latest=ubuntu:latest

# Run directly on host (no Docker container)
act -P ubuntu-latest=-self-hosted
act -P windows-latest=-self-hosted
act -P macos-latest=-self-hosted
```

---

## Secrets, Variables & Environment

### Secrets

```bash
# Inline value
act -s MY_SECRET=supersecret

# Read from environment (prompts if not set)
act -s MY_SECRET

# From file
act --secret-file my.secrets

# GITHUB_TOKEN for actions that need API access
act -s GITHUB_TOKEN="$(gh auth token)"
```

### Repository Variables

```bash
# Inline
act --var MY_VAR=somevalue

# From file
act --var-file my.vars
```

### Environment Variables

```bash
# Inline
act --env MY_ENV=value

# From .env file (default: ./.env)
act --env-file my.env
```

### File Format (.env / .secrets)

Uses `godotenv` format (Ruby's dotenv-compatible):

```bash
export MY_ENV='value'
PRIV_KEY="---...\nmulti-line\n...---"
SOME_VAR=SOME_VALUE
```

---

## Events & Custom Payloads

### Supported Event Names

`push` (default), `pull_request`, `schedule`, `workflow_dispatch`, and any [standard GitHub event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).

### Custom Payloads (`-e`)

Simulate specific event scenarios with JSON payloads:

```bash
act pull_request -e event.json
```

**pull_request.json:**

```json
{
  "pull_request": {
    "head": { "ref": "feature-branch" },
    "base": { "ref": "main" }
  }
}
```

**push with tag.json:**

```json
{
  "ref": "refs/tags/v1.0.0"
}
```

**workflow_dispatch.json:**

```json
{
  "inputs": {
    "NAME": "Manual Run",
    "VERSION": "1.2.3"
  }
}
```

---

## Skipping Jobs/Steps Locally

### Skip an Entire Job

Use a custom event property:

```yaml
jobs:
  deploy:
    if: ${{ !github.event.act }}  # Skip during local act runs
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy skipped locally"
```

Run with: `act -e event.json` where `event.json = { "act": true }`

### Skip a Single Step

Use the `ACT` environment variable (automatically set by `act`):

```yaml
steps:
  - name: Slack notification
    if: ${{ !env.ACT }}
    run: |
      curl -X POST https://hooks.slack.com/...
```

---

## Matrix Strategy

```bash
# Run only matrix configs with node:18
act push --matrix node:18

# Run only configs matching ALL criteria
act push --matrix node:18 --matrix os:ubuntu-latest

# Run multiple os values
act push --matrix os:ubuntu-latest --matrix os:macos-latest
```

> **Note:** You cannot add new matrix values not in the workflow. The workflow's `exclude` field takes precedence over `--matrix`.

---

## Artifacts

The artifact server is **disabled by default**. Enable it to use `actions/upload-artifact`:

```bash
act --artifact-server-path $PWD/.artifacts
```

**Supported:**
- `actions/upload-artifact@v3` and `@v4`
- `actions/download-artifact@v3` and `@v4` (same workflow run only)

**Not supported in v4:** cross-run, cross-workflow, or cross-repo artifact downloads.

---

## Offline Mode

```bash
act --action-offline-mode
```

- Stops pulling existing images
- Doesn't fail if cached actions exist and you're offline
- Still pulls missing actions/images on first run
- Works after at least one online run to populate cache
- Avoids rate limiting and timeout issues

---

## Watch Mode

Re-run workflows automatically when files change:

```bash
act --watch
act -w
```

Useful during active development of workflow files.

---

## Local Repository Override

Replace a remote action reference with a local directory — useful for testing private/unpublished actions:

```bash
act --local-repository "test/my-action@v1=/home/user/my-action"
act --local-repository "https://github.com/test/test@v0=/home/act/test"
```

---

## Dry Run & Validation

```bash
# Validate workflow without running containers
act --dryrun
act -n

# Validate with strict schema checking
act --validate --strict
```

---

## Debugging

```bash
# Verbose output with job ID prefix for easier reading
act -v --log-prefix-job-id

# Generate bug report (system info for issues)
act --bug-report

# JSON output for programmatic parsing
act --json
```

---

## Known Limitations

### Unsupported Features
- `services` in workflows (planned for future)
- Full Windows/macOS runner environments (Docker limitation)
- `systemd` inside containers
- Podman/containerd as alternative backends (Docker-only)
- Some runner-specific built-in tools

### Common Issues

**MODULE_NOT_FOUND (JavaScript actions):**
`act` copies the repo but doesn't run `npm install`. Pre-build dependencies or use `actions/checkout` with `node_modules` persisted.

**Missing tools in default images:**
Default images are minimal. Use full images for more complete environments:
```bash
act -P ubuntu-latest=catthehacker/ubuntu:full-latest
```
Or install tools in workflow steps.

---

## Integration with Gitea/Forgejo

`act` is the engine behind **Gitea Actions** and **Forgejo Actions**:

- [gitea/act](https://github.com/gitea/act) — Fork of nektos/act with Gitea-specific features
- [act_runner](https://github.com/gitea/act_runner) — Runner daemon that connects to Gitea/Forgejo via gRPC
- Workflows go in `.forgejo/workflows/` (or `.gitea/workflows/`)

If you run Forgejo self-hosted, you already have `act` technology running via `act_runner`.

---

## Practical Examples

### Test CI Before Push

```bash
# Run all workflows for push event
act push

# Run a specific job only
act -j test
act -j build

# List what would run
act -l
```

### Simulate Pull Request

```bash
# Create event payload
cat > pr.json << 'EOF'
{
  "pull_request": {
    "head": { "ref": "feature/awesome" },
    "base": { "ref": "main" }
  }
}
EOF

# Run PR checks locally
act pull_request -e pr.json
```

### Test Multiple Workflows

```bash
# Test all workflow files
for f in .github/workflows/*.yml; do
  echo "=== Testing $f ==="
  act -W "$f"
done
```

### Replace Makefile

```bash
# .actrc in repo root
--pull=false
--action-offline-mode
-P ubuntu-latest=catthehacker/ubuntu:act-latest

# Then use like Makefile targets
act -j test       # make test
act -j lint       # make lint
act -j build      # make build
```

### Full Matrix Subset Testing

```bash
# Quick test of specific combinations
act push --matrix node:18 --matrix os:ubuntu-latest
```

### Offline CI Development

```bash
act --action-offline-mode --pull=false
```

### Workflow Dispatch with Inputs

```bash
cat > dispatch.json << 'EOF'
{
  "inputs": {
    "environment": "staging",
    "version": "1.2.3"
  }
}
EOF

act workflow_dispatch -e dispatch.json --input environment=staging
```

---

## Summary

`act` is the most practical tool for:

- **Debugging** GitHub Actions workflows before committing
- **Teaching/learning** GitHub Actions without consuming CI minutes
- **Local CI** for projects that already have GitHub Actions defined
- **Gitea/Forgejo** users — it's the same engine powering your self-hosted CI

The workflow is the same everywhere: write your `.github/workflows/*.yml`, run `act`, iterate until green, then commit.

---

## Related

- [Forgejo CI/CD with Docker Compose](forgejo-cicd-docker-compose.md) — Self-hosted CI using act_runner
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [nektos/act on GitHub](https://github.com/nektos/act)
- [nektosact.com](https://nektosact.com) — Official user guide
