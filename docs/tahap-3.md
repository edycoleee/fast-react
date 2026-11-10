# Tahapan 3 — Urutan Implementasi yang Disarankan

Tujuan tahap ini adalah memastikan implementasi berjalan efisien, minim rework, dan mudah divalidasi.

## Urutan Eksekusi

1. **Fondasi repository & environment**
   - Rapikan struktur folder `frontend/`, `backend/`, `deploy/`, `docs/`.
   - Siapkan `.env.example`, `.env.development`, dan variabel inti.

2. **Backend core terlebih dahulu (minimum viable backend)**
   - Jalankan FastAPI dasar.
   - Tambahkan endpoint `GET /health`.
   - Siapkan koneksi database yang bisa diverifikasi.

3. **Database dan migrasi**
   - Setup PostgreSQL.
   - Setup SQLAlchemy + Alembic.
   - Buat migrasi baseline dan verifikasi `upgrade/downgrade`.

4. **Frontend core**
   - Setup React + Vite + routing dasar.
   - Buat layout/public-protected page skeleton.
   - Terapkan design system awal + `data-testid` pada elemen penting.

5. **Integrasi frontend ↔ backend**
   - Siapkan API client (Axios).
   - Uji alur request dasar dari frontend ke backend.
   - Tangani loading/error state secara konsisten.

6. **Deploy stack lokal (integrasi penuh)**
   - Jalankan semua service via Docker Compose: frontend, backend, postgres, nginx.
   - Verifikasi alur akses lewat Nginx.

7. **Hardening & validasi akhir tahap**
   - Jalankan test minimum (backend + frontend).
   - Pastikan checklist quality gate dari Tahap 1 dan 2 terpenuhi.
   - Dokumentasikan perintah jalan dan troubleshooting dasar.

## Kesimpulan

Prioritas implementasi: **backend core dulu**, lalu **frontend**, kemudian **deploy/infrastruktur integrasi**.  
Dengan urutan ini, risiko integrasi biasanya lebih rendah dan proses debugging lebih cepat.

