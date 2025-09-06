# download_history.py


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from .db import engine

Base = declarative_base()

class DownloadHistory(Base):
    __tablename__ = "download_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
