# download_history.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base


class DownloadHistory(Base):
    __tablename__ = "download_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String(2048), nullable=False)
    title = Column(String(500), nullable=True)
    artist = Column(String(200), nullable=True)
    duration = Column(Float, nullable=True)  # Duration in seconds
    file_size = Column(Integer, nullable=True)  # File size in bytes
    file_path = Column(String(1000), nullable=True)  # Path to downloaded file
    status = Column(String(50), nullable=False)  # "pending", "downloading", "completed", "failed"
    error_message = Column(Text, nullable=True)
    download_started_at = Column(DateTime(timezone=True), nullable=True)
    download_completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", backref="download_history")
