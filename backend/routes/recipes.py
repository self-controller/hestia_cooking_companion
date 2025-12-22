from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_

from database import Recipe, User, get_db
from models.schemas import (
    RecipeResponse, 
    IngredientSearchRequest,
    RecipeCreate
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
    Search recipes by title or description (user's recipes + default recipes).
    """
    # Validate search query
    if not q or not q.strip():
        return []
    
    # Case-insensitive search on title and description
    search_term = f"%{q.strip()}%"
    query = select(Recipe).where(
        and_(
            or_(
                Recipe.user_id == current_user.id,  # User's own recipes
                Recipe.user_id.is_(None)  # Default recipes for all users
            ),
            or_(
                Recipe.title.ilike(search_term),
                and_(Recipe.description.isnot(None), Recipe.description.ilike(search_term))
            )
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
    Search recipes by ingredients (user's recipes only).
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
    
    # Get user's recipes only
    all_recipes = db.scalars(
        select(Recipe).where(
            or_(
                Recipe.user_id == current_user.id,  # User's own recipes
                Recipe.user_id.is_(None)  # Default recipes for all users
            )
        )
    ).all()

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


@router.get("", response_model=List[RecipeResponse])
def list_recipes(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all recipes with pagination (user's recipes only).
    """
    query = select(Recipe).where(
        or_(
            Recipe.user_id == current_user.id,  # User's own recipes
            Recipe.user_id.is_(None)  # Default recipes for all users
        )
    ).limit(limit).offset(offset).order_by(Recipe.created_at.desc())
    recipes = db.scalars(query).all()
    return recipes


@router.post("", response_model=RecipeResponse)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe."""
    # Convert ingredients to JSON format
    ingredients_json = [{"name": ing.name, "quantity": ing.quantity, "unit": ing.unit} for ing in recipe.ingredients]
    
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=ingredients_json,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        servings=recipe.servings,
        source_url=recipe.source_url,
        user_id=current_user.id
    )
    
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    return db_recipe


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single recipe by ID (user's recipes only).
    """
    query = select(Recipe).where(
        Recipe.id == recipe_id,
        or_(
            Recipe.user_id == current_user.id,
            Recipe.user_id.is_(None)
        )
    )
    recipe = db.scalar(query)
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe