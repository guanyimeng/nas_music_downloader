# Dockerfile for FastAPI backend using Poetry

# --- Build stage ---

FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies (no ffmpeg needed in build stage)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only dependency files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# --- Main image ---
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (runtime only)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy backend source code
COPY src/ ./src/
COPY data/ ./data/
COPY docker/ ./docker/

# Expose port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
