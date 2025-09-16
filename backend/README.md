# NAS Music Downloader Backend

FastAPI-based backend that exposes REST APIs for user authentication, music download management, and system monitoring. Uses PostgreSQL for persistence and integrates with a React frontend. Designed to run standalone for development or together with the frontend and database via Docker Compose.

## Overview

- Framework: FastAPI (Starlette, Pydantic v2)
- Database: PostgreSQL (SQLAlchemy)
- Auth: JWT (access tokens), password hashing with bcrypt/passlib
- Downloader: yt-dlp
- Docs: Auto-generated Swagger at `/docs`
- Healthcheck: `/health`

## Service Ports

- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

When running with the root Docker Compose, the frontend is served on http://localhost:3000 and proxies `/auth` and `/api` to the backend service.

## API Endpoints

### Authentication
- `POST /auth/register` — Register a new user (JSON body)
- `POST /auth/login` — Authenticate and obtain a JWT token
  - Expects `application/x-www-form-urlencoded` body (OAuth2PasswordRequestForm: `username`, `password`)
- `POST /auth/logout` — Logout user and blacklist token
- `GET /auth/me` — Retrieve current authenticated user information

### Downloads
- `POST /api/download` — Initiate a music download from a given URL (JSON `{ "url": "..." }`)
- `GET /api/downloads` — Retrieve paginated download history for the authenticated user (`page`, `per_page`)
- `GET /api/downloads/{id}` — Retrieve details of a specific download by ID

### System
- `GET /health` — Health check endpoint
- `GET /` — Basic service info and status

## Authentication Details

- Login uses `application/x-www-form-urlencoded` (OAuth2PasswordRequestForm) with fields `username` and `password`.
- On success, returns `{ "access_token": "...", "token_type": "bearer" }`.
- For authenticated endpoints, send `Authorization: Bearer <access_token>` header.
- Logout blacklists the current token (tracked in DB), and tokens naturally expire per configuration.

## CORS

The backend enables CORS for local development and Docker frontend:
- Allowed origins include `http://localhost:5173` (Vite dev) and `http://localhost:3000` (Docker/Nginx).
- Methods and headers are unrestricted (`*`) and credentials are allowed.

If deploying behind another domain, update CORS origins in `src/music_downloader/app.py` accordingly.

## Environment Variables

Common settings (see `.env.example` in repo root for examples):

- `DATABASE_URL` — PostgreSQL connection string.
  - Example (local dev): `postgresql://postgres:password@localhost:5432/nas_music_downloader`
  - Example (in Docker Compose): `postgresql://postgres:password@postgres:5432/nas_music_downloader`
- `SECRET_KEY` — JWT signing key (change in production).
- `ALGORITHM` — JWT algorithm (default HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES` — Token lifetime in minutes (e.g. 30).
- `OUTPUT_DIRECTORY` — Directory path where downloaded files are written (default `/app/downloads`).
- `DEBUG` — `true`/`false` to control Uvicorn reload and log level.

Compose-only (set in the root `.env` file):
- `DOWNLOADS_HOST_PATH` — Host path to mount for downloads (e.g., `E:/Downloads`, `/home/you/Music`). If not set, defaults to `./downloads` in the repository root.

## Running Options

### 1) Docker Compose (Recommended)

From the repository root (`nas_music_downloader/`):

1. Copy env file and configure as needed:
   ```bash
   cp .env.example .env
   # Optional: set DOWNLOADS_HOST_PATH in .env to mount a host/NAS directory
   ```

2. Build and start all services (Postgres + Backend + Frontend):
   ```bash
   docker compose up -d --build
   ```

3. Open:
   - Frontend: http://localhost:3000
   - Backend Swagger: http://localhost:8000/docs
   - Health: http://localhost:8000/health

Downloads will be stored inside the backend container at `/app/downloads`, which maps to the host path configured via `DOWNLOADS_HOST_PATH` (or `./downloads` by default).

### 2) Local Development (without Compose)

Prerequisites:
- Python 3.11+
- Poetry
- A running PostgreSQL instance

1. Install dependencies:
   ```bash
   cd backend
   poetry install
   ```

2. Start PostgreSQL (example via Docker):
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_DB=nas_music_downloader \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 postgres:15-alpine
   ```

3. Set `DATABASE_URL` (and any other vars) in your environment and run the app:
   ```bash
   # Example DATABASE_URL for local dockerized Postgres
   # export DATABASE_URL=postgresql://postgres:password@localhost:5432/nas_music_downloader

   poetry run uvicorn src.music_downloader.app:app --reload
   ```

4. Visit http://localhost:8000/docs

If you also want the React dev server running, open a second terminal and follow the frontend README (`frontend/README.md`) to run Vite at http://localhost:5173. The Vite dev proxy routes `/auth` and `/api` to http://localhost:8000.

## Downloads and Storage

- The backend writes downloaded files to `OUTPUT_DIRECTORY` (default `/app/downloads`).
- In Docker Compose, the host path is mounted into the backend container at that location. Set `DOWNLOADS_HOST_PATH` in the root `.env` to control the host-mount path.
- Ensure the mounted directory is writable by the container user.

## Database Models (Summary)

### User
- Credentials, profile info, admin flag, activity tracking, last login

### DownloadHistory
- Each download request with metadata: URL, title/artist (when available), `status` (`pending`, `downloading`, `completed`, `failed`), file path, timestamps

### TokenBlacklist
- Blacklisted JWT tokens for logout handling with expiration cleanup

### AuditLog
- All user actions: IP address, user agent, action context for security and compliance

## Monitoring and Logging

- Health endpoint: `GET /health`
- Structured logging with configurable levels
- Container healthchecks (curl) in Docker Compose
- Audit trail for authentication and download actions

## Project Structure (Backend)

```
backend/
├── Dockerfile
├── pyproject.toml
├── src/
│   └── music_downloader/
│       ├── auth/           # Authentication helpers and dependencies
│       ├── config/         # Settings management
│       ├── model/          # SQLAlchemy models and DB session
│       ├── route/          # API routers (auth, download, monitor)
│       ├── schema/         # Pydantic schemas
│       ├── service/        # Business logic (e.g., yt-dlp integration)
│       └── app.py          # FastAPI application factory / entry
└── test/                   # (if present) tests
```

## Security Features

- JWT token-based authentication
- Token blacklisting on logout
- Password hashing via bcrypt (passlib)
- Runs as non-root user in container
- Input validation via Pydantic schemas
- Comprehensive audit logging

## Troubleshooting

- 401 Unauthorized — ensure the `Authorization: Bearer <token>` header is present. Re-login if the token was invalidated.
- DB connection issues — verify `DATABASE_URL` and Postgres availability (`pg_isready` or Docker logs).
- CORS errors in dev — use the Vite dev proxy (frontend) or add your origin to CORS origins in `app.py`.
- Permission errors writing downloads — ensure the host mount path is writable by the container user.
- yt-dlp failures — check logs for errors from external sites; network and format availability can vary.

## Token Blacklist Cleanup

Expired tokens can be periodically removed to keep the blacklist clean:
```sql
DELETE FROM token_blacklist WHERE expires_at < now();
```

## License

MIT (or your preferred license). See the project root for details.
