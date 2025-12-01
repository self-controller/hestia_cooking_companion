# main.py
from contextlib import asynccontextmanager

from typing import Optional
from fastapi import FastAPI, Depends, Response, HTTPException, Cookie
from sqlalchemy import create_engine, text, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, Session
import redis
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from models.schemas import User_in, User_out
from helper import hash_password, get_user_by_email, get_uuid
from database import User, init_db, get_db, engine


REDIS_URL = "redis://localhost:6379/0"

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

@app.post("/signup", response_model=User_out)
def signup(*, user: User_in, db: Session = Depends(get_db), response: Response, r: redis.Redis = Depends(get_redis)):
    new_user = User(
        username=user.username, 
        email=user.email, 
        hash_password=hash_password(user.password)
        )
    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    db.refresh(new_user)
    SID = get_uuid()
    response.set_cookie(key="SID", value=SID)
    r.setex(name=SID, time=60*60*24, value="yay its working")
    return new_user

@app.get("/auth/me")
def authenticate(SID: Optional[str] = Cookie(None)):
    if SID:
        return {"message": f"Session ID: {SID}"}
    else:
        return {"message": "Session ID cookie not found."}

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="SID")
    return {"message": "You have been logged out"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    query = select(User)
    result = db.execute(query)
    return result.scalars().all()


