# Tahapan 1 — Menyiapkan Boilerplate SIMRS yang Reusable

Tujuan tahap ini adalah membangun fondasi proyek yang bisa dipakai ulang untuk banyak aplikasi/modul di masa depan.

## 1) Tetapkan batasan dan standar inti

- Kunci stack utama: **Frontend (React + Vite + SWC)**, **Backend (FastAPI + SQLAlchemy + Alembic)**, **DB (PostgreSQL)**, **Infra (Docker Compose + Nginx)**.
- Tetapkan prinsip arsitektur: **modular monolith**, pemisahan per domain/fitur, dan tidak ada logika menumpuk di satu file besar.
- Definisikan aturan naming, struktur folder, style code, dan aturan import agar konsisten di semua aplikasi turunan.

## 2) Bentuk struktur repository yang reusable

Buat struktur yang jelas sejak awal:

- `frontend/` → semua kebutuhan UI
- `backend/` → API, service, repository, model, schema
- `deploy/` → docker, nginx, env template
- `docs/` → dokumentasi arsitektur, cara pakai, SOP pengembangan

Gunakan pola folder berbasis fitur/domain agar saat menambah modul baru tidak perlu refactor besar.

## 3) Siapkan fondasi backend

- Buat aplikasi FastAPI dasar dengan pemisahan:
  - router
  - schema
  - service
  - repository
  - model
- Siapkan koneksi PostgreSQL berbasis environment variable.
- Pasang SQLAlchemy 2.x + Alembic sebagai fondasi migrasi.
- Tambahkan endpoint health check (`/health`) untuk verifikasi container dan monitoring.

## 4) Siapkan fondasi frontend

- Inisialisasi React + Vite + SWC (JavaScript).
- Pasang routing dasar (public vs protected area).
- Siapkan layer:
  - `pages/`
  - `features/`
  - `shared/`
  - `api/`
  - `stores/`
  - `providers/`
- Siapkan API client (Axios), state async (TanStack Query), dan state global ringan (Zustand/Context sesuai kebutuhan).
- Siapkan design system frontend agar UI profesional dan seragam:
  - Definisikan **semantic color tokens** (bukan warna acak per halaman): `primary`, `secondary`, `success`, `warning`, `danger`, `muted`, `background`, `foreground`.
  - Simpan token warna terpusat di Tailwind theme + CSS variables agar mudah diubah global.
  - Siapkan mode **light/dark** sejak awal.
- Buat komponen UI reusable sebagai fondasi tampilan:
  - `Button`, `Input`, `Select`, `Card`, `Badge`, `Alert`, `Table`, `Modal/Dialog`.
  - Setiap komponen punya varian standar (contoh tombol: `primary`, `secondary`, `outline`, `ghost`, `danger`).
  - Hindari styling langsung berulang di halaman; gunakan komponen bersama.
- Tetapkan standar `data-testid` untuk elemen penting agar testing stabil:
  - halaman: `page-<nama-halaman>` (contoh: `page-login`)
  - form: `form-<nama-form>` (contoh: `form-login`)
  - input: `input-<nama-field>` (contoh: `input-email`)
  - tombol: `btn-<aksi>` (contoh: `btn-submit-login`)
  - tabel/list: `table-<nama-entity>`, `row-<nama-entity>-<id>`
  - state penting: `loading-*`, `error-*`, `empty-*`
- Gunakan `data-testid` pada komponen interaktif/krusial saja (hindari menambah ke semua elemen agar markup tetap bersih).

## 5) Siapkan infrastruktur lokal dan deployment dasar

- Buat `docker-compose` untuk:
  - frontend
  - backend
  - postgres
  - nginx
- Konfigurasi Nginx sebagai reverse proxy untuk frontend/backend.
- Pastikan ada pemisahan konfigurasi environment:
  - `.env.example`
  - `.env.development`
  - `.env.production`

## 6) Pastikan boilerplate siap dipakai ulang

- Buat template konfigurasi yang mudah diganti per aplikasi (nama app, port, domain, kredensial DB, dsb.).
- Hindari hardcode nilai lingkungan/deployment.
- Dokumentasikan “cara cloning boilerplate untuk proyek baru” langkah demi langkah.

## 7) Buat quality gate minimum sebelum lanjut ke tahap berikutnya

Minimal checklist selesai:

- [ ] `docker compose up` berhasil
- [ ] PostgreSQL sehat
- [ ] Backend FastAPI bisa diakses lewat Nginx
- [ ] Frontend build sukses
- [ ] Color system semantik (Tailwind theme + CSS variables) sudah ditetapkan
- [ ] Komponen UI foundation reusable sudah tersedia dan dipakai lintas halaman
- [ ] Konvensi `data-testid` React sudah diterapkan di komponen/halaman fondasi
- [ ] Struktur folder mengikuti standar modular
- [ ] `.env.example` lengkap
- [ ] README berisi cara setup dari nol

## 8) Output yang harus jadi di akhir Tahap 1

1. Struktur proyek final yang konsisten dan modular  
2. Frontend & backend skeleton siap dikembangkan  
3. Docker + Nginx + PostgreSQL siap jalan  
4. Dokumentasi setup dan aturan pengembangan dasar  

---

Jika semua poin di atas sudah terpenuhi, proyek siap masuk **Tahap 2** (model database, SQLAlchemy detail, Alembic migration, dan health checks lanjutan).