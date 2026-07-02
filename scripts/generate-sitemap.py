#!/usr/bin/env python3
"""Generate sitemap.xml from nav.json"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
NAV_FILE = DOCS_DIR / "nav.json"
SITEMAP_FILE = DOCS_DIR / "sitemap.xml"
BASE_URL = "https://notes.edsuwarna.id"

nav = json.loads(NAV_FILE.read_text())

urls = []
for cat, info in nav["categories"].items():
    for article in info["articles"]:
        path = f"{cat}/{article}"
        urls.append(f"  <url><loc>{BASE_URL}/#/{escape(path)}</loc></url>")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE_URL}/</loc></url>
{chr(10).join(urls)}
</urlset>
"""

SITEMAP_FILE.write_text(sitemap)
print(f"✅ Generated sitemap.xml with {len(urls) + 1} URLs")
