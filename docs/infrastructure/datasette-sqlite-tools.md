# Datasette & Open-Source SQLite Tools with Web UI

A curated list of open-source tools that enhance SQLite with a **web UI**, auto-generated APIs, and extra features — for exploring, managing, and serving SQLite databases without writing boilerplate.

---

## 1. Datasette (Recommended)

[datasette.io](https://datasette.io) — by Simon Willison (Datasette Project)

| Feature | Detail |
|---|---|
| Web UI | ✅ Built-in browser with live SQL query editor |
| REST API | ✅ Auto-generated for every table/view |
| Full-Text Search | ✅ Built-in FTS5 support |
| Plugins | 100+ plugins (charts, geospatial, auth, publish) |
| Deployment | `pip install datasette`, single binary, or Docker |
| Use Case | Explore any SQLite DB instantly with a UI + API |

### Quick Start

```bash
pip install datasette
datasette mydata.db --host 0.0.0.0 --port 8080
```

### Key Features

- **Faceted browsing** — click any value to filter, like a spreadsheet
- **SQL query editor** — run arbitrary SQL, save queries as canned
- **CSV/JSON export** — every table/query downloadable
- **Metadata & plugins** — custom pages, auth, geospatial, charts (datasette-chartjs)
- **Publish** — deploy to Cloud Run, Fly.io, Vercel, or Heroku in one command

### Docker

```yaml
services:
  datasette:
    image: datasetteproject/datasette
    container_name: datasette
    volumes:
      - ./data:/data
    ports:
      - "8080:8081"
    command: datasette -p 8081 -h 0.0.0.0 /data/*.db
```

---

## 2. Turso / libSQL

[turso.tech](https://turso.tech) | [github.com/tursodatabase/libsql](https://github.com/tursodatabase/libsql)

A **fork of SQLite** with built-in enhancements:

- Row-level replication & branching (like Git for databases)
- HTTP protocol (connect over REST instead of SQL)
- Vector search support
- Embedded + server modes (via `sqld`)
- **Turso Studio** — web UI for managing databases
- Both managed (Turso Cloud) and self-hosted

```bash
# Self-host with sqld
docker run -d --name sqld -p 8080:8080 \
  -v sqld-data:/var/lib/sqld \
  ghcr.io/tursodatabase/sqld:latest
```

---

## 3. SQLPage

[sql-page.com](https://sql-page.com) | [github.com/lovasoa/SQLPage](https://github.com/lovasoa/SQLPage)

Write **SQL queries → web UI** automatically. No HTML, no JS.

- Single Rust binary, ~8MB, ultra lightweight
- Write `.sql` files, get rendered pages with charts, cards, forms, tables
- Built-in components: `card`, `chart`, `form`, `table`, `list`, `map`, `timeline`
- Authentication via HTTP basic auth or OIDC

```sql
-- myfile.sql → becomes a web page
SELECT 'title' as component, 'Dashboards' as contents;
SELECT 'chart' as component, 'Weekly Active Users' as title, 'bar' as type;
SELECT day, COUNT(*) AS value FROM events GROUP BY day ORDER BY day;
```

```bash
docker run -p 8080:8080 -v ./sql:/etc/sqlpage lovasoa/sqlpage
```

---

## 4. Directus

[directus.io](https://directus.io) | [github.com/directus/directus](https://github.com/directus/directus)

Headless CMS that works with SQLite (also MySQL/PostgreSQL).

- Auto-generates REST + GraphQL API from schema
- **Polished admin UI** — drag & drop, roles, file manager, rich text, WYSIWYG
- Extensions via Flows (no-code automations)
- Built-in auth, permissions, activity log

```yaml
services:
  directus:
    image: directus/directus:11
    container_name: directus
    ports:
      - "8055:8055"
    volumes:
      - directus-data:/directus/database
      - directus-uploads:/directus/uploads
    environment:
      DB_CLIENT: sqlite3
      DB_FILENAME: /directus/database/data.db
      ADMIN_EMAIL: admin@example.com
      ADMIN_PASSWORD: changeme
```

---

## 5. NocoDB

[nocodb.com](https://nocodb.com) | [github.com/nocodb/nocodb](https://github.com/nocodb/nocodb)

Open-source **Airtable alternative** with SQLite backend.

- Spreadsheet-like interface: grid, form, kanban, gallery views
- Filter, sort, group, rollup, lookup (like Airtable)
- Auto-generated REST & GraphQL APIs
- Team collaboration with roles and permissions

```bash
docker run -d --name nocodb \
  -p 8080:8080 \
  -v nocodb-data:/usr/app/data \
  nocodb/nocodb:latest
```

---

## Comparison Table

| Tool | Weight | Setup | Web UI Quality | Extra Features | Best For |
|---|---|---|---|---|---|
| **Datasette** | 🪶 Light | `pip install` | ✅ Good | FTS, facets, plugins, publish | Explore & serve SQLite DBs |
| **Turso/libSQL** | 🪶 Light | Docker | ✅ Studio | Replication, branching, vector search | Enhanced SQLite engine |
| **SQLPage** | 🪶 Ultra-light | Single binary | ✅ Auto | Query→UI components | Internal tools, dashboards |
| **Directus** | 🐋 Heavy | Docker | ✅✅ Excellent | Roles, files, rich text, flows | Admin panel, CMS |
| **NocoDB** | 🐋 Heavy | Docker | ✅✅ Excellent | Kanban, grid, forms, team | Airtable replacement |

---

## Recommendation

For **DevOps / infrastructure use cases** (monitoring data, config DBs, logs), **Datasette** is the best fit:

1. Point it at any existing SQLite file → instant UI + API
2. Plugins for auth, geospatial, charts, publish
3. Works well alongside tools like Beszel, Dozzle, and Dex

For a **full admin panel** over SQLite data → **Directus**.
For a **quick internal dashboard** from SQL queries → **SQLPage**.
