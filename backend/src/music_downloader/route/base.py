from fastapi import APIRouter

from .monitor import monitor_router
from .auth import auth_router
from .download import download_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(monitor_router, prefix="/monitor", tags=["monitor"])
api_router.include_router(download_router, prefix="/download", tags=["download"])