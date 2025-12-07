import { useState, useEffect, useCallback } from "react";
import { searchRecipes, searchByIngredients } from "@/services/recipeApi";
import type { Recipe } from "@/services/recipeApi";

type SearchMode = "name" | "ingredients";

function RecipeSearch() {
  const [searchMode, setSearchMode] = useState<SearchMode>("name");
  const [searchQuery, setSearchQuery] = useState("");
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [currentIngredient, setCurrentIngredient] = useState("");
  const [matchAll, setMatchAll] = useState(false);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  // Debounce function
  const debounce = useCallback((func: Function, wait: number) => {
    let timeout: ReturnType<typeof setTimeout>;
    return (...args: any[]) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), wait);
    };
  }, []);

  // Search by name with debouncing
  const performNameSearch = useCallback(
    debounce(async (query: string) => {
      if (!query.trim()) {
        setRecipes([]);
        setHasSearched(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const results = await searchRecipes({ q: query, limit: 20 });
        setRecipes(results);
        setHasSearched(true);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to search recipes"
        );
        setRecipes([]);
      } finally {
        setLoading(false);
      }
    }, 500),
    []
  );

  // Handle name search input change
  useEffect(() => {
    if (searchMode === "name") {
      performNameSearch(searchQuery);
    }
  }, [searchQuery, searchMode, performNameSearch]);

  // Search by ingredients
  const handleIngredientSearch = async () => {
    if (ingredients.length === 0) {
      setError("Please add at least one ingredient");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const results = await searchByIngredients({
        ingredients: ingredients,
        match_all: matchAll,
        limit: 20,
      });
      setRecipes(results);
      setHasSearched(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to search recipes");
      setRecipes([]);
    } finally {
      setLoading(false);
    }
  };

  // Add ingredient
  const addIngredient = () => {
    const trimmed = currentIngredient.trim();
    if (trimmed && !ingredients.includes(trimmed)) {
      setIngredients([...ingredients, trimmed]);
      setCurrentIngredient("");
    }
  };

  // Remove ingredient
  const removeIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  // Handle Enter key in ingredient input
  const handleIngredientKeyPress = (
    e: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addIngredient();
    }
  };

  // Handle recipe card click
  const handleRecipeClick = (recipeId: number) => {
    // Navigate to recipe detail page
    window.location.href = `/recipe/${recipeId}`;
  };

  return (
    <div className="w-full space-y-6">
      {/* Search Mode Toggle */}
      <div className="flex gap-4 border-b border-[#FA812F]/30 pb-4">
        <button
          onClick={() => {
            setSearchMode("name");
            setRecipes([]);
            setHasSearched(false);
            setError(null);
          }}
          className={`px-6 py-2 rounded-lg font-semibold transition-colors font-['Montserrat',sans-serif] ${
            searchMode === "name"
              ? "bg-[#DD0303] text-[#FEF3E2] shadow-md"
              : "bg-[#FEF3E2] text-[#DD0303] hover:bg-[#FA812F]/20"
          }`}
        >
          Search by Name
        </button>
        <button
          onClick={() => {
            setSearchMode("ingredients");
            setRecipes([]);
            setHasSearched(false);
            setError(null);
          }}
          className={`px-6 py-2 rounded-lg font-semibold transition-colors font-['Montserrat',sans-serif] ${
            searchMode === "ingredients"
              ? "bg-[#DD0303] text-[#FEF3E2] shadow-md"
              : "bg-[#FEF3E2] text-[#DD0303] hover:bg-[#FA812F]/20"
          }`}
        >
          Search by Ingredients
        </button>
      </div>

      {/* Search Input - Name Mode */}
      {searchMode === "name" && (
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search recipes by name or description..."
            className="w-full px-4 py-3 rounded-lg border-2 border-[#FA812F]/30 focus:border-[#DD0303] focus:outline-none text-[#DD0303] placeholder-[#DD0303]/50 font-['Montserrat',sans-serif] bg-[#FEF3E2]"
          />
          {loading && (
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-[#DD0303]"></div>
            </div>
          )}
        </div>
      )}

      {/* Search Input - Ingredients Mode */}
      {searchMode === "ingredients" && (
        <div className="space-y-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={currentIngredient}
              onChange={(e) => setCurrentIngredient(e.target.value)}
              onKeyPress={handleIngredientKeyPress}
              placeholder="Enter an ingredient (e.g., chicken, tomatoes)..."
              className="flex-1 px-4 py-3 rounded-lg border-2 border-[#FA812F]/30 focus:border-[#DD0303] focus:outline-none text-[#DD0303] placeholder-[#DD0303]/50 font-['Montserrat',sans-serif] bg-[#FEF3E2]"
            />
            <button
              onClick={addIngredient}
              className="px-6 py-3 bg-[#DD0303] text-[#FEF3E2] rounded-lg font-semibold hover:bg-[#FA812F] transition-colors font-['Montserrat',sans-serif]"
            >
              Add
            </button>
          </div>

          {/* Ingredients List */}
          {ingredients.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {ingredients.map((ingredient, index) => (
                <span
                  key={index}
                  className="inline-flex items-center gap-2 px-3 py-1 bg-[#FA812F]/20 text-[#DD0303] rounded-full font-['Montserrat',sans-serif] text-sm"
                >
                  {ingredient}
                  <button
                    onClick={() => removeIngredient(index)}
                    className="hover:text-[#FA812F] transition-colors"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}

          {/* Match All Toggle */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="matchAll"
              checked={matchAll}
              onChange={(e) => setMatchAll(e.target.checked)}
              className="w-4 h-4 text-[#DD0303] border-[#FA812F]/30 rounded focus:ring-[#DD0303]"
            />
            <label
              htmlFor="matchAll"
              className="text-[#DD0303] font-['Montserrat',sans-serif] text-sm"
            >
              Recipe must contain all ingredients
            </label>
          </div>

          {/* Search Button */}
          <button
            onClick={handleIngredientSearch}
            disabled={ingredients.length === 0 || loading}
            className="w-full px-6 py-3 bg-[#DD0303] text-[#FEF3E2] rounded-lg font-semibold hover:bg-[#FA812F] transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-['Montserrat',sans-serif]"
          >
            {loading ? "Searching..." : "Search Recipes"}
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg font-['Montserrat',sans-serif]">
          {error}
        </div>
      )}

      {/* Loading State */}
      {loading && searchMode === "ingredients" && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#DD0303]"></div>
        </div>
      )}

      {/* Empty State */}
      {hasSearched && !loading && recipes.length === 0 && !error && (
        <div className="text-center py-12">
          <p className="text-[#DD0303]/70 font-['Montserrat',sans-serif] text-lg">
            No recipes found. Try a different search.
          </p>
        </div>
      )}

      {/* Results Grid */}
      {recipes.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <div
              key={recipe.id}
              onClick={() => handleRecipeClick(recipe.id)}
              className="bg-[#FEF3E2] rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow cursor-pointer border border-[#FA812F]/20 hover:border-[#DD0303]/30"
            >
              <h3 className="text-xl font-bold text-[#DD0303] mb-2 font-['Playfair_Display',serif]">
                {recipe.title}
              </h3>
              {recipe.description && (
                <p className="text-[#DD0303]/70 text-sm mb-4 line-clamp-2 font-['Montserrat',sans-serif]">
                  {recipe.description}
                </p>
              )}
              <div className="flex flex-wrap gap-4 text-sm text-[#DD0303]/80 font-['Montserrat',sans-serif]">
                {recipe.prep_time && <span>Prep: {recipe.prep_time} min</span>}
                {recipe.cook_time && <span>Cook: {recipe.cook_time} min</span>}
                {recipe.servings && <span>Serves: {recipe.servings}</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RecipeSearch;
