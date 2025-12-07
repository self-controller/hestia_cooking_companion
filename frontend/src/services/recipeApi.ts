const API_BASE_URL = "http://localhost:8000";

export interface IngredientItem {
  name: string;
  quantity?: string;
  unit?: string;
}

export interface Recipe {
  id: number;
  title: string;
  description?: string;
  ingredients: IngredientItem[] | any; // Can be JSON array from backend
  instructions: string;
  prep_time?: number;
  cook_time?: number;
  servings?: number;
  source_url?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface SearchParams {
  q: string;
  limit?: number;
  offset?: number;
}

export interface IngredientSearchParams {
  ingredients: string[];
  match_all?: boolean;
  limit?: number;
  offset?: number;
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const response = await fetch(url, {
    ...options,
    credentials: "include", // Include cookies for authentication
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Clear any stale auth data
      localStorage.removeItem("user");
      // Only redirect if we're not already on login page
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
      throw new Error("Not authenticated");
    }
    const errorData = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(errorData.detail || "Request failed");
  }

  return response.json();
}

export async function searchRecipes(params: SearchParams): Promise<Recipe[]> {
  const { q, limit = 20, offset = 0 } = params;
  const queryParams = new URLSearchParams({
    q,
    limit: limit.toString(),
    offset: offset.toString(),
  });
  
  return fetchWithAuth(`${API_BASE_URL}/api/recipes/search?${queryParams}`);
}

export async function searchByIngredients(params: IngredientSearchParams): Promise<Recipe[]> {
  return fetchWithAuth(`${API_BASE_URL}/api/recipes/search/ingredients`, {
    method: "POST",
    body: JSON.stringify({
      ingredients: params.ingredients,
      match_all: params.match_all || false,
      limit: params.limit || 20,
      offset: params.offset || 0,
    }),
  });
}

export async function getRecipe(id: number): Promise<Recipe> {
  return fetchWithAuth(`${API_BASE_URL}/api/recipes/${id}`);
}

export async function getAllRecipes(page: number = 1, limit: number = 20): Promise<Recipe[]> {
  const offset = (page - 1) * limit;
  const queryParams = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });
  
  return fetchWithAuth(`${API_BASE_URL}/api/recipes?${queryParams}`);
}

