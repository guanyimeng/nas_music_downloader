from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .db import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    jti         = Column(String(255), nullable=False, unique=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    revoked_at  = Column(DateTime(timezone=True), server_default=func.now())
    expires_at  = Column(DateTime(timezone=True), nullable=False)

    user        = relationship("User", back_populates="revoked_tokens")