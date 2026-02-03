# NAS Music Downloader

A full‑stack music downloader optimized for NAS systems. FastAPI backend (PostgreSQL, JWT, audit logging) and a React (Vite) web UI for initiating downloads and monitoring status. Docker Compose is provided to run everything together.

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
Downloads saved to: /app/downloads (host‑mounted)
```

## Quick Start (Docker Compose)
Prerequisites:
- Docker Desktop (or Docker Engine) running

1) Clone the repo
```
git clone <repository-url>
cd nas_music_downloader
```

2) Create and configure environment file
- Copy `.env.example` to `.env`:
  ```
  cp .env.example .env
  ```
- Edit `.env` to set your NAS storage path in `NAS_STORAGE_PATH` (e.g., `/home/youruser/Music:/app/downloads:rw` for Linux). This mounts your host directory to the container's downloads folder.

3) Bring up the stack
```
docker compose up -d --build
```

4) Access the app
- Frontend: http://localhost:3000
- Backend Swagger: http://localhost:8000/docs
- Healthcheck: http://localhost:8000/health

5) Use the UI
- Register, then login
- Paste a URL to start a download
- Watch status in Recent Activity or the History page

## Local Development (Optional)
You can develop backend and frontend locally without Docker if preferred.

### Backend (FastAPI)
Prerequisites: Python 3.11+, Poetry, a running PostgreSQL
```
cd backend
poetry install
# Ensure DATABASE_URL is set (e.g., postgresql://postgres:password@localhost:5432/nas_music_downloader)
poetry run uvicorn src.music_downloader.app:app --reload
```
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

### Frontend (React + Vite)
Prerequisites: Node.js 18+ (20+ recommended), npm
```
cd frontend
npm install
npm run dev
```
- Dev server: http://localhost:5173
- Dev proxy routes `/auth` and `/api` to http://localhost:8000 (see `vite.config.ts`)

## Configuration
Create a `.env` file from `.env.example` and adjust the values as needed. Backend environment variables:

- `NAS_STORAGE_PATH` — Host path to mount for downloads, e.g., `/home/youruser/Music:/app/downloads:rw` (Linux) or `E:/app/downloads:/app/downloads` (Windows)
- `DATABASE_URL` — PostgreSQL connection string, e.g., `postgresql://postgres:password@postgres:5432/nas_music_downloader`
- `POSTGRES_DB` — Database name, default `nas_music_downloader`
- `POSTGRES_USER` — Database user, default `postgres`
- `POSTGRES_PASSWORD` — Database password, default `password`
- `PORTS_MAPPING` — Port mapping for Postgres, e.g., `54322:5432`
- `SECRET_KEY` — JWT signing key (change in production, use `openssl rand -hex 32`)
- `ALGORITHM` — JWT algorithm, default `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` — Token expiration time in minutes, default `30`
- `OUTPUT_DIRECTORY` — Directory inside container for downloads, default `/app/downloads`
- `DEBUG` — Enable debug mode, `"true"` or `"false"` (default `false`)

Frontend build‑time (optional):
- `VITE_API_BASE_URL` — Override Axios baseURL. By default, the app uses relative paths and relies on the proxy (Vite in dev, Nginx in Docker).

## NAS/Host Volume Mapping Examples
Set `NAS_STORAGE_PATH` in your `.env` file to map your host/NAS path to `/app/downloads` in the container:

- Linux: `NAS_STORAGE_PATH="/home/youruser/Music:/app/downloads:rw"`
- Windows: `NAS_STORAGE_PATH="E:/app/downloads:/app/downloads"`
- Synology: `NAS_STORAGE_PATH="/volume1/music:/app/downloads"`
- TrueNAS: `NAS_STORAGE_PATH="/mnt/pool/music:/app/downloads"`

Ensure the mounted directory is writable by the container user.

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
├── .env.example                 # Example env vars
├── init-db.sql                  # Optional DB init script
└── README.md                    # This file
```

## Updating the Application

### Update yt-dlp
To update yt-dlp to the latest version:

```bash
cd backend
chmod +x update_yt-dlp.sh
./update_yt-dlp.sh
```

This script updates yt-dlp via Poetry, commits the changes to `poetry.lock`, and pushes to the remote repository.

### Rebuild backend
To update the application on your NAS/server:

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart containers
```bash
docker compose down
docker compose up -d --build backend
```

## License
MIT License. See `LICENSE` if present or include your chosen license terms.
