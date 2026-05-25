# Keamanan Supply Chain Open Source — Panduan Pencegahan

> Pelajaran dari serangan supply chain Trivy (GHSA-69fq-xp46-6x23, Maret 2026)
> dan praktik terbaik untuk mengamankan project open source.

## 1. 🔐 Keamanan GitHub / Repository

**Branch protection** — lindungi branch `main`:
- Tidak boleh force push
- Wajib ada review Pull Request sebelum merge
- Wajib status checks lolos sebelum merge

**Signed commits** — aktifkan GPG atau SSH signing:
- Git mendukung commit signing via GPG atau SSH keys
- GitHub kasih badge ✅ di commit yang terverifikasi
- Mencegah impersonasi — tidak ada yang bisa push atas nama lo

```bash
# Konfigurasi GPG signing
git config --global commit.gpgsign true
git config --global user.signingkey <KEY_ID>
```

**CODEOWNERS** — terapkan review untuk file kritis:
```github
# .github/CODEOWNERS
Dockerfile          @edsuwarna
.github/workflows/* @edsuwarna
requirements.txt    @edsuwarna
```

**2FA WAJIB** — two-factor authentication untuk semua maintainer:
- Insiden Trivy disebabkan oleh kredensial yang compromised tanpa 2FA
- GitHub sekarang mewajibkan 2FA untuk publish ke GitHub Packages / releases

## 2. 🔄 Keamanan CI/CD

**Pin semua GitHub Actions pakai commit SHA** — jangan pakai version tag:

```yaml
# ❌ BERBAHAYA — tag bisa di-force push!
uses: aquasecurity/trivy-action@v0.35.0

# ✅ AMAN — pin by SHA
uses: aquasecurity/trivy-action@8a3177a...

# ✅ AMAN dengan Dependabot auto-update
uses: aquasecurity/trivy-action@8a3177a...  # Dependabot akan update SHA
```

**Aturan:**
- Jangan pernah pakai `@latest` atau `@main` di workflow production
- Pakai Dependabot untuk update action SHA otomatis
- Simpan secret di **GitHub Secrets** atau pakai **OIDC** — jangan di YAML workflow
- Validasi checksum artifact sebelum dipakai

## 3. 📦 Manajemen Dependensi

**Lock dependencies dengan hashes** untuk cegah tampering:

```bash
# Python — pip-tools dengan hashes
pip-compile --generate-hashes requirements.in -o requirements.txt
```

**Scan dependensi otomatis:**
- **Dependabot** — auto PR untuk dependensi yang punya CVE
- **Renovate** — alternatif yang lebih configurable
- **pip-audit** — scan Python dependencies terhadap PyPI advisory DB

**Software Bill of Materials (SBOM):**
- Generate SBOM untuk setiap release pakai Syft atau Trivy
- Lampirkan SPDX/CycloneDX JSON ke GitHub releases
- Pengguna bisa verifikasi tidak ada dependensi mencurigakan yang ditambahkan

```bash
# Generate SBOM dengan Syft
syft packages your-image:latest -o spdx-json > sbom.spdx.json
```

## 4. 📤 Keamanan Release

**Immutable releases:**
- GitHub Releases sekarang immutable secara default — diaktifkan Maret 2026
- Mencegah overwrite asset release setelah dipublikasi
- Pastikan fitur ini sudah aktif di repo settings

**Signing release artifacts:**
```bash
# GPG sign release assets
gpg --armor --detach-sign my-release.tar.gz

# Cosign (container signing)
cosign sign --key cosign.key ghcr.io/username/image:tag
```

**Framework SLSA:**
- Target minimal **SLSA Level 1** — build provenance
- Generate attestasi yang tidak bisa dipalsukan bahwa artifact berasal dari CI lo
- SLSA Level 3+ memberikan jaminan integritas dependensi

**Jangan pernah reuse version tags:**
- Attacker Trivy force-push 76 dari 77 version tags di trivy-action
- Kalau harus pakai tags, buat immutable via GitHub settings
- Pipeline production harus pakai **release IDs** atau **content hashes**, bukan tags

## 5. 👥 Kontrol Akses

Insiden Trivy dimulai dari **kredensial maintainer yang compromised**.

**Praktik terbaik:**
```
✅ Maintainer minimal — 1-2 admin, sisanya sebagai contributor
✅ Fine-grained Personal Access Tokens (bukan classic tokens)
✅ Scoping token — berikan izin minimum yang diperlukan
✅ Rotasi token — expire dan perbarui secara berkala
✅ Tidak boleh ada shared credentials — setiap maintainer pakai akun sendiri
✅ Audit token aktif setiap bulan
```

**Spesifik GitHub:**
- Pakai **GitHub Apps** daripada PATs untuk automation
- Fine-grained PATs bisa di-scope ke repo dan permission tertentu
- Classic tokens punya akses luas — hindari

## 6. 🕵️ Pre-commit & Deteksi Secret

Cegah data sensitif masuk ke repository:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

**Tools untuk dijalankan berkala:**
- **TruffleHog** — scan riwayat git untuk secret yang terekspos
- **gitleaks** — alternatif secret scanning yang ringan
- **git secret** — enkripsi file sensitif di repo

```bash
# Scan seluruh riwayat git
trufflehog filesystem --directory=. .
```

## 7. 📋 Checklist Project Open Source Baru

Pakai ini setiap kali bikin project open source baru:

- [ ] **Branch protection** di `main` (no force push, require reviews)
- [ ] **GPG/SSH signing** untuk semua commit
- [ ] **GitHub Actions pin by SHA** (bukan tags)
- [ ] **Dependabot / Renovate** aktif untuk update dependensi
- [ ] **SBOM** di-generate untuk setiap release
- [ ] **2FA** aktif untuk semua maintainer
- [ ] **Pre-commit hooks** untuk deteksi secret
- [ ] **CODEOWNERS** untuk file sensitif
- [ ] **Fine-grained PATs** (jangan classic tokens)
- [ ] **Dependency scanning** di CI (pip-audit, Trivy, atau Grype)
- [ ] **Immutable releases** sudah dikonfirmasi di repo settings
- [ ] **Security policy** terdokumentasi (`SECURITY.md`) untuk laporan celah keamanan

---

*Terakhir diperbarui: Mei 2026*
*Terinspirasi dari insiden supply chain Trivy (GHSA-69fq-xp46-6x23)*
