from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DownloadRequest(BaseModel):
    url: str

class DownloadResponse(BaseModel):
    id: int
    url: str
    title: Optional[str] = None
    artist: Optional[str] = None
    status: str
    file_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True # Enable ORM mode

class DownloadHistoryResponse(BaseModel):
    downloads: List[DownloadResponse]
    total: int
    page: int
    per_page: int