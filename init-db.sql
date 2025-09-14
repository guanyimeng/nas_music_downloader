-- Initialize database with default admin user
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist (handled by POSTGRES_DB env var)

-- Connect to the nas_music_downloader database
\c nas_music_downloader;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created automatically by SQLAlchemy when the app starts
-- This file is mainly for any initial data or custom configurations

-- You can add initial admin user creation here if needed
-- INSERT INTO users (username, email, hashed_password, is_admin, is_active) 
-- VALUES ('admin', 'admin@example.com', '$2b$12$...', true, true);

-- Add any other initialization queries here

-- Create a user from api:
-- Use /auth/register/

-- Cleanup expired blacklist entries.
-- Tokens will naturally expire; you can periodically delete old rows:
DELETE FROM token_blacklist WHERE expires_at < now();