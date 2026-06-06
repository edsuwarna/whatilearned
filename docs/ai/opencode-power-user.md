# OpenCode — Power User Guide


## Table of Contents

- [📋 Table of Contents](#table-of-contents)
- [1. 🤖 Custom Instructions (System Behavior)](#1-custom-instructions-system-behavior)
  - [Basic Setup](#basic-setup)
- [General Rules](#general-rules)
- [Output Preferences](#output-preferences)
- [Project Context](#project-context)
  - [Per-Project Override](#per-project-override)
- [Anjungan IDP Project](#anjungan-idp-project)
  - [What to Put in Instructions](#what-to-put-in-instructions)
- [2. ⌨️ TUI Keyboard Shortcuts](#2-tui-keyboard-shortcuts)
  - [Essential Shortcuts](#essential-shortcuts)
  - [Navigation](#navigation)
  - [Pro Tips](#pro-tips)
- [3. 🎯 Token Budget & Context Management](#3-token-budget-context-management)
  - [The 80/20 Rule of File Attachment](#the-8020-rule-of-file-attachment)
  - [When to Use `-f` vs Let It Discover](#when-to-use-f-vs-let-it-discover)
  - [Compact Strategy](#compact-strategy)
  - [Signs You Need to Reset](#signs-you-need-to-reset)
  - [Pro Tip: Session per Task](#pro-tip-session-per-task)
- [4. 🧠 Model Strategy with 9Router](#4-model-strategy-with-9router)
  - [Recommended Model Mapping](#recommended-model-mapping)
  - [Task-to-Model Mapping](#task-to-model-mapping)
  - [Switch Mid-Session](#switch-mid-session)
- [5. 🦸 Git Superpowers](#5-git-superpowers)
  - [Interactive Rebase Assistant](#interactive-rebase-assistant)
  - [Conflict Resolution](#conflict-resolution)
  - [Git Bisect with OpenCode](#git-bisect-with-opencode)
  - [Changelog Generation](#changelog-generation)
  - [PR Description Generator](#pr-description-generator)
  - [Commit Message with Full Context](#commit-message-with-full-context)
- [6. 🖥️ tmux + OpenCode Workflow](#6-tmux-opencode-workflow)
  - [Recommended Layout](#recommended-layout)
  - [tmux Script](#tmux-script)
  - [Workflow](#workflow)
- [7. 🔄 Session Management](#7-session-management)
  - [Fresh Session Checklist](#fresh-session-checklist)
  - [Session Start Template](#session-start-template)
  - [Session End Template](#session-end-template)
- [8. 🔒 Secrets & Sensitive Data Handling](#8-secrets-sensitive-data-handling)
  - [What NOT to Put in Context](#what-not-to-put-in-context)
  - [Safe Patterns](#safe-patterns)
  - [Dedicated Command: Sanitized File Review](#dedicated-command-sanitized-file-review)
  - [Using Environment Variables](#using-environment-variables)
- [9. 📚 Learning & Legacy Code Exploration](#9-learning-legacy-code-exploration)
  - [Unknown Codebase Onboarding](#unknown-codebase-onboarding)
  - [Deep Dive into a Module](#deep-dive-into-a-module)
  - [Generate Diagrams from Code](#generate-diagrams-from-code)
  - [Legacy Code Documentation](#legacy-code-documentation)
  - ["Why is this done this way?"](#why-is-this-done-this-way)
- [10. ⚙️ Config Reference (`~/.opencode.json`)](#10-config-reference-opencodejson)
  - [Key Options Explained](#key-options-explained)
  - [Recommended Config for Daily Use](#recommended-config-for-daily-use)
- [11. 🔗 OpenCode + GitHub CLI Integration](#11-opencode-github-cli-integration)
  - [Review Open PRs](#review-open-prs)
  - [Check Your Own PR Before Push](#check-your-own-pr-before-push)
  - [Auto-Generate PR from Branch](#auto-generate-pr-from-branch)
- [12. 🐛 Debugging OpenCode Itself](#12-debugging-opencode-itself)
  - [Check Config](#check-config)
  - [Check Logs](#check-logs)
  - [Common Issues & Fixes](#common-issues-fixes)
  - [Reset Everything](#reset-everything)
- [💡 Quick Reference Card](#quick-reference-card)

Config tweaks, keyboard shortcuts, token management, session hygiene, and workflows that make OpenCode faster, cheaper, and more precise.

> **Prerequisite**: OpenCode installed with 9Router or direct API key. See [opencode-daily-use-cases](opencode-daily-use-cases.md) for fundamentals.

---

## 📋 Table of Contents

- [1. Custom Instructions (System Behavior)](#1-custom-instructions-system-behavior)
- [2. TUI Keyboard Shortcuts](#2-tui-keyboard-shortcuts)
- [3. Token Budget & Context Management](#3-token-budget-context-management)
- [4. Model Strategy with 9Router](#4-model-strategy-with-9router)
- [5. Git Superpowers](#5-git-superpowers)
- [6. tmux + OpenCode Workflow](#6-tmux-opencode-workflow)
- [7. Session Management](#7-session-management)
- [8. Secrets & Sensitive Data Handling](#8-secrets-sensitive-data-handling)
- [9. Learning & Legacy Code Exploration](#9-learning-legacy-code-exploration)
- [10. Config Reference (`~/.opencode.json`)](#10-config-reference-opencode-json)
- [11. OpenCode + GitHub CLI Integration](#11-opencode-github-cli-integration)
- [12. Debugging OpenCode Itself](#12-debugging-opencode-itself)

---

## 1. 🤖 Custom Instructions (System Behavior)

OpenCode reads **`~/.opencode/instructions.md`** and injects it into every session. Use this to set global behavior without typing it every time.

### Basic Setup

```bash
mkdir -p ~/.opencode
```

**`~/.opencode/instructions.md`**:

```markdown
## General Rules
- Always check existing patterns before creating new code
- Prefer fewer files over many small files
- Use TypeScript with strict mode for JS projects
- Write tests alongside implementation
- Explain your reasoning for non-trivial decisions

## Output Preferences
- Use concise commit messages (conventional commits)
- Generate idiomatic code for the language
- Prefer async/await over callbacks
- Include error handling in all API endpoints
- Add input validation for all user-facing functions

## Project Context
- Docker Compose for local development
- GitHub Actions for CI/CD
- Deploy via Docker images to GHCR
- Health checks required on all services
```

### Per-Project Override

You can also have **`<project>/.opencode/instructions.md`** for project-specific behavior:

**`~/projects/anjungan/.opencode/instructions.md`**:

```markdown
## Anjungan IDP Project
- Tech: Go backend + SvelteKit frontend + Emerald CSS
- Database: PostgreSQL via Docker Compose
- Auth: JWT with email OTP
- Always use Emerald utility classes, not custom CSS
- Frontend text must be 100% English
- Backend uses chi router with standard middleware pattern
- Docker images go to reg.edsuwarna.xyz
```

### What to Put in Instructions

| Category | Example |
|----------|---------|
| **Tech stack** | Framework, language version, database |
| **Code style** | Naming conventions, file structure |
| **Testing** | Framework, coverage expectations |
| **Deployment** | Registry, CI/CD, hosting |
| **Security** | Auth method, secret management |
| **Gotchas** | Things OpenCode often gets wrong for this project |

---

## 2. ⌨️ TUI Keyboard Shortcuts

OpenCode TUI is keyboard-driven. These shortcuts save minutes every session.

### Essential Shortcuts

| Shortcut | Action | When to Use |
|----------|--------|-------------|
| **`Ctrl+P`** | Command palette | Run custom commands (from `commands/` dir) |
| **`Ctrl+K`** | Custom commands list | Browse and run `.md` command files |
| **`Ctrl+Shift+F`** | Search files | Find files by name or content |
| **`Ctrl+Shift+P`** | Model picker | Switch model mid-session |
| **`Ctrl+L`** | Clear chat | Start fresh visually (history preserved) |
| **`Ctrl+C`** | Interrupt | Stop a long generation or exit |
| **`Ctrl+Z`** | Undo last message | Undo last assistant response |
| **`Tab`** | Accept suggestion | Accept autocomplete / file path |
| **`Esc`** | Close panel | Close file preview, search, palette |

### Navigation

| Shortcut | Action |
|----------|--------|
| **`↑`/`↓`** | Scroll output / Navigate list |
| **`PgUp`/`PgDn`** | Page up/down in output |
| **`Home`/`End`** | Jump to top/bottom of output |
| **`Ctrl+U`** | Clear current input line |
| **`Ctrl+A`** | Go to beginning of input |
| **`Ctrl+E`** | Go to end of input |

### Pro Tips

- **`Ctrl+K` → type partial command name → Enter** is faster than finding files
- **`Ctrl+Shift+P`** to switch from cheap model (planning) to expensive model (implementation)
- **`Ctrl+L`** when output gets too long — doesn't lose context, just cleans display

---

## 3. 🎯 Token Budget & Context Management

OpenCode's biggest weakness is **context swamping** — too many files = confused agent. Manage your token budget aggressively.

### The 80/20 Rule of File Attachment

```
Don't attach → project has 50 files, attach all of them
Do attach    → project has 50 files, attach the 5 most relevant ones
```

### When to Use `-f` vs Let It Discover

| Situation | Strategy |
|-----------|----------|
| You know which file | Use `-f filename.ts` — saves tokens |
| You don't know | Describe the problem; OpenCode searches |
| Large codebase | Use `-f` on entry points + types only |
| Monorepo | **Always** `-f` scoped files, never whole repo |

### Compact Strategy

OpenCode has auto-compact (`autoCompact: true` in config). When enabled, it automatically summarizes older parts of the conversation to stay within context.

```bash
# Force compact mid-session (if feeling slow)
# Just type: "compact" or "summarize and continue"
```

### Signs You Need to Reset

| Symptom | Fix |
|---------|-----|
| OpenCode starts suggesting wrong approaches | Exit and restart fresh |
| It forgets what file it was editing | `Ctrl+C` → `o9` again |
| Output gets repetitive / vague | Context is full — restart |
| It suggests files that don't exist | Token budget exhausted |
| Response time increased significantly | Too much accumulated context |

### Pro Tip: Session per Task

```
Don't: One long session for "fix bugs in auth module, then add search feature, then deploy"
Do:   Three sessions — one per task
```

Each session starts fresh with focused context. No cross-task confusion.

---

## 4. 🧠 Model Strategy with 9Router

With 9Router you can switch between **cheap and expensive models** depending on the task. Configure this in `~/.opencode.json`.

### Recommended Model Mapping

```json
{
  "agents": {
    "coder": {
      "model": "local.kr/deepseek-v4-flash"
    },
    "planner": {
      "model": "local.kr/claude-sonnet-4"
    }
  },
  "autoCompact": true,
  "customCommands": [
    {
      "name": "plan",
      "prompt": "Design the architecture for {{task}}. Output a detailed plan with trade-offs before any code.",
      "args": ["task"]
    },
    {
      "name": "implement",
      "prompt": "Implement {{task}} following the existing patterns in the codebase.",
      "args": ["task"]
    },
    {
      "name": "review",
      "prompt": "Review {{file}} for bugs, security issues, and performance problems.",
      "args": ["file"]
    }
  ]
}
```

### Task-to-Model Mapping

| Task Type | Model | Reasoning |
|-----------|-------|-----------|
| Simple code gen | DeepSeek V4 Flash / GPT-4o Mini | Fast, cheap, good enough |
| Debugging | Claude Sonnet 4 | Better at reasoning through errors |
| Architecture / Plan | Claude Sonnet 4 / Opus | Needs deep reasoning |
| Refactoring | Claude Sonnet 4 | Understands implications of changes |
| Code review | DeepSeek V4 Flash | Good pattern matching, cheaper |
| Documentation | GPT-4o / DeepSeek | Creative writing, structure |
| Security audit | Claude Sonnet 4 | Security nuance matters |
| Docker / Infra | Claude Sonnet 4 | Multi-step reasoning needed |

### Switch Mid-Session

**`Ctrl+Shift+P`** in TUI → pick model → continue. Use cheap model for planning/exploration, then switch to expensive for implementation.

---

## 5. 🦸 Git Superpowers

OpenCode + Git is incredibly powerful when used right.

### Interactive Rebase Assistant

```bash
# Before an interactive rebase
o9r "I need to squash the last 3 commits and rewrite the middle commit message.
Current commits:
$(git log --oneline -5)

What's the rebase strategy?" --agent plan
```

### Conflict Resolution

```bash
# After a merge conflict
o9r "Resolve all merge conflicts in this project.
Approach:
1. Read both sides of each conflict
2. Choose the correct resolution (or merge both)
3. Keep functionality from both branches where possible
4. Remove conflict markers
5. Verify the file still makes sense as a whole

Focus on files with conflicts:" -f <(git diff --name-only --diff-filter=U)
```

### Git Bisect with OpenCode

```bash
# Automate bisect
git bisect start HEAD <known-good-commit>
git bisect run o9r "Is this commit ($(git log -1 --format=%h)) the one that broke the
login feature? Analyze the diff and tell me if it causes the bug.
Respond with ONLY 'y' (yes, it's bad) or 'n' (no, it's good)" -f <(git diff HEAD~1..HEAD) > /dev/null 2>&1 && echo "y" || echo "n"
```

### Changelog Generation

```bash
o9r "Generate a changelog from the diff between tag v1.0.0 and HEAD.
Group by:
- Features (feat)
- Bug Fixes (fix)
- Security (security)
- Performance (perf)
- Refactoring (refactor)
- Documentation (docs)

For each entry: component, summary, PR number if found" \
  -f <(git log v1.0.0..HEAD --oneline --no-decorate)
```

### PR Description Generator

```bash
o9r "Generate a PR description for branch $(git branch --show-current).
Include:
- What changed and why
- Key implementation details
- Breaking changes (if any)
- Testing done
- Screenshots if UI changes
- Deployment notes" \
  -f <(git diff main...HEAD --stat) -f <(git log main..HEAD --oneline)
```

### Commit Message with Full Context

```bash
alias o9commit='o9r "Generate a conventional commit message from this staged diff.
Focus on WHY the change was made, not just WHAT changed.
Format: type(scope): description

Types: feat, fix, refactor, chore, docs, test, perf, security, ci" \
  -f <(git diff --cached)'
```

---

## 6. 🖥️ tmux + OpenCode Workflow

Split your terminal into panes for maximum efficiency. tmux is ideal for this.

### Recommended Layout

```
┌──────────────────────────────┬──────────────────────────┐
│                              │                          │
│      OpenCode TUI            │     Terminal #1          │
│      (main workspace)        │     (docker logs,        │
│                              │      server output,      │
│                              │      test runner)        │
│                              │                          │
├──────────────────────────────┼──────────────────────────┤
│                              │                          │
│      Terminal #2             │     Terminal #3          │
│      (git, file ops,         │     (ssh to servers,     │
│       npm/pip commands)      │      kubectl,            │
│                              │      infrastructure)     │
│                              │                          │
└──────────────────────────────┴──────────────────────────┘
```

### tmux Script

**`~/.config/tmux-opencode.sh`**:

```bash
#!/bin/bash
SESSION="dev"

# Kill existing session if it exists
tmux kill-session -t $SESSION 2>/dev/null

# Create new session with 4 panes
tmux new-session -d -s $SESSION -n "opencode"

# Split horizontally (left-right)
tmux split-window -h -t $SESSION:0

# Split right pane vertically
tmux split-window -v -t $SESSION:0.1

# Split left pane vertically (bottom)
tmux split-window -v -t $SESSION:0.0

# Layout: left main + right stacked, then bottom-left
tmux select-layout -t $SESSION:0 tiled 2>/dev/null

# Resize: give more space to OpenCode pane
tmux resize-pane -t $SESSION:0.0 -x 60% 2>/dev/null

# Start OpenCode in main (top-left)
tmux send-keys -t $SESSION:0.0 "cd ~/projects/anjungan && o9" Enter

# Bottom-left: git + commands
tmux send-keys -t $SESSION:0.2 "cd ~/projects/anjungan && echo '→ git, npm, build commands here'" Enter

# Top-right: docker logs
tmux send-keys -t $SESSION:0.1 "cd ~/projects/anjungan && echo '→ docker logs, server output'" Enter

# Bottom-right: SSH / infra
tmux send-keys -t $SESSION:0.3 "echo '→ SSH, kubectl, infrastructure commands'" Enter

# Attach
tmux select-pane -t $SESSION:0.0
tmux attach-session -t $SESSION
```

Make it executable: `chmod +x ~/.config/tmux-opencode.sh`

Then alias in `~/.zshrc`:

```bash
alias dev='~/.config/tmux-opencode.sh'
```

### Workflow

```
Pane 1 (OpenCode)   ↔ "Fix this bug" → OpenCode works
Pane 3 (git/cmd)    ↔ git add, npm test, build while OpenCode thinks
Pane 2 (logs)       ↔ docker logs -f --tail 50 api — see real-time effects
Pane 4 (SSH/infra)  ↔ ssh server, check deployment, kubectl get pods
```

OpenCode generates → you test (Pane 3) → see logs (Pane 2) → deploy (Pane 4). All without switching windows.

---

## 7. 🔄 Session Management

Knowing **when to reset** is the difference between "OpenCode is amazing" and "OpenCode is stupid".

### Fresh Session Checklist

Start a new session when:

- [ ] **Task scope changed** — was fixing auth, now building a feature → reset
- [ ] **OpenCode is confused** — suggesting wrong files, wrong approach → reset
- [ ] **Response is slow** — accumulated context is bogging it down → reset
- [ ] **It keeps forgetting** — asks "what file?" when you already told it → reset
- [ ] **Cross-project contamination** — was in project A, now in project B → **must reset**

### Session Start Template

```bash
o9 "Context: I'm working on $(basename $(pwd)).
Today's task: [one sentence].
Files involved: [key files].
What I've done so far: [brief status].
Blockers: [if any].
Start with: [first action]."
```

This orients OpenCode instantly without it having to rediscover context.

### Session End Template

```bash
o9 "Summarize what we did this session:
- Files changed
- Key decisions made
- What's left to do
- Any gotchas for next time"
```

Useful before closing the terminal or switching tasks.

---

## 8. 🔒 Secrets & Sensitive Data Handling

OpenCode sends context to an AI provider. **Never** send secrets, keys, or production credentials.

### What NOT to Put in Context

| ❌ Dangerous | ✅ Safe |
|-------------|---------|
| `.env` file contents | `.env.example` (values redacted) |
| Production database URLs | "PostgreSQL on port 5432" |
| API keys / tokens | "The API key is in AWS Secrets Manager" |
| SSH private keys | "SSH key path: ~/.ssh/id_ed25519" |
| `kubeconfig` with live clusters | "K8s cluster with 3 nodes" |
| Cloud provider credentials | "AWS account, use IAM role" |

### Safe Patterns

```bash
# ❌ BAD: sends actual values
o9r "Analyze this .env:" -f .env

# ✅ GOOD: redact first
cp .env .env.redacted && sed -i 's/=.*/=REDACTED/' .env.redacted \
  && o9r "Check if these env vars are complete and correctly named" \
  -f .env.redacted && rm .env.redacted
```

### Dedicated Command: Sanitized File Review

**`review-config-safe.md`**:

```markdown
# Review Config: $FILE
Review this config file for issues.
⚠️ SENSITIVE: Do NOT display or transmit actual secret values.
Replace all password/token/key values with [REDACTED] in your output.

Check for:
- Missing required variables
- Typos in variable names
- Deprecated variable names
- Inconsistent naming convention
- Missing documentation comments
- Values that look suspicious (placeholder values left in)
```

### Using Environment Variables

OpenCode can read environment variables safely:

```bash
# Set in ~/.zshrc — OpenCode inherits them
export DEPLOY_ENV=staging
export PROJECT_ROOT=$HOME/projects/anjungan
```

Reference in prompts:

```bash
o9r "Deploy to $DEPLOY_ENV environment at $PROJECT_ROOT"
```

---

## 9. 📚 Learning & Legacy Code Exploration

OpenCode is a fantastic **learning tool** for unfamiliar codebases.

### Unknown Codebase Onboarding

```bash
o9 "I'm new to this project. Help me understand it:

1. One-paragraph summary: what does this do?
2. Walk me through the main flow:
   - Entry point → routes → controllers → services → data layer
3. What are the core abstractions? (classes, types, interfaces)
4. What patterns are used? (MVC, Repository, Event-driven)
5. Where are the tricky parts? (gotchas, tech debt, known issues)
6. How are errors handled?
7. Testing strategy?

Be thorough — I want to contribute to this codebase."
```

### Deep Dive into a Module

```bash
o9r "Deep dive into this module. Explain:
- What does each exported function do?
- What are the side effects?
- What assumptions does it make about input?
- What would break if I changed X?
- Are there tests I should look at?
- Any hidden dependencies?" -f src/services/paymentService.ts
```

### Generate Diagrams from Code

```bash
o9p "Generate a Mermaid.js sequence diagram from these controller files.
Show the request flow: HTTP → middleware → controller → service → database.
Include error paths (validation error, not found, server error)." \
  -f 'src/controllers/**/*.ts' -f 'src/services/**/*.ts' --agent plan
```

### Legacy Code Documentation

```bash
o9r "This file has no documentation and is critical to the system.
Read through it and add JSDoc comments explaining:
- What each function does (not how — that's the code)
- Expected inputs and outputs
- Side effects
- Error conditions
- Related functions" -f src/legacy/processor.js
```

### "Why is this done this way?"

```bash
o9r "I don't understand why this code exists. Explain:
- What problem does this solve?
- Why this approach instead of a simpler one?
- Is there historical context? (old API, migration, compatibility)
- Could it be removed or simplified now?
- What would break if I deleted it?" -f src/utils/weirdParser.ts
```

---

## 10. ⚙️ Config Reference (`~/.opencode.json`)

Full reference of config options and what they do.

```json
{
  "agents": {
    "coder": {
      "model": "local.kr/deepseek-v4-flash",
      "systemPrompt": "Optional: override default system prompt for this agent",
      "temperature": 0.3,
      "maxTokens": 8192
    },
    "planner": {
      "model": "local.kr/claude-sonnet-4",
      "temperature": 0.2,
      "maxTokens": 16384
    }
  },
  "autoCompact": true,
  "autoCompactThreshold": 0.75,
  "maxContextTokens": 32000,
  "customCommands": [
    {
      "name": "test",
      "prompt": "Write tests for {{file}}",
      "args": ["file"]
    }
  ],
  "mcpServers": {},
  "theme": {
    "accent": "green",
    "background": "dark"
  },
  "editor": "code",
  "diffEditor": true,
  "git": {
    "autoCommit": false,
    "commitMessageLang": "en"
  }
}
```

### Key Options Explained

| Option | Default | Description |
|--------|---------|-------------|
| `autoCompact` | `true` | Auto-summarize old messages when context gets full |
| `autoCompactThreshold` | `0.75` | Compact when context is 75% full (lower = more aggressive) |
| `maxContextTokens` | `32000` | Maximum tokens before compacting |
| `diffEditor` | `true` | Show diffs in side panel instead of inline |
| `editor` | system default | External editor for manual edits (`code`, `vim`, `cursor`) |
| `git.autoCommit` | `false` | Auto-commit after OpenCode makes changes (risky — keep off) |

### Recommended Config for Daily Use

```json
{
  "agents": {
    "coder": {
      "model": "local.kr/deepseek-v4-flash",
      "temperature": 0.3
    }
  },
  "autoCompact": true,
  "autoCompactThreshold": 0.7,
  "diffEditor": true,
  "customCommands": [
    { "name": "plan",     "prompt": "Design architecture for {{task}} with trade-offs", "args": ["task"] },
    { "name": "implement","prompt": "Implement {{task}} following existing patterns", "args": ["task"] },
    { "name": "review",   "prompt": "Review {{file}} for bugs and security issues", "args": ["file"] },
    { "name": "test",     "prompt": "Write unit tests for {{file}}", "args": ["file"] },
    { "name": "docs",     "prompt": "Document {{file}} with usage examples", "args": ["file"] },
    { "name": "refactor", "prompt": "Refactor {{file}} with explanation of changes", "args": ["file"] },
    { "name": "migrate",  "prompt": "Create DB migration for {{description}}", "args": ["description"] },
    { "name": "docker",   "prompt": "Create Dockerfile + compose for {{project}}", "args": ["project"] },
    { "name": "deploy",   "prompt": "Create deploy config for {{project}}", "args": ["project"] },
    { "name": "audit",    "prompt": "Security audit {{file}}", "args": ["file"] }
  ]
}
```

---

## 11. 🔗 OpenCode + GitHub CLI Integration

Combine `gh` CLI with OpenCode for a powerful PR workflow.

### Review Open PRs

```bash
# Review a PR without leaving terminal
o9r "Review this PR diff. Check for:
- Logic bugs and edge cases
- Security vulnerabilities
- Performance issues
- Missing tests
- Code style consistency

Rate each finding: critical / major / minor / suggestion" \
  -f <(gh pr view 42 --json body,title,additions,deletions,files \
    | jq -r '.title + "\n" + .body') \
  -f <(gh pr diff 42)
```

### Check Your Own PR Before Push

```bash
alias o9pr='o9r "Review my uncommitted changes before I push.
Check for:
- Debug code left in (console.log, println, debugger)
- Hardcoded secrets or test credentials
- Missing error handling
- TODO comments
- Breaking changes in types/interfaces
- Missing exports or re-exports

Rate each finding: critical / major / minor" \
  -f <(git diff main...$(git branch --show-current))'
```

### Auto-Generate PR from Branch

```bash
o9r "Generate a PR description for my current branch.
Branch: $(git branch --show-current)

Fetch the diff from main and describe:
- The problem being solved
- The approach taken
- Files changed summary
- Testing notes
- Deployment considerations" \
  -f <(git log main..HEAD --oneline --no-decorate) \
  -f <(git diff main...HEAD --stat)
```

---

## 12. 🐛 Debugging OpenCode Itself

When OpenCode behaves unexpectedly, here's how to diagnose.

### Check Config

```bash
cat ~/.opencode.json | jq .
```

### Check Logs

```bash
# OpenCode logs (if running in debug mode)
tail -f ~/.opencode/logs/*.log
```

### Common Issues & Fixes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Model not found" | 9Router provider name wrong | Check model name in `~/.opencode.json` |
| Slow responses | Context too full | `Ctrl+C` → restart fresh session |
| Wrong code style | Missing instructions | Update `~/.opencode/instructions.md` |
| Ignores `-f` files | File path typo or doesn't exist | Use absolute or verified relative paths |
| Keeps regenerating same thing | Temperature too high | Set `temperature: 0.3` in config |
| Crashes on startup | Config JSON syntax error | Validate: `cat ~/.opencode.json \| jq .` |
| Can't find custom commands | Wrong directory | Commands go in `~/.config/opencode/commands/` or `~/.opencode/commands/` |

### Reset Everything

```bash
# Start completely fresh
rm -rf ~/.opencode/
mkdir -p ~/.opencode/commands/
# Then reconfigure ~/.opencode.json
```

---

## 💡 Quick Reference Card

```bash
# ── Session Management ──
o9                                # Start TUI in current dir
Ctrl+C                            # Interrupt / exit
Ctrl+L                            # Clear display (keep context)

# ── Context ──
-f filename.ts                    # Attach file as context
-f src/ --agent plan              # Full directory + plan mode
-f <(command)                     # Pipe command output as context

# ── Model ──
Ctrl+Shift+P                      # Switch model mid-session
temperature: 0.3                  # Default for coding (lower = focused)

# ── Commands ──
Ctrl+K                            # Browse and run .md command files
Ctrl+P                            # Command palette (JSON commands)

# ── Git ──
-f <(git diff --cached)           # Staged diff as context
-f <(git log --oneline -10)       # Recent commits as context

# ── Safety ──
NEVER: -f .env                    # Don't send secrets
DO:    -f .env.example            # Send redacted version
```

---

*Last updated: June 2026*
