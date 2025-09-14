from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import logging
from types import SimpleNamespace
from jose import JWTError, ExpiredSignatureError


from ..model import get_db, User, TokenBlacklist
from .security import verify_token

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    try:
        payload = verify_token(token)
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=401, detail="Malformed token")
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    # Check blacklist
    if db.query(TokenBlacklist).filter_by(jti=jti).first():
        raise HTTPException(status_code=401, detail="Token has been revoked")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
     # Attach token data to the return value so logout can see it
    user.token_data = SimpleNamespace(jti=jti, exp=payload.get("exp"))
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    return current_user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current user if they are admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
