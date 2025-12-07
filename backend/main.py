# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import redis
from database import init_db, engine
from routes.routes import router
from routes.recipes import router as recipes_router
from dependencies import set_redis_client
from config import REDIS_URL, CORS_ORIGINS

# --- Lifespan --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: init Redis and optionally test DB
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    set_redis_client(redis_client)

    # quick smoke test (optional)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    init_db()

    yield  # app runs here

    # shutdown: close Redis + DB engine
    set_redis_client(None)
    if redis_client is not None:
        redis_client.close()

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

app.include_router(router)
app.include_router(recipes_router)