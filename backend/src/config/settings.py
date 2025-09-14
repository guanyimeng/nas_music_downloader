import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/nas_music_downloader"
    )
    
    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-please-20250914")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # NAS output settings
    output_directory: str = os.getenv("OUTPUT_DIRECTORY", "/app/downloads")
    
    # App settings
    app_name: str = "NAS Music Downloader"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    class Config:
        env_file = ".env"


settings = Settings()
