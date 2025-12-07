import { useState, useEffect } from "react";
import { getRecipe } from "@/services/recipeApi";
import type { Recipe, IngredientItem } from "@/services/recipeApi";
import Navbar from "@/components/Navbar";

function RecipeDetail() {
  // Get recipe ID from URL path (e.g., /recipe/123)
  const getRecipeIdFromPath = () => {
    const path = window.location.pathname;
    const match = path.match(/\/recipe\/(\d+)/);
    return match ? match[1] : null;
  };

  const recipeId = getRecipeIdFromPath();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<{
    id: number;
    username: string;
    email: string;
  } | null>(null);
  const [isOwner, setIsOwner] = useState(false);

  useEffect(() => {
    // Get current user
    const fetchUser = async () => {
      try {
        const response = await fetch("http://localhost:8000/auth/me", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        }
      } catch (error) {
        // User not authenticated, but continue loading recipe
      }
    };

    fetchUser();
  }, []);

  useEffect(() => {
    const fetchRecipe = async () => {
      if (!recipeId) {
        setError("Recipe ID is required");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const recipeData = await getRecipe(parseInt(recipeId));
        setRecipe(recipeData);

        // Check if current user owns the recipe
        if (user && recipeData.user_id === user.id) {
          setIsOwner(true);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load recipe");
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [recipeId, user]);

  const handleBack = () => {
    // Navigate back to kitchen/search page
    window.location.href = "/kitchen";
  };

  const handleEdit = () => {
    // Navigate to edit page (to be implemented)
    if (recipeId) {
      window.location.href = `/recipe/${recipeId}/edit`;
    }
  };

  const handleDelete = async () => {
    if (!recipe || !window.confirm("Are you sure you want to delete this recipe?")) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/recipes/${recipe.id}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (response.ok) {
        // Navigate back to kitchen after successful deletion
        window.location.href = "/kitchen";
      } else {
        const errorData = await response.json().catch(() => ({ detail: "Failed to delete recipe" }));
        alert(errorData.detail || "Failed to delete recipe");
      }
    } catch (err) {
      alert("An error occurred while deleting the recipe");
    }
  };

  // Parse instructions - handle both string and array formats
  const parseInstructions = (instructions: string | string[]): string[] => {
    if (Array.isArray(instructions)) {
      return instructions;
    }
    // Split by newlines or numbered steps
    return instructions
      .split(/\n+/)
      .map((step) => step.trim())
      .filter((step) => step.length > 0);
  };

  // Parse ingredients - handle both array of objects and JSON string
  const parseIngredients = (ingredients: any): IngredientItem[] => {
    if (Array.isArray(ingredients)) {
      return ingredients.map((ing) => {
        if (typeof ing === "string") {
          return { name: ing };
        }
        return {
          name: ing.name || ing.ingredient_name || "",
          quantity: ing.quantity || undefined,
          unit: ing.unit || undefined,
        };
      });
    }
    return [];
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#DD0303] mx-auto mb-4"></div>
            <p className="text-[#DD0303] font-['Montserrat',sans-serif]">Loading recipe...</p>
          </div>
        </div>
      </>
    );
  }

  if (error || !recipe) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2] px-6 py-8">
          <div className="max-w-4xl mx-auto">
            <button
              onClick={handleBack}
              className="mb-6 text-[#DD0303] hover:text-[#FA812F] transition-colors font-['Montserrat',sans-serif] font-semibold"
            >
              ← Back to Search
            </button>
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
              <p className="font-['Montserrat',sans-serif]">
                {error || "Recipe not found"}
              </p>
            </div>
          </div>
        </div>
      </>
    );
  }

  const instructions = parseInstructions(recipe.instructions);
  const ingredients = parseIngredients(recipe.ingredients);
  const totalTime = (recipe.prep_time || 0) + (recipe.cook_time || 0);

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#FEF3E2] via-[#FFF8F0] to-[#FEF3E2] px-6 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <button
            onClick={handleBack}
            className="mb-6 text-[#DD0303] hover:text-[#FA812F] transition-colors font-['Montserrat',sans-serif] font-semibold flex items-center gap-2"
          >
            <span>←</span>
            <span>Back to Search</span>
          </button>

          {/* Recipe Header */}
          <div className="bg-[#FEF3E2] rounded-lg p-8 shadow-md border border-[#FA812F]/20 mb-6">
            <div className="flex justify-between items-start mb-4">
              <h1 className="text-4xl md:text-5xl font-black text-[#DD0303] font-['Playfair_Display',serif] tracking-[-0.03em] flex-1">
                {recipe.title}
              </h1>
              {isOwner && (
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={handleEdit}
                    className="px-4 py-2 bg-[#FA812F] text-[#FEF3E2] rounded-lg font-semibold hover:bg-[#DD0303] transition-colors font-['Montserrat',sans-serif] text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    className="px-4 py-2 bg-red-600 text-[#FEF3E2] rounded-lg font-semibold hover:bg-red-700 transition-colors font-['Montserrat',sans-serif] text-sm"
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>

            {recipe.description && (
              <p className="text-lg text-[#DD0303]/80 font-['Montserrat',sans-serif] mb-6">
                {recipe.description}
              </p>
            )}

            {/* Recipe Meta Information */}
            <div className="flex flex-wrap gap-6 text-[#DD0303]/80 font-['Montserrat',sans-serif]">
              {recipe.prep_time && (
                <div>
                  <span className="font-semibold">Prep Time:</span> {recipe.prep_time} min
                </div>
              )}
              {recipe.cook_time && (
                <div>
                  <span className="font-semibold">Cook Time:</span> {recipe.cook_time} min
                </div>
              )}
              {totalTime > 0 && (
                <div>
                  <span className="font-semibold">Total Time:</span> {totalTime} min
                </div>
              )}
              {recipe.servings && (
                <div>
                  <span className="font-semibold">Servings:</span> {recipe.servings}
                </div>
              )}
            </div>

            {recipe.source_url && (
              <div className="mt-4">
                <a
                  href={recipe.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[#FA812F] hover:text-[#DD0303] underline font-['Montserrat',sans-serif] text-sm"
                >
                  View Original Recipe
                </a>
              </div>
            )}
          </div>

          {/* Ingredients Section */}
          <div className="bg-[#FEF3E2] rounded-lg p-8 shadow-md border border-[#FA812F]/20 mb-6">
            <h2 className="text-2xl font-bold text-[#DD0303] mb-4 font-['Playfair_Display',serif]">
              Ingredients
            </h2>
            <ul className="space-y-2">
              {ingredients.map((ingredient, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-[#DD0303] font-['Montserrat',sans-serif]"
                >
                  <span className="text-[#FA812F] mt-1">•</span>
                  <span>
                    {ingredient.quantity && <span className="font-semibold">{ingredient.quantity} </span>}
                    {ingredient.unit && <span>{ingredient.unit} </span>}
                    <span>{ingredient.name}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Instructions Section */}
          <div className="bg-[#FEF3E2] rounded-lg p-8 shadow-md border border-[#FA812F]/20">
            <h2 className="text-2xl font-bold text-[#DD0303] mb-4 font-['Playfair_Display',serif]">
              Instructions
            </h2>
            <ol className="space-y-4">
              {instructions.map((step, index) => (
                <li
                  key={index}
                  className="flex gap-4 text-[#DD0303] font-['Montserrat',sans-serif]"
                >
                  <span className="flex-shrink-0 w-8 h-8 bg-[#DD0303] text-[#FEF3E2] rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </span>
                  <span className="flex-1 pt-1">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </div>
    </>
  );
}

export default RecipeDetail;

