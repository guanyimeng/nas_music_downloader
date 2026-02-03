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

2) Configure the downloads mount
- Open `docker-compose.yml` and set the host path you want to use for downloads on the `backend` service volumes:
  ```yaml
  backend:
    volumes:
      - "/home/youruser/Music:/app/downloads:rw"   # Linux example
      # - "E:/app/downloads:/app/downloads"        # Windows example
  ```
- Replace `/home/youruser/Music` (or `E:/app/downloads`) with your NAS/host directory. The right‑hand side must remain `/app/downloads`.

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
Backend environment variables (see `.env.example`):
- DATABASE_URL — e.g. `postgresql://postgres:password@postgres:5432/nas_music_downloader`
- SECRET_KEY — JWT signing key (change in production)
- ALGORITHM — default HS256
- ACCESS_TOKEN_EXPIRE_MINUTES — e.g. 30
- OUTPUT_DIRECTORY — default `/app/downloads`
- DEBUG — `"true"`/`"false"`

Frontend build‑time (optional):
- VITE_API_BASE_URL — override Axios baseURL. By default, the app uses relative paths and relies on the proxy (Vite in dev, Nginx in Docker).

## NAS/Host Volume Mapping Examples
Map your host/NAS path to `/app/downloads` in `docker-compose.yml`:

- Linux
  ```yaml
  volumes:
    - /home/youruser/Music:/app/downloads:rw
  ```
- Windows
  ```yaml
  volumes:
    - "E:/app/downloads:/app/downloads"
  ```
- Synology
  ```yaml
  volumes:
    - /volume1/music:/app/downloads
  ```
- TrueNAS
  ```yaml
  volumes:
    - /mnt/pool/music:/app/downloads
  ```

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

### Rebuild on Server
To update the application on your NAS/server:

```bash
# SSH into your server
ssh user@your-server-ip

# Navigate to the project directory
cd /path/to/nas_music_downloader

# Pull latest changes
git pull origin main

# Rebuild and restart containers
docker compose down
docker compose up -d --build
```

### Update yt-dlp
To update yt-dlp to the latest version:

```bash
cd backend
./update_yt-dlp.sh
```

This script updates yt-dlp via Poetry, commits the changes to `poetry.lock`, and pushes to the remote repository.

## License
MIT License. See `LICENSE` if present or include your chosen license terms.
