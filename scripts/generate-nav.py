#!/usr/bin/env python3
"""Scan docs/ and generate nav.json + auto-update README.md for the WhatILearned SPA.

Auto-runs via .githooks/pre-commit before each commit.
Output: docs/nav.json — read by index.html to build nav + category pages.
        README.md — category article listings synced with actual files.
"""

import json
import subprocess
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
NAV_FILE = DOCS_DIR / "nav.json"
README_FILE = DOCS_DIR.parent / "README.md"

# Emoji & description for known categories
CATEGORY_META = {
    "terminal": {"emoji": "🖥️", "desc": "ZSH, oh-my-zsh, colorls, terminal customization"},
    "security": {"emoji": "🔒", "desc": "Supply chain security, best practices"},
    "cloudflare": {"emoji": "☁️", "desc": "Pages, Workers, DNS, deployments"},
    "ai": {"emoji": "🤖", "desc": "AI agent frameworks, comparisons, deep dives"},
    "infrastructure": {"emoji": "⚙️", "desc": "Deployment, Docker, Traefik, Dokploy"},
    "compliance": {"emoji": "🛡️", "desc": "CIS benchmarks, Lynis, Anjungan \u2014 plus 30+ technology compliance standards"},
}
DATES_FILE = DOCS_DIR / "article-dates.json"
IGNORE_DIRS = {"images"}
IGNORE_FILES = {"index.html", "nav.json"}

