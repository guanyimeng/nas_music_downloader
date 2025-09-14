# NAS Music Downloader Backend

## Overview
This backend service provides a RESTful API for user authentication, music download management, and system monitoring. It is built with FastAPI and uses PostgreSQL for data persistence.

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate user and obtain JWT token
- `POST /auth/logout` - Logout user and blacklist token
- `GET /auth/me` - Retrieve current authenticated user information

### Downloads
- `POST /api/download` - Initiate a music download from a given URL
- `GET /api/downloads` - Retrieve paginated download history for the user
- `GET /api/downloads/{id}` - Retrieve details of a specific download by ID

### System
- `GET /health` - Health check endpoint to verify service status
- `GET /` - Basic service information and status

## Environment Variables

| Variable           | Description                      | Default                                               |
|--------------------|--------------------------------|-------------------------------------------------------|
| `DATABASE_URL`      | PostgreSQL connection string   | `postgresql://postgres:password@localhost:5432/nas_music_downloader` |
| `SECRET_KEY`        | JWT secret key for token signing | `your-secret-key-change-in-production`               |
| `OUTPUT_DIRECTORY`  | Directory path for downloaded files | `/app/downloads`                                    |
| `DEBUG`            | Enable debug mode (true/false) | `false`                                              |

## Database Models

### User
- Stores user credentials and profile information
- Supports admin role for privileged access
- Tracks user activity and status

### DownloadHistory
- Records metadata for each download request
- Stores file paths, sizes, and download status (pending, in-progress, completed, failed)
- Supports pagination for history retrieval

### TokenBlacklist
- Maintains a list of invalidated JWT tokens for logout handling
- Tokens expire naturally and are periodically cleaned up

### AuditLog
- Logs all user actions for security and compliance
- Captures IP address, user agent, and detailed action context

## Development Setup

### Prerequisites
- Python 3.10+
- Poetry for dependency management
- Docker (for PostgreSQL container)

### Local Development

1. Install dependencies:
   ```bash
   cd backend
   poetry install
   ```

2. Start PostgreSQL database:
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_DB=nas_music_downloader \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 postgres:15-alpine
   ```

3. Run the FastAPI application with auto-reload:
   ```bash
   cd backend
   poetry run uvicorn src.music_downloader.app:app --reload
   ```

## Project Structure

```
nas_music_downloader/
├── backend/
│   ├── src/
│   │   ├── music_downloader/
│   │   │   ├── auth/          # Authentication logic and routes
│   │   │   ├── config/        # Configuration and settings
│   │   │   ├── model/         # Database models
│   │   │   ├── route/         # API route handlers
│   │   │   ├── schema/        # Pydantic schemas for request/response validation
│   │   │   ├── service/       # Business logic and external integrations
│   │   │   └── app.py         # FastAPI application entrypoint
│   ├── Dockerfile
│   └── pyproject.toml
├── docker-compose.yml
└── README.md
```

## Security Features

- JWT token-based authentication with token blacklisting on logout
- Password hashing using bcrypt for secure credential storage
- Runs as non-root user inside Docker container
- Input validation and sanitization via Pydantic schemas
- Comprehensive audit logging for all user actions

## Monitoring and Logging

- Health check endpoint available at `/health`
- Structured logging with configurable log levels
- Docker health checks included in container setup
- Audit trail maintained for compliance and troubleshooting

## User Registration

- Register new users via the API endpoint: `POST /auth/register`

## Token Blacklist Cleanup

- Expired tokens are removed periodically to keep the blacklist clean:
  ```sql
  DELETE FROM token_blacklist WHERE expires_at < now();
