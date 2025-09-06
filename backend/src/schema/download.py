from pydantic import BaseModel
from typing import List

class DownloadRequest(BaseModel):
    url: str

class DownloadResponse(BaseModel):
    status: str
    history: List[str]