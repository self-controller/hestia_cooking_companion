import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import User
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
    
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password

def get_user_by_email(email: str, db: Session):
    query = select(User).where(User.email == email)
    user = db.scalar(query)
    return user

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
