"""
Script to seed default recipes for all users.
Usage: python seed_default_recipes.py [number_of_recipes]
"""
import sys
from database import SessionLocal, Recipe
from spoonacular_service import search_spoonacular_recipes, get_spoonacular_recipe, convert_spoonacular_to_recipe

def seed_default_recipes(num_recipes: int = 20):
    """Seed default recipes (user_id = None) that all users can access."""
    db = SessionLocal()
    
    try:
        print(f"Seeding {num_recipes} default recipes for all users...")
        
        # Search for popular recipes
        popular_queries = ["pasta", "chicken", "dessert", "salad", "soup", "pizza", "bread", "cake"]
        recipes_added = 0
        
        for query in popular_queries:
            if recipes_added >= num_recipes:
                break
                
            try:
                results = search_spoonacular_recipes(query, number=5)
                recipe_ids = [r["id"] for r in results.get("results", [])]
                
                for recipe_id in recipe_ids:
                    if recipes_added >= num_recipes:
                        break
                    
                    try:
                        # Check if recipe already exists as a default recipe
                        existing = db.query(Recipe).filter(
                            Recipe.user_id.is_(None),
                            Recipe.source_url.like(f"%{recipe_id}%")
                        ).first()
                        
                        if existing:
                            print(f"Default recipe {recipe_id} already exists, skipping...")
                            continue
                        
                        # Fetch and import recipe
                        spoonacular_data = get_spoonacular_recipe(recipe_id)
                        recipe_data = convert_spoonacular_to_recipe(spoonacular_data)
                        
                        db_recipe = Recipe(
                            title=recipe_data["title"],
                            description=recipe_data["description"],
                            ingredients=recipe_data["ingredients"],
                            instructions=recipe_data["instructions"],
                            prep_time=recipe_data["prep_time"],
                            cook_time=recipe_data["cook_time"],
                            servings=recipe_data["servings"],
                            source_url=recipe_data["source_url"],
                            user_id=None  # NULL for default recipes
                        )
                        
                        db.add(db_recipe)
                        recipes_added += 1
                        print(f"Added default recipe: {recipe_data['title']}")
                        
                    except Exception as e:
                        print(f"Error importing recipe {recipe_id}: {e}")
                        continue
                
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
        
        db.commit()
        print(f"\nSuccessfully seeded {recipes_added} default recipes!")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    num_recipes = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seed_default_recipes(num_recipes)