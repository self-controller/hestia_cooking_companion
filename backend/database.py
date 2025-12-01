from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
import redis
from sqlalchemy.ext.declarative import declarative_base
from models.schemas import User_in

# --- Config ----------------------------------------------------
DATABASE_URL = "postgresql://postgres:postgres@localhost:5431/hestia_db"

# --- Postgres (sync SQLAlchemy) --------------------------------
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Create Table  ---------------------------------------------
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)
