from fastapi import APIRouter
from typing import List

from .service.yt_music import yt_downloader
from .service.yt_history import load_history, save_history
from .schema import DownloadRequest, DownloadResponse

download_router = APIRouter()

@download_router.get("/")
async def root():
    return {"status": "ok", "message": "Backend is running"}

@download_router.post("/download", response_model=DownloadResponse)
async def download_music(request: DownloadRequest):
    url = request.url
    try:
        # Download music using yt_downloader
        downloader = yt_downloader()
        output_file = downloader.download_youtube_as_mp3(url)
        if output_file:
            status = downloader.output_musicname + downloader.download_status + " ✅"
        else:
            status = downloader.output_musicname + "Download failed ❌"

        # Add to history (keep only last 10)
        download_history: List[str] = load_history()
        download_history.append(status)
        if len(download_history) > 10:
            download_history.pop(0)

        save_history(download_history)

        return DownloadResponse(status=status, history=download_history)

            
    except Exception as e:
        status = f"Error: {e}"
        return DownloadResponse(status=status, history=download_history)