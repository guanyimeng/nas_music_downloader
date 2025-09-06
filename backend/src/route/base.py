from fastapi import APIRouter

from .monitor import monitor_router
from .download import download_router

api_router = APIRouter()
api_router.include_router(monitor_router, prefix="/monitor", tags=["monitor"])
api_router.include_router(download_router, prefix="/download", tags=["download"])