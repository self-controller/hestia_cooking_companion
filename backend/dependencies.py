import redis
from typing import Optional
from fastapi import HTTPException, Cookie, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from config import REDIS_URL, DEV_MODE
from database import User, get_db
from models.schemas import User_out
from helper import hash_password

# Global Redis client instance
redis_client: redis.Redis | None = None

def get_redis() -> redis.Redis:
    """
    Dependency function to get Redis client.
    Note: redis_client must be initialized before use (typically in lifespan).
    """
    assert redis_client is not None, "Redis not initialized"
    return redis_client

def set_redis_client(client: redis.Redis | None) -> None:
    """
    Set the global Redis client. Used by lifespan in main.py.
    """
    global redis_client
    redis_client = client

def _get_production_user(
    SID: Optional[str] = Cookie(None),
    r: redis.Redis = Depends(get_redis),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency function to get the current authenticated user.
    Raises HTTPException if not authenticated.
    """
    # Confirm SID cookie exists
    if not SID:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Validate SID exists in Redis
    user_id_str = r.get(SID)
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    # Convert user ID from string to int (Redis stores as string)
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid session data")
    
    # Query database for user by ID
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def _get_dev_user(db: Session) -> User:
    """Internal: Get or create a dev user for development mode."""
    # Try to get user with ID 1
    user = db.scalar(select(User).where(User.id == 1))
    if user:
        return user
    
    # Try to get any user
    user = db.scalar(select(User).limit(1))
    if user:
        return user
    
    # Create a dev user if none exists
    dev_user = User(
        username="dev_user",
        email="dev@example.com",
        hash_password=hash_password("dev_password")
    )
    db.add(dev_user)
    db.commit()
    db.refresh(dev_user)
    return dev_user

def get_current_user(
    SID: Optional[str] = Cookie(None),
    r: redis.Redis = Depends(get_redis),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency function to get the current authenticated user.
    Automatically handles dev mode vs production mode.
    """
    if DEV_MODE:
        return _get_dev_user(db)
    else:
        return _get_production_user(SID, r, db)