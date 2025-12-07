from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from database import Recipe, User, get_db
from models.schemas import (
    RecipeResponse, 
    IngredientSearchRequest
)
from dependencies import get_current_user

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


@router.get("/search", response_model=List[RecipeResponse])
def search_recipes(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search recipes by title or description.
    """
    # Case-insensitive search on title and description
    search_term = f"%{q}%"
    query = select(Recipe).where(
        or_(
            Recipe.title.ilike(search_term),
            Recipe.description.ilike(search_term)
        )
    ).limit(limit).offset(offset).order_by(Recipe.created_at.desc())
    
    recipes = db.scalars(query).all()
    return recipes


@router.post("/search/ingredients", response_model=List[RecipeResponse])
def search_by_ingredients(
    search_request: IngredientSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search recipes by ingredients.
    If match_all is True, recipe must contain all ingredients.
    If match_all is False, recipe must contain any of the ingredients.
    Results are ranked by number of matching ingredients.
    """
    if not search_request.ingredients:
        raise HTTPException(status_code=400, detail="At least one ingredient is required")
    
    # Normalize ingredient names (lowercase for comparison)
    search_ingredients = [ing.lower().strip() for ing in search_request.ingredients if ing.strip()]
    
    if not search_ingredients:
        raise HTTPException(status_code=400, detail="No valid ingredients provided")
    
    # Get all recipes first, then filter and rank in Python for better flexibility
    # This allows us to handle partial matches and complex ranking
    all_recipes = db.scalars(select(Recipe)).all()
    
    def count_matches(recipe: Recipe) -> int:
        """Count how many search ingredients match the recipe's ingredients."""
        if not recipe.ingredients:
            return 0
        
        # Extract ingredient names from recipe (handle both dict and string formats)
        recipe_ingredient_names = []
        for ing in recipe.ingredients:
            if isinstance(ing, dict):
                name = ing.get("name", "").lower()
            elif isinstance(ing, str):
                name = ing.lower()
            else:
                continue
            recipe_ingredient_names.append(name)
        
        # Count matches (check if search ingredient is contained in any recipe ingredient)
        matches = 0
        for search_ing in search_ingredients:
            for recipe_ing in recipe_ingredient_names:
                if search_ing in recipe_ing or recipe_ing in search_ing:
                    matches += 1
                    break  # Count each search ingredient only once
        
        return matches
    
    def has_all_ingredients(recipe: Recipe) -> bool:
        """Check if recipe contains all search ingredients."""
        if not recipe.ingredients:
            return False
        
        # Extract ingredient names from recipe
        recipe_ingredient_names = []
        for ing in recipe.ingredients:
            if isinstance(ing, dict):
                name = ing.get("name", "").lower()
            elif isinstance(ing, str):
                name = ing.lower()
            else:
                continue
            recipe_ingredient_names.append(name)
        
        # Check if all search ingredients are found
        for search_ing in search_ingredients:
            found = False
            for recipe_ing in recipe_ingredient_names:
                if search_ing in recipe_ing or recipe_ing in search_ing:
                    found = True
                    break
            if not found:
                return False
        return True
    
    # Filter recipes based on match_all flag
    if search_request.match_all:
        filtered_recipes = [r for r in all_recipes if has_all_ingredients(r)]
    else:
        filtered_recipes = [r for r in all_recipes if count_matches(r) > 0]
    
    # Sort by match count (descending) and then by creation date
    sorted_recipes = sorted(filtered_recipes, key=lambda r: (count_matches(r), r.created_at), reverse=True)
    
    # Apply pagination
    start = search_request.offset
    end = start + search_request.limit
    paginated_recipes = sorted_recipes[start:end]
    
    return paginated_recipes


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single recipe by ID.
    """
    query = select(Recipe).where(Recipe.id == recipe_id)
    recipe = db.scalar(query)
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe


@router.get("", response_model=List[RecipeResponse])
def list_recipes(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all recipes with pagination.
    """
    query = select(Recipe).limit(limit).offset(offset).order_by(Recipe.created_at.desc())
    recipes = db.scalars(query).all()
    return recipes

