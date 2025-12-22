"""
Spoonacular API service for searching and fetching recipes.
"""
import requests
import re
from typing import Dict, List, Optional
from config import SPOONACULAR_API_KEY, SPOONACULAR_BASE_URL


def search_spoonacular_recipes(query: str, number: int = 10, offset: int = 0) -> Dict:
    """
    Search for recipes using Spoonacular API.
    
    Args:
        query: Search query string
        number: Number of results to return (default: 10)
        offset: Number of results to skip (default: 0)
    
    Returns:
        Dictionary with 'results' key containing list of recipe summaries
    """
    url = f"{SPOONACULAR_BASE_URL}/recipes/complexSearch"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "number": number,
        "offset": offset,
        "addRecipeInformation": False,  # We'll fetch full details separately
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_spoonacular_recipe(recipe_id: int) -> Dict:
    """
    Get full recipe information by ID from Spoonacular API.
    
    Args:
        recipe_id: Spoonacular recipe ID
    
    Returns:
        Dictionary with full recipe information
    """
    url = f"{SPOONACULAR_BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "includeNutrition": False,
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def convert_spoonacular_to_recipe(spoonacular_data: Dict) -> Dict:
    """
    Convert Spoonacular recipe format to our internal recipe format.
    
    Args:
        spoonacular_data: Recipe data from Spoonacular API
    
    Returns:
        Dictionary in our internal recipe format
    """
    # Extract ingredients
    ingredients = []
    for ingredient in spoonacular_data.get("extendedIngredients", []):
        ingredients.append({
            "name": ingredient.get("name", ""),
            "quantity": str(ingredient.get("amount", "")),
            "unit": ingredient.get("unit", "")
        })
    
    # Extract instructions
    instructions = ""
    analyzed_instructions = spoonacular_data.get("analyzedInstructions", [])
    if analyzed_instructions:
        steps = analyzed_instructions[0].get("steps", [])
        instruction_list = [step.get("step", "") for step in steps]
        instructions = "\n".join(instruction_list)
    
    # Extract prep and cook time
    prep_time = spoonacular_data.get("preparationMinutes")
    cook_time = spoonacular_data.get("cookingMinutes")
    
    # If total time is available but prep/cook are not, estimate
    if not prep_time and not cook_time:
        total_time = spoonacular_data.get("readyInMinutes")
        if total_time:
            # Rough estimate: 30% prep, 70% cook
            prep_time = int(total_time * 0.3)
            cook_time = int(total_time * 0.7)
    
    # Clean HTML tags from description
    description = spoonacular_data.get("summary", "")
    if description:
        # Remove HTML tags
        description = re.sub(r'<[^>]+>', '', description)
        # Limit length
        description = description[:500] if len(description) > 500 else description
    
    return {
        "title": spoonacular_data.get("title", ""),
        "description": description if description else None,
        "ingredients": ingredients,
        "instructions": instructions,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "servings": spoonacular_data.get("servings"),
        "source_url": spoonacular_data.get("sourceUrl") or spoonacular_data.get("spoonacularSourceUrl"),
    }

