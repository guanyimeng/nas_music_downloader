# NAS Music Downloader

A FastAPI-based music downloader service designed to run on NAS systems with PostgreSQL database, user authentication, and comprehensive audit logging.

## Features

- 🎵 **Music Download**: Download music from YouTube and other platforms using yt-dlp
- 🔐 **User Authentication**: JWT-based authentication system with user registration/login
- 📊 **Download History**: Complete download history with metadata tracking
- 🔍 **Audit Logging**: Comprehensive audit trail for all user actions
- 🐳 **Docker Ready**: Containerized deployment with Docker Compose
- 💾 **PostgreSQL**: Robust database with proper relationships and indexing
- 📁 **NAS Integration**: Direct file output to NAS filesystem via volume mounting

## Quick Start

### Prerequisites
- Docker and Docker Compose
- NAS system with Docker support

### Deployment on NAS

1. **Clone the repository to your NAS**:
   ```bash
   git clone <repository-url>
   cd nas_music_downloader
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Update docker-compose.yml**:
   - Change the volume mount path to your NAS music directory:
   ```yaml
   volumes:
     - /volume1/music:/app/downloads  # Adjust this path for your NAS
   ```

4. **Start the services**:
   ```bash
   docker-compose up -d
   ```

5. **Access the API**:
   - Backend API: `http://your-nas-ip:8000`
   - API Documentation: `http://your-nas-ip:8000/docs`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user info

### Downloads
- `POST /api/download` - Download music from URL
- `GET /api/downloads` - Get download history (paginated)
- `GET /api/downloads/{id}` - Get specific download

### System
- `GET /health` - Health check
- `GET /` - Service info

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/nas_music_downloader` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `OUTPUT_DIRECTORY` | Download output directory | `/app/downloads` |
| `DEBUG` | Enable debug mode | `false` |

## Database Schema

### Users
- User management with authentication
- Admin role support
- Activity tracking

### Download History
- Complete download metadata
- File paths and sizes
- Status tracking (pending, downloading, completed, failed)

### Audit Logs
- All user actions logged
- IP address and user agent tracking
- Detailed action context

## Development

### Local Development Setup

1. **Install dependencies**:
   ```bash
   cd backend
   poetry install
   ```

2. **Start PostgreSQL**:
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_DB=nas_music_downloader \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 postgres:15-alpine
   ```

3. **Run the application**:
   ```bash
   cd backend
   poetry run uvicorn src.app:app --reload
   ```

### Project Structure
```
nas_music_downloader/
├── backend/
│   ├── src/
│   │   ├── auth/          # Authentication system
│   │   ├── config/        # Configuration settings
│   │   ├── model/         # Database models
│   │   ├── route/         # API routes
│   │   ├── schema/        # Pydantic schemas
│   │   ├── service/       # Business logic
│   │   └── app.py         # FastAPI application
│   ├── Dockerfile
│   └── pyproject.toml
├── docker-compose.yml
└── README.md
```

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Non-root container execution
- Input validation and sanitization
- Comprehensive audit logging

## NAS-Specific Configuration

### Synology NAS
```yaml
volumes:
  - /volume1/music:/app/downloads
```

### QNAP NAS
```yaml
volumes:
  - /share/music:/app/downloads
```

### TrueNAS
```yaml
volumes:
  - /mnt/pool/music:/app/downloads
```

## Monitoring and Logs

- Health check endpoint at `/health`
- Structured logging with configurable levels
- Docker health checks included
- Audit trail for compliance

## License

MIT License