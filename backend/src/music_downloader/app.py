
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import logging
import os

from .config.settings import settings
from .model import init_db
from .route.auth import auth_router
from .route.download import download_router
from .route.monitor import monitor_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app():
    version = "0.1.0"
    app = FastAPI(
        title=settings.app_name, 
        version=version, 
        description="Backend API for downloading music for NAS storage with authentication and audit logging"
    )

    # CORS middleware
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    # Ensure output directory exists
    os.makedirs(settings.output_directory, exist_ok=True)
    logger.info(f"Output directory ready: {settings.output_directory}")

    # Include routers
    app.include_router(auth_router)
    app.include_router(download_router)
    app.include_router(monitor_router)

    @app.get("/")
    async def root():
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": version,
            "status": "running"
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.app_name}

    return app

app = create_app()

if __name__ == "__main__":
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
    server = uvicorn.Server(config)
    server.run()