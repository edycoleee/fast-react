# Tahapan 2 — Fondasi Data Layer dan FastAPI Core

Tujuan tahap ini adalah memastikan backend punya pondasi data yang kuat, terukur, dan siap scale untuk modul-modul berikutnya.

## 1) Finalisasi desain database awal

Fokus dulu pada entitas foundation (bukan modul klinis detail):

- `users`
- `roles`
- `permissions`
- tabel relasi user-role dan role-permission
- field audit dasar (`created_at`, `updated_at`, `created_by`, `updated_by` bila diperlukan)

Prinsip:
- Gunakan primary key konsisten (UUID/int sesuai keputusan global).
- Definisikan unique constraint penting (mis. username/email).
- Definisikan index untuk kolom yang sering query/filter.

## 2) Implementasi SQLAlchemy model per domain

- Pisahkan model per fitur/domain (jangan monolitik satu file).
- Gunakan `Base` terpusat dan pola import yang mencegah circular dependency.
- Definisikan relasi (`relationship`) dengan jelas dan konsisten naming-nya.
- Siapkan mixin umum bila perlu (timestamp/audit/soft delete).

## 3) Setup Alembic secara rapi

- Konfigurasi Alembic agar membaca metadata SQLAlchemy yang benar.
- Buat migrasi awal dari model foundation.
- Review hasil autogenerate (jangan langsung trust penuh).
- Pastikan migrasi bisa:
  - `upgrade head`
  - `downgrade` ke versi sebelumnya (minimal 1 langkah)

## 4) Bangun FastAPI application core

- Bentuk struktur app inti:
  - `main.py` (bootstrap)
  - `core/config`
  - `core/database`
  - `api/router registry`
- Daftarkan router per modul, bukan semua endpoint di satu tempat.
- Siapkan dependency injection untuk DB session.
- Tambahkan handler error global dasar (validasi & internal error) dengan format response konsisten.

## 5) Tambahkan health checks yang siap dipakai operasional

Minimal endpoint:

- `GET /health` → status app
- `GET /health/db` → status koneksi database

Kriteria:
- Response ringan, cepat, dan mudah dipakai Docker/K8s health probing.
- Jangan expose informasi sensitif di response health check.

## 6) Siapkan baseline testing backend

Minimal untuk tahap ini:

- Unit test untuk service/repository penting foundation.
- API test untuk endpoint health check.
- Integration test koneksi DB + migrasi dasar (gunakan PostgreSQL test DB, bukan SQLite).

## 7) Quality gate Tahap 2

Checklist selesai:

- [ ] Semua model foundation terbentuk dan tervalidasi
- [ ] Migrasi awal berhasil di environment lokal
- [ ] FastAPI app start tanpa error
- [ ] Endpoint `/health` dan `/health/db` lolos test
- [ ] Test dasar data layer berjalan stabil dan deterministic
- [ ] Dokumentasi command migrasi ditulis di README/dokumen teknis

## 8) Output wajib di akhir Tahap 2

1. Struktur data layer yang rapi dan modular  
2. Migrasi Alembic awal yang dapat diulang dengan aman  
3. FastAPI core app siap jadi fondasi fitur autentikasi (Tahap 3)  
4. Baseline test backend untuk mencegah regresi awal  

---

Jika semua checklist lolos, lanjut ke **Tahap 3**: autentikasi, manajemen user, role, dan permission dengan keamanan yang benar.
