#!/usr/bin/env python3
"""Scan docs/ and generate nav.json for the WhatILearned SPA.

Auto-runs via .githooks/pre-commit before each commit.
Output: docs/nav.json — read by index.html to build nav + category pages.
"""

import json
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
OUTPUT_FILE = DOCS_DIR / "nav.json"

# Emoji & description for known categories — add new ones here if you want icons
CATEGORY_META = {
    "terminal": {"emoji": "🖥️", "desc": "ZSH, oh-my-zsh, colorls, terminal customization"},
    "security": {"emoji": "🔒", "desc": "Supply chain security, best practices"},
    "cloudflare": {"emoji": "☁️", "desc": "Pages, Workers, DNS, deployments"},
    "ai": {"emoji": "🤖", "desc": "AI agent frameworks, comparisons, deep dives"},
    "infrastructure": {"emoji": "⚙️", "desc": "Deployment, Docker, Traefik, Dokploy"},
    "compliance": {"emoji": "🛡️", "desc": "Compliance scanning, CIS benchmarks, Lynis"},
}

IGNORE_DIRS = {"images"}
IGNORE_FILES = {"index.html", "nav.json"}


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def main() -> int:
    if not DOCS_DIR.exists():
        print(f"❌ docs/ not found at {DOCS_DIR}")
        return 1

    categories = {}
    order: list[str] = []

    for child in sorted(DOCS_DIR.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in IGNORE_DIRS:
            continue

        slug = child.name
        articles = sorted(
            f.stem
            for f in child.iterdir()
            if f.suffix == ".md" and f.name not in IGNORE_FILES
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

    nav = {"categories": categories, "order": order}

    # Avoid unnecessary writes (preserves mtime for CF Pages cache)
    existing = None
    if OUTPUT_FILE.exists():
        try:
            existing = json.loads(OUTPUT_FILE.read_text())
        except json.JSONDecodeError:
            pass

    if existing == nav:
        print("✅ nav.json unchanged")
        return 0

    OUTPUT_FILE.write_text(json.dumps(nav, indent=2, ensure_ascii=False) + "\n")
    total = sum(len(c["articles"]) for c in categories.values())
    print(f"✅ Generated nav.json ({len(order)} categories, {total} articles)")
    return 0


if __name__ == "__main__":
    exit(main())
