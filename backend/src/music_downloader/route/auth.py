from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from ..model import get_db, User, AuditLog, TokenBlacklist
from ..schema.auth import UserCreate, UserResponse, UserLogin, Token
from ..auth import verify_password, get_password_hash, create_access_token, get_current_user
from ..service.audit import log_user_action

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        await log_user_action(
            db=db,
            user_id=None,
            action="register_failed",
            details=f"User already exists: {user_data.username}",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            status="failed"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    await log_user_action(
        db=db,
        user_id=db_user.id,
        action="register_success",
        details=f"New user registered: {user_data.username}",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        status="success"
    )
    
    logger.info(f"New user registered: {user_data.username}")
    return db_user


@auth_router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Login user and return JWT token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        await log_user_action(
            db=db,
            user_id=user.id if user else None,
            action="login_failed",
            details=f"Failed login attempt for: {form_data.username}",
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            status="failed"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        await log_user_action(
            db=db,
            user_id=user.id,
            action="login_failed",
            details=f"Inactive user login attempt: {form_data.username}",
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            status="failed"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    await log_user_action(
        db=db,
        user_id=user.id,
        action="login_success",
        details=f"User logged in: {user.username}",
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None,
        status="success"
    )
    
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
async def logout_user(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user (mainly for audit logging)"""
    # assume current_user_token is attached by your dependency
    jti = current_user.token_data.jti
    exp = current_user.token_data.exp

    # create a blacklist entry
    db.add(TokenBlacklist(
        jti=jti,
        user_id=current_user.id,
        expires_at=datetime.fromtimestamp(exp)
    ))
    db.commit()

    await log_user_action(
        db=db,
        user_id=current_user.id,
        action="logout",
        details=f"User logged out: {current_user.username}",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        status="success"
    )
    
    logger.info(f"User logged out: {current_user.username}")
    return {"message": "Successfully logged out"}


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
