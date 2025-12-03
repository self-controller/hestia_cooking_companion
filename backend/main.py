# main.py
from contextlib import asynccontextmanager

from typing import Optional
from fastapi import FastAPI, Depends, Response, HTTPException, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, Session
import redis
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from models.schemas import User_in, User_out, LoginRequest
from helper import hash_password, get_user_by_email, get_uuid, verify_password
from database import User, init_db, get_db, engine
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# get CORS origins via .env file
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:5173"
    ).split(",")

CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS]

DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

# --- Redis (sync redis-py) -------------------------------------
redis_client: redis.Redis | None = None

def get_redis() -> redis.Redis:
    # lifespan guarantees this is set
    assert redis_client is not None, "Redis not initialized"
    return redis_client

# --- Lifespan --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client

    # startup: init Redis and optionally test DB
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)

    # quick smoke test (optional)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    init_db()

    yield  # app runs here

    # shutdown: close Redis + DB engine
    if redis_client is not None:
        redis_client.close()
        redis_client = None

    engine.dispose()

app = FastAPI(lifespan=lifespan)

# --- CORS Middleware -------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ----------------------------------------------------
@app.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"db": result.scalar_one()}

@app.get("/ping-redis")
def ping_redis(r: redis.Redis = Depends(get_redis)):
    r.set("ping", "pong", ex=10)
    value = r.get("ping")
    return {"redis": value}

@app.post("/register", response_model=User_out)
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
    response.set_cookie(key="SID", value=SID, max_age=60*60*24, path="/", 
                        samesite="lax", httponly=True, secure=False)        
    r.setex(name=SID, time=60*60*24, value=str(new_user.id)) # <-- IMPORTANT -- Change samesite and secure when deploying
    return new_user

@app.get("/auth/me", response_model=User_out)
def authenticate(SID: Optional[str] = Cookie(None), 
                 r: redis.Redis = Depends(get_redis),
                 db: Session = Depends(get_db)
                 ):
    # Dev mode: return mock user
    if DEV_MODE:
        # Return a mock user for development
        mock_user = User_out(
            id=1,
            username="dev_user",
            email="dev@example.com"
        )
        return mock_user

    # confirm SID cookie exists
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
    
    # Return user data (User_out schema will exclude hash_password)
    return user

@app.post("/logout")
def logout(response: Response, SID: Optional[str] = Cookie(None), r: redis.Redis = Depends(get_redis)):
    # Delete session from Redis if exists
    if SID:
        r.delete(SID)
    # Delete the cookie from the browser 
    response.delete_cookie(key="SID")
    return {"message": "You have been logged out"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # creates sql query to select all users
    query = select(User)
    result = db.execute(query)
    return result.scalars().all()

@app.post("/auth/login", response_model=User_out)
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
        response.set_cookie(key="SID", value=SID, max_age=60*60*24, path="/", 
                            samesite="lax", httponly=True, secure=False) 
        r.setex(name=SID, time=60*60*24, value=str(curr_user.id)) # <-- IMPORTANT -- Change samesite and secure when deploying
        return curr_user
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

