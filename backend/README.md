# NAS Music Downloader — Backend (FastAPI)

Lightweight REST API for authentication, download management, and monitoring. Uses PostgreSQL and writes files to `/app/downloads` (host-mapped via docker-compose).

Run the full stack from the repository root:
- `docker compose up -d --build`
- API: http://localhost:8000 (docs at `/docs`)
- Frontend: http://localhost:3000

For development details and configuration (env vars, volume mapping), see the root README.
