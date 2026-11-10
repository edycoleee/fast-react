# Fast React + FastAPI Boilerplate

Boilerplate reusable untuk aplikasi lain dengan stack:
- Frontend: React + Vite + SWC
- Backend: FastAPI + SQLAlchemy 2.x + Alembic
- Database: PostgreSQL
- Infra lokal: Docker Compose + Nginx

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
   - `uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000`
3. Frontend (terminal lain):
   - `cd frontend`
   - `npm install`
   - `npm run dev -- --host 0.0.0.0 --port 5173`

## Quick Start (Docker Compose)

1. `cp .env.example .env`
2. `docker compose up --build`
3. Buka:
   - App via Nginx: `http://localhost:8080`
   - API docs: `http://localhost:8080/docs`
   - Health: `http://localhost:8080/health`

## Quality Gate Minimum

- `docker compose up` sukses
- `/health` return OK
- `/health/db` return OK saat PostgreSQL aktif
- `alembic upgrade head` sukses
- frontend build/dev bisa jalan

## Reuse ke Proyek Lain

1. Clone boilerplate.
2. Ganti nilai di `.env`.
3. Tambah modul domain baru di `backend/app/modules/<domain>`.
4. Tambah feature di `frontend/src/features/<feature>`.
5. Buat migration baru:
   - `alembic -c backend/alembic.ini revision --autogenerate -m "add <domain>"`
   - `alembic -c backend/alembic.ini upgrade head`

