from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class User_in(BaseModel):
    username: str
    password: str
    email: str

class User_out(BaseModel):
    id: int
    username: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str


# Recipe Schemas
class IngredientItem(BaseModel):
    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[IngredientItem]  # List of ingredient objects
    instructions: str
    prep_time: Optional[int] = None  # in minutes
    cook_time: Optional[int] = None  # in minutes
    servings: Optional[int] = None
    source_url: Optional[str] = None

class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    ingredients: List[dict]  # JSON array from database
    instructions: str
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    source_url: Optional[str] = None
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RecipeSearchRequest(BaseModel):
    q: str  # Search query string
    limit: Optional[int] = 20
    offset: Optional[int] = 0

class IngredientSearchRequest(BaseModel):
    ingredients: List[str]  # List of ingredient names to search for
    match_all: Optional[bool] = False  # If True, recipe must contain all ingredients; if False, any ingredient
    limit: Optional[int] = 20
    offset: Optional[int] = 0

# Spoonacular Schemas (deprecated - keeping for backwards compatibility)
class SpoonacularRecipeSummary(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    imageType: Optional[str] = None

class SpoonacularSearchResponse(BaseModel):
    results: List[SpoonacularRecipeSummary]
    offset: int
    number: int
    totalResults: int