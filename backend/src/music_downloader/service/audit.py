from sqlalchemy.orm import Session
from typing import Optional
from ..model import AuditLog
import json
import logging

logger = logging.getLogger(__name__)


async def log_user_action(
    db: Session,
    user_id: Optional[int],
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status: str = "success"
) -> AuditLog:
    """Log user action to audit table"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
    except Exception as e:
        logger.error(f"Failed to log audit action: {e}")
        db.rollback()
        raise


async def log_download_action(
    db: Session,
    user_id: int,
    action: str,
    url: str,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status: str = "success"
) -> AuditLog:
    """Log download-specific action"""
    details_str = json.dumps(details) if details else None
    
    return await log_user_action(
        db=db,
        user_id=user_id,
        action=action,
        resource_type="download",
        resource_id=url,
        details=details_str,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status
    )
