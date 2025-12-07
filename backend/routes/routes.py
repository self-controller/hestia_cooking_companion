from typing import Optional
from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import redis

from models.schemas import User_in, User_out, LoginRequest
from helper import hash_password, get_user_by_email, get_uuid, verify_password, set_auth_cookie, delete_auth_cookie
from database import User, get_db
from dependencies import get_redis, get_current_user
from config import DEV_MODE

router = APIRouter()


# --- Routes ----------------------------------------------------
@router.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"db": result.scalar_one()}

@router.get("/ping-redis")
def ping_redis(r: redis.Redis = Depends(get_redis)):
    r.set("ping", "pong", ex=10)
    value = r.get("ping")
    return {"redis": value}

@router.post("/register", response_model=User_out)
def register(*, user: User_in, 
           db: Session = Depends(get_db), 
           response: Response, 
           r: redis.Redis = Depends(get_redis)
           ):
    # creates new user
    new_user = User(
        username=user.username, 
        email=user.email, 
        hash_password=hash_password(user.password)
        )
    # adds to database
    db.add(new_user)

    try:
        # commits changes to db
        db.commit()
    except IntegrityError:
        # undoes uncommitted changes
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    db.refresh(new_user)
    # create a cookie for user
    SID = get_uuid()
    set_auth_cookie(response, SID)
    r.setex(name=SID, time=60*60*24, value=str(new_user.id)) # <-- IMPORTANT -- Change samesite and secure when deploying
    return new_user

@router.get("/auth/me", response_model=User_out)
def authenticate(current_user: User = Depends(get_current_user),
                 response: Response = None,
                 r: redis.Redis = Depends(get_redis),
                ) -> User_out:
    # In dev mode, optionally set a cookie for consistency with frontend
    if DEV_MODE:
        dev_session_id = "dev_session"
        set_auth_cookie(response, dev_session_id)
        r.setex(name=dev_session_id, time=60*60*24, value=str(current_user.id))
    
    # Return user data (User_out schema will exclude hash_password)
    return current_user
    
@router.post("/logout")
def logout(response: Response, SID: Optional[str] = Cookie(None), r: redis.Redis = Depends(get_redis)):
    # Delete session from Redis if exists
    if SID:
        r.delete(SID)
    # Delete the cookie from the browser with same parameters as setting
    delete_auth_cookie(response)
    return {"message": "You have been logged out"}

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    # creates sql query to select all users
    query = select(User)
    result = db.execute(query)
    return result.scalars().all()

@router.post("/auth/login", response_model=User_out)
def login(*, login_request: LoginRequest, 
          db: Session = Depends(get_db), 
          response: Response, 
          r: redis.Redis = Depends(get_redis)):
    # find user through inputted email
    curr_user = get_user_by_email(login_request.email, db)
    # verify password and email
    if curr_user and verify_password(login_request.password, curr_user.hash_password):
        # create new cookie if verified
        SID = get_uuid()
        set_auth_cookie(response, SID)
        r.setex(name=SID, time=60*60*24, value=str(curr_user.id)) # <-- IMPORTANT -- Change samesite and secure when deploying
        return curr_user
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

