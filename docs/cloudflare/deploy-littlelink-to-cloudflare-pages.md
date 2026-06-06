---
title: "Deploy LittleLink to Cloudflare Pages"
description: "Step-by-step guide to deploy LittleLink (open-source Linktree alternative) on Cloudflare Pages"
category: "Cloudflare"
tags: [cloudflare, pages, littlelink, hosting, static-site]
---

# Deploy LittleLink to Cloudflare Pages


## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Fork LittleLink](#step-1-fork-littlelink)
- [Step 2: Customize Your Page](#step-2-customize-your-page)
- [Step 3: Push to GitHub](#step-3-push-to-github)
- [Step 4: Deploy on Cloudflare Pages](#step-4-deploy-on-cloudflare-pages)
- [Step 5: Set Custom Domain (Optional)](#step-5-set-custom-domain-optional)
- [Auto-Deploy on Every Push](#auto-deploy-on-every-push)
- [Adding Custom Button Colors](#adding-custom-button-colors)
- [Troubleshooting](#troubleshooting)
- [References](#references)

[LittleLink](https://github.com/sethcottle/littlelink) is an open-source alternative to Linktree/Bio.link. It's a lightweight, single-page HTML site with 100+ branded button styles.

Cloudflare Pages is a perfect fit — it's free, fast, and automatically deploys from your GitHub repo.

## Prerequisites

- A [GitHub](https://github.com) account
- A [Cloudflare](https://dash.cloudflare.com) account (free tier works)
- LittleLink fork/clone in your GitHub

## Step 1: Fork LittleLink

1. Go to [github.com/sethcottle/littlelink](https://github.com/sethcottle/littlelink)
2. Click **Fork** → **Create fork**
3. Wait for the fork to complete

> Alternatively, clone it locally, customize, then push to your own repo.

## Step 2: Customize Your Page

Edit these files in your repo:

| File | What to change |
|------|---------------|
| `index.html` | Your name, bio, links, buttons |
| `css/brands.css` | Add custom button styles if needed |
| `images/` | Replace avatar and favicon |

**Key changes in `index.html`:**
- **Line ~70**: Change `<h1>` to your name
- **Line ~73**: Change bio text
- **Lines ~105+**: Replace button links with your own URLs
- **Line ~35**: Update favicon path

Example button structure:

```html
<a class="button button-github" href="https://github.com/yourusername" target="_blank" rel="noopener" role="button">
  <img class="icon" src="images/icons/github.svg" alt="">GitHub
</a><br>
```

## Step 3: Push to GitHub

```bash
git add .
git commit -m "Customize LittleLink"
git push origin main
```

## Step 4: Deploy on Cloudflare Pages

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click **Workers & Pages** in the left sidebar
3. Click **Create** → **Pages** → **Connect to Git**
4. Authorize Cloudflare to access your GitHub repos
5. Select your LittleLink repo
6. In **Set up builds and deployment**:
   - **Project name**: `littlelink` (or your preference)
   - **Production branch**: `main`
   - **Framework preset**: **None** (it's plain HTML/CSS)
   - **Build command**: leave empty
   - **Build output directory**: `.` (root directory — where `index.html` lives)
7. Click **Save and Deploy**

> ⚡ That's it! Cloudflare will deploy your site in ~30 seconds.

## Step 5: Set Custom Domain (Optional)

1. In your Pages project, go to **Custom domains**
2. Click **Set up a custom domain**
3. Enter your domain (e.g., `link.yourdomain.com`)
4. Cloudflare automatically adds the DNS record

## Auto-Deploy on Every Push

Every time you push to the `main` branch, Cloudflare Pages automatically rebuilds and redeploys. No manual steps needed.

## Adding Custom Button Colors

Add new button styles in `css/brands.css`:

```css
/* Custom button example */
.button.button-custom {
  color: #ffffff;
  background-color: #yourcolor;
}
.button.button-custom:hover,
.button.button-custom:focus {
  filter: brightness(110%);
}
```

Then use it in `index.html`:

```html
<a class="button button-custom" href="https://example.com" ...>My Button</a><br>
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Page not updating after push | Wait ~1 min, check Cloudflare Pages build log |
| 404 on deploy | Make sure `index.html` is in the repo root |
| Images not showing | Use relative paths like `images/icon.svg` |
| Custom domain not working | Ensure DNS is pointed to Cloudflare |

## References

- [LittleLink GitHub](https://github.com/sethcottle/littlelink)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
