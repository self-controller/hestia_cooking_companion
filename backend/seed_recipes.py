"""
Script to seed initial recipes from Spoonacular.
Usage: python seed_recipes.py <user_email> <number_of_recipes>
"""
import sys
from database import SessionLocal, User, Recipe
from spoonacular_service import search_spoonacular_recipes, get_spoonacular_recipe, convert_spoonacular_to_recipe

def seed_recipes(user_email: str, num_recipes: int = 20):
    """Seed recipes from Spoonacular for a user."""
    db = SessionLocal()
    
    try:
        # Get user
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            print(f"User with email {user_email} not found!")
            return
        
        print(f"Seeding {num_recipes} recipes for user: {user.username}")
        
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
                        # Check if recipe already exists for this user
                        existing = db.query(Recipe).filter(
                            Recipe.user_id == user.id,
                            Recipe.source_url.like(f"%{recipe_id}%")
                        ).first()
                        
                        if existing:
                            print(f"Recipe {recipe_id} already exists, skipping...")
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
                            user_id=user.id
                        )
                        
                        db.add(db_recipe)
                        recipes_added += 1
                        print(f"Added recipe: {recipe_data['title']}")
                        
                    except Exception as e:
                        print(f"Error importing recipe {recipe_id}: {e}")
                        continue
                
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
        
        db.commit()
        print(f"\nSuccessfully seeded {recipes_added} recipes!")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python seed_recipes.py <user_email> [number_of_recipes]")
        sys.exit(1)
    
    user_email = sys.argv[1]
    num_recipes = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    seed_recipes(user_email, num_recipes)