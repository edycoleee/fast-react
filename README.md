# Fast React + FastAPI Boilerplate

Boilerplate reusable untuk aplikasi lain dengan stack:
- Frontend: React + Vite + SWC
- Backend: FastAPI + SQLAlchemy 2.x + Alembic
- Database: PostgreSQL
- Infra lokal: Docker Compose + Nginx
- Theme default: palet profesional hijau-teal
- Tersedia toggle Light/Dark mode (persist di localStorage browser)

## Struktur

- `frontend/` aplikasi React
- `backend/` aplikasi FastAPI modular
- `deploy/` konfigurasi Nginx
- `docs/` referensi tahapan dan tujuan

## Quick Start (local, tanpa Docker)

1. Salin env:
   - `cp .env.example .env`
2. Backend:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -e .[dev]`
   - `alembic -c backend/alembic.ini upgrade head`
   - `python scripts/seed.py`
   - `uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000`
3. Frontend (terminal lain):
   - `cd frontend`
   - `npm install`
   - `npm run dev -- --host 0.0.0.0 --port 5173`

## Quick Start (Docker Compose)

1. `cp .env.example .env`
2. `docker compose up --build`
3. Seed admin:
   - `docker compose exec backend python scripts/seed.py`
4. Buka:
   - App via Nginx: `http://localhost:8080`
   - API docs: `http://localhost:8080/docs`
   - Health: `http://localhost:8080/health`

> Jika Anda mengubah `NGINX_PORT` di `.env`, sesuaikan URL di atas.

## Default Login (hasil seed)

- Email: `admin@example.com`
- Password: `admin123`

Ganti credential default lewat variabel:
- `SEED_ADMIN_EMAIL`
- `SEED_ADMIN_USERNAME`
- `SEED_ADMIN_PASSWORD`

## Auth API Ringkas

- `POST /api/v1/auth/login`
  - body: `{ "email": "...", "password": "..." }`
  - response: bearer token + profile user + permissions
- `GET /api/v1/auth/me`
  - header: `Authorization: Bearer <token>`
- `GET /api/v1/access/summary`
  - butuh permission `access.read`

## IAM API (Users / Roles / Permissions)

Semua endpoint IAM butuh permission `iam.manage`.

- Permissions
  - `GET /api/v1/iam/permissions?page=1&page_size=10&q=keyword`
  - `POST /api/v1/iam/permissions`
  - `PATCH /api/v1/iam/permissions/{permission_id}`
  - `DELETE /api/v1/iam/permissions/{permission_id}`
- Roles
  - `GET /api/v1/iam/roles?page=1&page_size=10&q=keyword`
  - `POST /api/v1/iam/roles`
  - `PATCH /api/v1/iam/roles/{role_id}`
  - `DELETE /api/v1/iam/roles/{role_id}`
- Users
  - `GET /api/v1/iam/users?page=1&page_size=10&q=keyword&is_active=true|false`
  - `POST /api/v1/iam/users`
  - `PATCH /api/v1/iam/users/{user_id}`
  - `DELETE /api/v1/iam/users/{user_id}`

## UI Admin Access

- Login sebagai admin, lalu buka:
  - `/dashboard` → tombol **Go to Access Management**
  - `/admin/access` untuk kelola permission, role, dan user.

## Quality Gate Minimum

- `docker compose up` sukses
- `/health` return OK
- `/health/db` return OK saat PostgreSQL aktif
- `alembic upgrade head` sukses
- `python scripts/seed.py` sukses
- frontend build/dev bisa jalan
- backend test lulus: `pytest backend/tests -q`

## Reuse ke Proyek Lain

1. Clone boilerplate.
2. Ganti nilai di `.env`.
3. Tambah modul domain baru di `backend/app/modules/<domain>`.
4. Tambah feature di `frontend/src/features/<feature>`.
5. Buat migration baru:
   - `alembic -c backend/alembic.ini revision --autogenerate -m "add <domain>"`
   - `alembic -c backend/alembic.ini upgrade head`
