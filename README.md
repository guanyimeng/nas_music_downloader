# NAS Music Downloader

A FastAPI-based music downloader service optimized for NAS systems, featuring PostgreSQL integration, user authentication, and detailed audit logging.

## Features

- 🎵 **Music Download**: Download music from YouTube and other platforms using yt-dlp.
- 🔐 **User Authentication**: Secure JWT-based authentication with user registration and login.
- 📊 **Download History**: Track complete download history with metadata.
- 🔍 **Audit Logging**: Maintain a comprehensive audit trail of all user actions.
- 🐳 **Docker Ready**: Easily deploy using Docker Compose.
- 💾 **PostgreSQL**: Reliable database backend with relationships and indexing.
- 📁 **NAS Integration**: Save downloaded files directly to your NAS via volume mounting.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your NAS.
- A NAS system that supports Docker.

### Deployment Steps

1. **Clone the repository to your NAS:**
   ```bash
   git clone <repository-url>
   cd nas_music_downloader
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit the .env file to customize your settings
   ```

3. **Update `docker-compose.yml`:**
   Modify the volume mount path to point to your NAS music directory:
   ```yaml
   volumes:
     - /path/to/your/nas/music:/app/downloads  # Replace with your NAS path
   ```

4. **Start the services:**
   ```bash
   docker-compose up -d
   ```

5. **Access the API:**
   - Backend API: `http://your-nas-ip:8000`
   - API Documentation (Swagger UI): `http://your-nas-ip:8000/docs`

## NAS Volume Mount Examples

Adjust the volume path in `docker-compose.yml` according to your NAS type:

- **Synology NAS**
  ```yaml
  volumes:
    - /volume1/music:/app/downloads
  ```

- **QNAP NAS**
  ```yaml
  volumes:
    - /share/music:/app/downloads
  ```

- **TrueNAS**
  ```yaml
  volumes:
    - /mnt/pool/music:/app/downloads
  ```

- **Ugreen NAS**
  ```yaml
  volumes:
    - /media/usb/music:/app/downloads
  ```

## License

This project is licensed under the MIT License.
