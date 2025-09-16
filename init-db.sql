-- Initialize database with default admin user
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist (handled by POSTGRES_DB env var)

-- Connect to the nas_music_downloader database
\c nas_music_downloader;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Schema is managed by Alembic migrations (applied on container start).
-- Use this file mainly for initial data or custom configurations that aren't suited for Alembic.

-- You can add initial admin user creation here if needed
-- INSERT INTO users (username, email, hashed_password, is_admin, is_active) 
-- VALUES ('admin', 'admin@example.com', '$2b$12$...', true, true);

-- Add any other initialization queries here
