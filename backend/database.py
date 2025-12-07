from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
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
    
    # Relationships
    recipes = relationship("Recipe", back_populates="user", cascade="all, delete-orphan")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    ingredients = Column(JSON, nullable=False)  # Store as JSON array: [{"name": "flour", "quantity": "2", "unit": "cups"}, ...]
    instructions = Column(Text, nullable=False)
    prep_time = Column(Integer, nullable=True)  # in minutes
    cook_time = Column(Integer, nullable=True)  # in minutes
    servings = Column(Integer, nullable=True)
    source_url = Column(String, nullable=True)  # For AI-parsed recipes
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="recipes")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    ingredient_name = Column(String, nullable=False, index=True)
    quantity = Column(String, nullable=True)  # e.g., "2", "1/2"
    unit = Column(String, nullable=True)  # e.g., "cups", "tbsp", "lbs"
    
    # Relationships
    recipe = relationship("Recipe", back_populates="recipe_ingredients")




def init_db():
    Base.metadata.create_all(bind=engine)
