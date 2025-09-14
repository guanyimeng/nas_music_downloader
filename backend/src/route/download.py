from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os
import logging

from ..model import get_db, User, DownloadHistory
from ..schema.download import DownloadRequest, DownloadResponse, DownloadHistoryResponse
from ..auth import get_current_active_user
from ..service.yt_music import MusicDownloader
from ..service.audit import log_download_action
from ..config.settings import settings

logger = logging.getLogger(__name__)

download_router = APIRouter(prefix="/api", tags=["downloads"])

@download_router.post("/download", response_model=DownloadResponse)
async def download_music(
    request: DownloadRequest,
    http_request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download music from URL"""
    url = request.url
    
    # Create download history record
    download_record = DownloadHistory(
        user_id=current_user.id,
        url=url,
        status="pending"
    )
    db.add(download_record)
    db.commit()
    db.refresh(download_record)
    
    # Log download start
    await log_download_action(
        db=db,
        user_id=current_user.id,
        action="download_started",
        url=url,
        details={"download_id": download_record.id},
        ip_address=http_request.client.host,
        user_agent=http_request.headers.get("user-agent"),
        status="success"
    )
    
    try:
        # Update status to downloading
        download_record.status = "downloading"
        download_record.download_started_at = datetime.utcnow()
        db.commit()
        
        # Download music using MusicDownloader
        downloader = MusicDownloader(output_dir=settings.output_directory)
        download_result = downloader.download_audio(url=url)
        
        if download_result.success and download_result.file_path:
            # Update download record with success
            download_record.status = "completed"
            download_record.title = download_result.title
            download_record.file_path = download_result.file_path
            download_record.artist = download_result.artist
            download_record.duration = download_result.duration
            download_record.download_completed_at = datetime.utcnow()
            
            # Get file size if file exists
            if os.path.exists(download_result.file_path):
                download_record.file_size = os.path.getsize(download_result.file_path)
            
            db.commit()
            
            await log_download_action(
                db=db,
                user_id=current_user.id,
                action="download_completed",
                url=url,
                details={
                    "download_id": download_record.id,
                    "file_path": download_result.file_path,
                    "title": download_record.title
                },
                ip_address=http_request.client.host,
                user_agent=http_request.headers.get("user-agent"),
                status="success"
            )
            
            logger.info(f"Download completed for user {current_user.username}: {url}")
        else:
            # Update download record with failure
            download_record.status = "failed"
            download_record.error_message = "Download failed - no output file"
            download_record.download_completed_at = datetime.utcnow()
            db.commit()
            
            await log_download_action(
                db=db,
                user_id=current_user.id,
                action="download_failed",
                url=url,
                details={"download_id": download_record.id, "error": "No output file"},
                ip_address=http_request.client.host,
                user_agent=http_request.headers.get("user-agent"),
                status="failed"
            )
            
            logger.warning(f"Download failed for user {current_user.username}: {url}")

        return download_record
            
    except Exception as e:
        # Update download record with error
        download_record.status = "failed"
        download_record.error_message = str(e)
        download_record.download_completed_at = datetime.utcnow()
        db.commit()
        
        await log_download_action(
            db=db,
            user_id=current_user.id,
            action="download_failed",
            url=url,
            details={"download_id": download_record.id, "error": str(e)},
            ip_address=http_request.client.host,
            user_agent=http_request.headers.get("user-agent"),
            status="failed"
        )
        
        logger.error(f"Download error for user {current_user.username}: {url} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Download failed: {str(e)}"
        )


@download_router.get("/downloads", response_model=DownloadHistoryResponse)
async def get_download_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's download history with pagination"""
    offset = (page - 1) * per_page
    
    downloads = db.query(DownloadHistory).filter(
        DownloadHistory.user_id == current_user.id
    ).order_by(DownloadHistory.created_at.desc()).offset(offset).limit(per_page).all()
    
    total = db.query(DownloadHistory).filter(
        DownloadHistory.user_id == current_user.id
    ).count()
    
    return DownloadHistoryResponse(
        downloads=downloads,
        total=total,
        page=page,
        per_page=per_page
    )


@download_router.get("/downloads/{download_id}", response_model=DownloadResponse)
async def get_download_by_id(
    download_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific download by ID"""
    download = db.query(DownloadHistory).filter(
        DownloadHistory.id == download_id,
        DownloadHistory.user_id == current_user.id
    ).first()
    
    if not download:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Download not found"
        )
    
    return download