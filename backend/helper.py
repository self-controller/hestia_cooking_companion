import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import User
from fastapi import Response
from config import DEV_MODE
import uuid

# Generate a Version 4 UUID
def get_uuid():
    my_uuid = uuid.uuid4()
    return str(my_uuid)

def hash_password(password):
    """Hashes a password with a randomly generated salt using bcrypt."""
    # Encode the password to bytes, as bcrypt works with bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a random salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Hash the password with the generated salt
    hashed_password = hashed_password.decode('utf-8')
    
    return hashed_password

def get_user_by_email(email: str, db: Session):
    query = select(User).where(User.email == email)
    user = db.scalar(query)
    return user

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def set_auth_cookie(response: Response, session_id: str) -> None:
    """Set authentication cookie with appropriate settings for dev/production."""
    response.set_cookie(
        key="SID",
        value=session_id,
        max_age=60*60*24,  # 24 hours
        path="/",
        samesite="lax" if DEV_MODE else "none",
        httponly=True,
        secure=not DEV_MODE
    )


def delete_auth_cookie(response: Response) -> None:
    """Delete authentication cookie with matching parameters."""
    response.delete_cookie(
        key="SID",
        path="/",
        samesite="lax" if DEV_MODE else "none"
    )