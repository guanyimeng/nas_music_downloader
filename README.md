# NAS Music Downloader

A full-stack music downloader optimized for NAS systems. It features a FastAPI backend with PostgreSQL, JWT authentication, audit logging, and a React (Vite) web UI for initiating downloads and monitoring status. Docker Compose is provided to run everything together.

## Features

- 🎵 Download audio via yt-dlp (YouTube and many others)
- 🔐 JWT-based auth (register, login, logout, /auth/me)
- 🧾 Audit logging of user actions
- 🗃️ PostgreSQL persistence (users, downloads, token blacklist)
- 🖥️ Web UI (React + Vite) for URL input, start download, live status, and history
- 🐳 Docker Compose: one command brings up Postgres, backend API, and frontend
- 📁 NAS-friendly: mount your NAS path as the downloads directory

## Architecture

- Backend (FastAPI) on port 8000
- Frontend (Nginx serving React build) on port 3000
- Nginx proxies `/auth` and `/api` to the backend
- Postgres as the database

```
[Browser] ──> http://localhost:3000  (Nginx)
    ├── /auth → http://backend:8000/auth (proxy)
    └── /api  → http://backend:8000/api  (proxy)

[Backend] FastAPI (8000) ↔ PostgreSQL
Downloads saved to: /app/downloads (host-mounted)
```

## Quick Start (Docker Compose)

Prerequisites:
- Docker Desktop (or Docker Engine) running
- Optional: set a host path for downloads

1) Clone the repo
```
git clone <repository-url>
cd nas_music_downloader
```

2) Configure environment
```
cp .env.example .env
```
- To have downloads saved to a specific host path, set `DOWNLOADS_HOST_PATH` in `.env`. Examples:
  - Windows: `DOWNLOADS_HOST_PATH=E:/Downloads`
  - Linux:  `DOWNLOADS_HOST_PATH=/home/you/Music`
  - macOS:  `DOWNLOADS_HOST_PATH=/Users/you/Music`

If not set, Compose will mount a local `./downloads` folder into the backend container at `/app/downloads`.

3) Bring up the stack
```
docker compose up -d --build
```

4) Access the app
- Frontend: http://localhost:3000
- Backend Swagger: http://localhost:8000/docs
- Healthcheck: http://localhost:8000/health

5) Use the UI
- Register a new account, then login
- Paste a URL to start a download
- Watch status update (pending/downloading/completed/failed) in Recent Activity or check the History page

## Local Development (Optional)

You can develop backend and frontend locally without Docker if preferred.

### Backend (FastAPI)
Prerequisites: Python 3.11+, Poetry

```
cd backend
poetry install
# Ensure a Postgres instance is running and DATABASE_URL is set
poetry run uvicorn src.music_downloader.app:app --reload
```
- API at http://localhost:8000
- Swagger at http://localhost:8000/docs

### Frontend (React + Vite)
Prerequisites: Node.js 18+ (20+ recommended), npm

```
cd frontend
npm install
npm run dev
```
- Dev server: http://localhost:5173
- Dev proxy routes `/auth` and `/api` to http://localhost:8000 (see `vite.config.ts`)
- CORS in backend allows http://localhost:5173 and http://localhost:3000

## Environment Variables

Backend (see `.env.example`):
- `DATABASE_URL` — e.g. `postgresql://postgres:password@postgres:5432/nas_music_downloader`
- `SECRET_KEY` — JWT signing key (change in production)
- `ALGORITHM` — default HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES` — e.g. 30
- `OUTPUT_DIRECTORY` — default `/app/downloads`
- `DEBUG` — `"true"`/`"false"`

Compose-only:
- `DOWNLOADS_HOST_PATH` — host path to mount for downloads (optional; defaults to `./downloads`)

Frontend build-time (optional):
- `VITE_API_BASE_URL` — override the axios baseURL. By default, the app uses relative paths and relies on dev proxy (Vite) or Nginx proxy (Docker).

## Repository Structure

```
nas_music_downloader/
├── backend/                     # FastAPI app, models, routes, services
│   ├── Dockerfile
│   └── src/music_downloader/...
├── frontend/                    # React SPA (Vite) and Nginx config
│   ├── Dockerfile
│   ├── nginx.conf
│   └── src/...
├── docker-compose.yml           # Postgres + Backend + Frontend
├── .env.example                 # Example env vars (copy to .env)
├── init-db.sql                  # Optional DB init script
└── README.md                    # This file
```

## NAS Volume Mount Examples

If you prefer to edit `docker-compose.yml` manually rather than using `DOWNLOADS_HOST_PATH`, mount your NAS path to `/app/downloads`:

- Synology
  ```yaml
  volumes:
    - /volume1/music:/app/downloads
  ```
- QNAP
  ```yaml
  volumes:
    - /share/music:/app/downloads
  ```
- TrueNAS
  ```yaml
  volumes:
    - /mnt/pool/music:/app/downloads
  ```
- Ugreen
  ```yaml
  volumes:
    - /media/usb/music:/app/downloads
  ```

## Troubleshooting

- Docker compose fails to pull images or connect: ensure Docker Desktop is running.
- “npm not recognized” during local dev: install Node.js from https://nodejs.org and make sure npm is on PATH.
- 401 Unauthorized: login again; tokens from old SECRET_KEY values become invalid.
- CORS in dev: Vite proxies to the backend; ensure backend is on http://localhost:8000.
- Paths on Windows: use forward slashes (e.g., `E:/Downloads`) in `.env` for `DOWNLOADS_HOST_PATH`.

## License

MIT License. See `LICENSE` if present or include your chosen license terms.
