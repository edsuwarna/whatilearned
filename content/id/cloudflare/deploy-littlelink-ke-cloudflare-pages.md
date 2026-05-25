---
title: "Deploy LittleLink ke Cloudflare Pages"
description: "Panduan langkah demi langkah deploy LittleLink (alternatif Linktree open-source) di Cloudflare Pages"
category: "Cloudflare"
tags: [cloudflare, pages, littlelink, hosting, static-site]
---

# Deploy LittleLink ke Cloudflare Pages

[LittleLink](https://github.com/sethcottle/littlelink) adalah alternatif open-source untuk Linktree/Bio.link. Ringan, single-page HTML, dengan 100+ gaya tombol branded.

Cloudflare Pages cocok banget — gratis, cepat, dan auto-deploy dari GitHub.

## Prasyarat

- Akun [GitHub](https://github.com)
- Akun [Cloudflare](https://dash.cloudflare.com) (tier gratis cukup)
- Fork/clone LittleLink di GitHub

## Langkah 1: Fork LittleLink

1. Buka [github.com/sethcottle/littlelink](https://github.com/sethcottle/littlelink)
2. Klik **Fork** → **Create fork**
3. Tunggu proses fork selesai

> Bisa juga clone lokal, kustomisasi, lalu push ke repo sendiri.

## Langkah 2: Kustomisasi Halaman

Edit file berikut di repo lo:

| File | Yang diubah |
|------|------------|
| `index.html` | Nama, bio, link, tombol |
| `css/brands.css` | Tambah style tombol kustom |
| `images/` | Ganti avatar dan favicon |

** perubahan penting di `index.html`:**
- **Line ~70**: Ganti `<h1>` dengan nama lo
- **Line ~73**: Ganti teks bio
- **Lines ~105+**: Ganti link tombol dengan URL lo
- **Line ~35**: Update path favicon

Contoh struktur tombol:

```html
<a class="button button-github" href="https://github.com/usernamekamu" target="_blank" rel="noopener" role="button">
  <img class="icon" src="images/icons/github.svg" alt="">GitHub
</a><br>
```

## Langkah 3: Push ke GitHub

```bash
git add .
git commit -m "Kustomisasi LittleLink"
git push origin main
```

## Langkah 4: Deploy di Cloudflare Pages

1. Buka [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Klik **Workers & Pages** di sidebar kiri
3. Klik **Create** → **Pages** → **Connect to Git**
4. Authorize Cloudflare akses ke repo GitHub lo
5. Pilih repo LittleLink lo
6. Di **Set up builds and deployment**:
   - **Project name**: `littlelink` (atau sesuai keinginan)
   - **Production branch**: `main`
   - **Framework preset**: **None** (plain HTML/CSS)
   - **Build command**: kosongkan
   - **Build output directory**: kosongkan (atau `/`)
7. Klik **Save and Deploy**

> ⚡ Selesai! Cloudflare akan deploy site lo dalam ~30 detik.

## Langkah 5: Pasang Custom Domain (Opsional)

1. Di project Pages lo, buka **Custom domains**
2. Klik **Set up a custom domain**
3. Masukkan domain lo (contoh: `link.domainkamu.com`)
4. Cloudflare otomatis nambahin DNS record

## Auto-Deploy Setiap Push

Setiap kali push ke branch `main`, Cloudflare Pages otomatis rebuild dan redeploy. Ga perlu langkah manual.

## Nambah Warna Tombol Kustom

Tambah style baru di `css/brands.css`:

```css
/* Contoh tombol kustom */
.button.button-kustom {
  color: #ffffff;
  background-color: #warnalo;
}
.button.button-kustom:hover,
.button.button-kustom:focus {
  filter: brightness(110%);
}
```

Lalu pake di `index.html`:

```html
<a class="button button-kustom" href="https://example.com" ...>Tombol Saya</a><br>
```

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Halaman ga update setelah push | Tunggu ~1 menit, cek log build Cloudflare Pages |
| 404 setelah deploy | Pastikan `index.html` ada di root repo |
| Gambar ga muncul | Pake relative path kayak `images/icon.svg` |
| Custom domain ga jalan | Pastikan DNS terarah ke Cloudflare |

## Referensi

- [LittleLink GitHub](https://github.com/sethcottle/littlelink)
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