# Predefined descriptions for articles (editorial quality > auto-extracted)
ARTICLE_DESCS = {
    "ai/9router-free-ai-router": "Setup guide for 9Router: free AI gateway for OpenCode, Claude Code, and other CLI tools",
    "ai/claw-framework-comparison": "Side-by-side comparison of OpenClaw, Hermes Agent, Nanoclaw, and Picoclaw AI agent frameworks",
    "ai/google-ai-studio-free-models": "Google AI Studio free tier models, rate limits, and API access guide",
    "ai/opencode-advanced-tips": "Advanced OpenCode workflows: live log tailing, SSH analysis, MCP servers, incident response, per-project commands, and SRE emergency kit",
    "ai/opencode-agent-skills": "OpenCode agent skills reference: open-source SKILL.md repositories, skill managers (skillkit, agnix), and cross-tool compatibility",
    "ai/opencode-commands-by-role": "OpenCode custom commands organized by engineering role: Developer, DevOps, SRE, Cloud, and Infrastructure",
    "ai/opencode-daily-use-cases": "Real-world daily use cases for OpenCode: coding, debugging, refactoring, Docker, CI/CD, security, and devops workflows",
    "ai/opencode-power-user": "OpenCode power user guide: custom instructions, TUI shortcuts, token management, model strategy, git superpowers, tmux workflow, and session hygiene",
    "ai/picoclaw-deep-dive": "Comprehensive deep dive into Picoclaw (sipeed/picoclaw), the ultra-lightweight Go-based AI agent framework",
    "career/upwork-profile": "Upwork profile optimization guide: headline, overview, portfolio, specialized profiles, and pricing strategy",
    "cloudflare/deploy-littlelink-to-cloudflare-pages": "Step-by-step guide to deploy LittleLink on Cloudflare Pages",
    "compliance/anjungan-compliance-scanner": "Automated compliance scanning for internal tools using CIS benchmarks and Lynis",
    "compliance/standards/01-governance-risk": "Governance & risk management compliance standards",
    "compliance/standards/02-server-infrastructure": "Server infrastructure security standards",
    "compliance/standards/03-cloud-saas": "Cloud & SaaS compliance standards",
    "compliance/standards/04-finance-payment": "Finance & payment industry compliance (PCI DSS, etc.)",
    "compliance/standards/05-healthcare-privacy": "Healthcare & privacy compliance (HIPAA, GDPR, etc.)",
    "compliance/standards/06-container-devops": "Container & DevOps compliance standards",
    "compliance/standards/07-regional-standards": "Regional compliance standards (Indonesia, EU, US)",
    "compliance/standards/README": "Overview of 30+ technology compliance standards mapped to ISO 27001 controls",
    "infrastructure/act": "Run GitHub Actions workflows locally with nektos/act: installation, CLI reference, runner images, secrets, events, and practical examples",
    "infrastructure/chisel": "Chisel: fast TCP/UDP tunnel over HTTP, alternative to frp and ngrok — client-server architecture",
    "infrastructure/dex-oidc": "Dex OIDC — federated OpenID Connect identity provider for self-hosted apps (Zot, Forgejo, Beszel)",
    "infrastructure/database-backup": "Database backup guide for PostgreSQL, MySQL, and MariaDB: dedicated users, strategies, automation scripts, and test restore",
    "infrastructure/database-backup-incremental": "Incremental database backup guide: pgBackRest, WAL archiving, XtraBackup, binary logs, MariaDB Backup — with tool comparison and pitfalls",
    "infrastructure/dagger": "Programmable CI/CD platform: SDKs in 8 languages, content-addressed caching, built-in tracing, Dagger Cloud",
    "infrastructure/dokploy-basic-auth": "Adding basic auth to Compose applications on Dokploy via Traefik middleware",
    "infrastructure/forgejo-cicd-docker-compose": "Self-hosted Forgejo with CI/CD (Forgejo Actions) using Docker Compose",
    "infrastructure/forgejo-mirror-github": "Mirror GitHub repositories to Forgejo via UI migration or CLI",
    "infrastructure/forgejo-storage": "Forgejo storage architecture, backup, cleanup, and Docker build cache management",
    "infrastructure/glibc-vs-musl": "Comprehensive comparison: architecture, performance, static linking, Docker implications, DNS, threading, and when to choose which C library",
    "infrastructure/kata-containers-vs-firecracker": "Comparison of Kata Containers and Firecracker for lightweight virtualization",
    "infrastructure/kopia-backup": "Kopia backup with Cloudflare R2: incremental, dedup, encrypted backup for VPS",
    "infrastructure/object-storage-comparison": "Comparison of S3-compatible object storage providers: R2, S3, GCS, Backblaze B2",
    "infrastructure/taskfile": "Modern YAML-based task runner: dependencies, caching, templates, includes, platform-specific commands",
    "infrastructure/wireguard": "WireGuard VPN: installation, hub & spoke topology, site-to-site, NAT traversal, advanced config, security, and migration from OpenVPN",
    "infrastructure/netbird-selfhosted": "Self-hosted Netbird WireGuard mesh VPN with SSO, groups, policies, TURN relay, and routing peers",
    "infrastructure/netmaker-selfhosted": "Self-hosted Netmaker WireGuard mesh VPN platform: installation, ingress/egress gateways, ACL, and automation",
    "infrastructure/zot-registry": "Lightweight OCI-compliant container registry with Zot: deployment, auth, R2 storage, CVE scanning",
    "infrastructure/beszel": "Beszel — lightweight server monitoring with historical data, Docker stats, alerts, and OIDC/OAuth support",
    "infrastructure/dozzle": "Dozzle — real-time Docker log viewer with forward-proxy OIDC auth via Dex and oauth2-proxy",
    "security/supply-chain-security": "Open source supply chain security prevention playbook",
    "terminal/colorls": "Beautify your ls command with color and icons",
    "terminal/customize-terminal": "ZSH + oh-my-zsh installation guide",
}


