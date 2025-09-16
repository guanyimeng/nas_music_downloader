# NAS Music Downloader — Backend (FastAPI)

Lightweight REST API for authentication, download management, and monitoring. Uses PostgreSQL and writes files to `/app/downloads` (host-mapped via docker-compose).

Run the full stack from the repository root:
- `docker compose up -d --build`
- API: http://localhost:8000 (docs at `/docs`)
- Frontend: http://localhost:3000

For development details and configuration (env vars, volume mapping), see the root README.

## Database migrations (Alembic)

This service uses Alembic for schema migrations. On container start, migrations are applied automatically before the API starts:
- The backend Dockerfile runs: `alembic upgrade head && python -m music_downloader.app`

Configuration:
- DB URL comes from `DATABASE_URL` (see `src/music_downloader/config/settings.py`).
- Alembic config lives in `/app/alembic.ini` with scripts in `/app/alembic/`.
- Target metadata is `music_downloader.model.Base.metadata` (autogenerate supported).

Local development (without Docker):
1) Ensure dependencies are installed:
   - `cd nas_music_downloader/backend`
   - `poetry install`
2) Set your database URL (or use `.env`):
   - `set DATABASE_URL=postgresql://postgres:password@localhost:5432/nas_music_downloader` (Windows CMD)
   - `export DATABASE_URL=postgresql://postgres:password@localhost:5432/nas_music_downloader` (bash/zsh)
3) Create a new migration (autogenerate from SQLAlchemy models):
   - `poetry run alembic revision --autogenerate -m "describe change"`
4) Apply migrations:
   - `poetry run alembic upgrade head`

With Docker Compose:
- Migrations are applied automatically when you run `docker compose up -d --build`.
- To run Alembic manually inside the container:
  - `docker compose exec backend alembic revision --autogenerate -m "describe change"`
  - `docker compose exec backend alembic upgrade head`

Note:
- The previous `Base.metadata.create_all()` initialization has been removed from app startup in favor of Alembic migrations. Ensure any schema changes go through a migration.
