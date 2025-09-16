FROM python:3.11-slim

WORKDIR /app

# Install system dependencies first
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libpq5 \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files including src
COPY poetry.lock pyproject.toml README.md ./
COPY src/ ./src/
COPY alembic.ini ./
COPY alembic ./alembic/

# Install dependencies globally (not in a virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# Create non-root user and ensure /app and downloads are owned by app
RUN useradd -m -u 1000 -s /usr/sbin/nologin app \
    && mkdir -p /app/downloads \
    && chown -R app:app /app \
    && chmod -R 755 /app

# Switch to non-root user
USER app

# Volume for downloads
VOLUME ["/app/downloads"]

# Environment variables
ENV PYTHONPATH=/app/src
ENV OUTPUT_DIRECTORY=/app/downloads
ENV DEBUG=false

# Lightweight healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose FastAPI port
EXPOSE 8000

# Run DB migrations then start FastAPI
CMD ["sh", "-c", "(alembic upgrade head || (alembic stamp 0001_initial && alembic upgrade head)) && python -m music_downloader.app"]