CATEGORY_DISPLAY = {
    "ai": "AI",
    "career": "Career",
    "cloudflare": "Cloudflare",
    "compliance": "Compliance",
    "infrastructure": "Infrastructure",
    "security": "Security",
    "terminal": "Terminal",
}


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def generate_nav_json() -> tuple[dict, list[dict]]:
    """Scan docs/ dirs and return (nav, article_list)."""
    categories = {}
    order: list[str] = []
    all_articles: list[dict] = []

    for child in sorted(DOCS_DIR.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in IGNORE_DIRS:
            continue

        slug = child.name
        articles = sorted(
            str(f.relative_to(child).with_suffix(""))
            for f in child.rglob("*.md")
            if f.name not in IGNORE_FILES
        )
        if not articles:
            continue

        meta = CATEGORY_META.get(slug, {"emoji": "📁", "desc": slug_to_title(slug)})
        categories[slug] = {
            "emoji": meta["emoji"],
            "desc": meta["desc"],
            "articles": articles,
        }
        order.append(slug)

        for art in articles:
            path = f"{slug}/{art}"
            all_articles.append({
                "cat": slug,
                "path": path,
                "article": art,
                "emoji": meta["emoji"],
                "desc": ARTICLE_DESCS.get(path, ""),
            })

    nav = {"categories": categories, "order": order}
    return nav, all_articles


def write_nav_json(nav: dict) -> bool:
    """Write nav.json. Returns True if changed."""
    existing = None
    if NAV_FILE.exists():
        try:
            existing = json.loads(NAV_FILE.read_text())
        except json.JSONDecodeError:
            pass

    if existing == nav:
        print("✅ nav.json unchanged")
        return False

    NAV_FILE.write_text(json.dumps(nav, indent=2, ensure_ascii=False) + "\n")
    total = sum(len(c["articles"]) for c in nav["categories"].values())
    print(f"✅ Generated nav.json ({len(nav['order'])} categories, {total} articles)")
    return True


def generate_readme_section(nav: dict, articles: list[dict]) -> str:
    """Generate the article listing section of README.md."""
    lines = []
    for cat in nav["order"]:
        info = nav["categories"][cat]
        lines.append(f"### {info['emoji']} {CATEGORY_DISPLAY.get(cat, cat.capitalize())}")
        for art in info["articles"]:
            path = f"{cat}/{art}"
            desc = ARTICLE_DESCS.get(path, "")
            lines.append(f"- **[docs/{path}.md](docs/{path}.md)** — {desc}")
        lines.append("")
    return "\n".join(lines)


def write_readme(nav: dict, articles: list[dict]) -> bool:
    """Update README.md article listing. Keeps header/footer intact."""
    if not README_FILE.exists():
        print(f"❌ README.md not found at {README_FILE}")
        return False

    content = README_FILE.read_text()
    new_section = generate_readme_section(nav, articles)

    # Find the first '###' after the intro
    # The intro section ends at '---' + disclaimer line + blank line
    marker = "> 🤖 Some content in this repository is generated with the assistance of AI. All content is reviewed, edited, and curated manually to ensure accuracy and relevance."

    if marker in content:
        # Keep everything up to and including the disclaimer line
        header_end = content.index(marker) + len(marker)
        # Keep the two blank lines after disclaimer, then our new content
        new_content = content[:header_end] + "\n\n" + new_section
    else:
        # Fallback: find first ### and replace from there
        first_cat = content.find("\n### ")
        if first_cat == -1:
            new_content = content + "\n\n" + new_section
        else:
            new_content = content[:first_cat] + "\n\n" + new_section

    if content == new_content:
        print("✅ README.md unchanged")
        return False

    README_FILE.write_text(new_content)
    print(f"✅ Updated README.md ({len(nav['order'])} categories)")
    return True


def generate_article_dates(articles: list[dict]) -> dict:
    """Generate last-updated dates for each article from git log."""
    repo_root = Path(__file__).resolve().parent.parent
    dates = {}
    for art in articles:
        md_path = DOCS_DIR / f"{art['path']}.md"
        if not md_path.exists():
            continue
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ai", "--", str(md_path.relative_to(repo_root))],
                capture_output=True, text=True, cwd=repo_root, timeout=5,
            )
            date_str = result.stdout.strip()
            if date_str:
                # "2024-12-25 14:30:00 +0700" → "Dec 25, 2024"
                parts = date_str.split()
                if parts:
                    from datetime import datetime
                    dt = datetime.strptime(parts[0], "%Y-%m-%d")
                    dates[art["path"]] = dt.strftime("%b %d, %Y")
        except Exception:
            pass
    return dates


def write_article_dates(dates: dict) -> bool:
    """Write article-dates.json. Returns True if changed."""
    existing = None
    if DATES_FILE.exists():
        try:
            existing = json.loads(DATES_FILE.read_text())
        except json.JSONDecodeError:
            pass

    if existing == dates:
        print("✅ article-dates.json unchanged")
        return False

    DATES_FILE.write_text(json.dumps(dates, indent=2, ensure_ascii=False) + "\n")
    print(f"✅ Generated article-dates.json ({len(dates)} dates)")
    return True


def main() -> int:
    if not DOCS_DIR.exists():
        print(f"❌ docs/ not found at {DOCS_DIR}")
        return 1

    nav, all_articles = generate_nav_json()
    write_nav_json(nav)
    write_readme(nav, all_articles)
    dates = generate_article_dates(all_articles)
    write_article_dates(dates)
    return 0


if __name__ == "__main__":
    exit(main())
