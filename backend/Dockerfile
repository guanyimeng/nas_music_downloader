# Dockerfile for NAS Music Downloader Backend with PostgreSQL support

# --- Build stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and poetry-plugin-export
RUN pip install --no-cache-dir poetry poetry-plugin-export

# Copy only dependency files
COPY poetry.lock pyproject.toml README.md ./
COPY src/ ./src/

# Export requirements.txt for production install
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# --- Main image ---
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt from builder and install with pip
# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Create directories and set permissions
RUN mkdir -p /app/downloads && chown -R app:app /app

# Copy backend source code
COPY --chown=app:app src/ ./src/

# Switch to non-root user
USER app

# Create volume mount point for NAS storage
VOLUME ["/app/downloads"]

# Environment variables
ENV PYTHONPATH=/app
ENV OUTPUT_DIRECTORY=/app/downloads

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Expose port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
