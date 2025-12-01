# backend/routes/recipes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import Recipe
from backend.models.schemas import RecipeCreate, Recipe
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

router = APIRouter()

@router.get("/")
def home():
    return{"status": "ok"}


@router.get(f"/register")
async def serve_registration_page():
    """Serve the React app for the registration page"""
    index_path = frontend_dist / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in frontend directory.")
    
@router.post(f"/register")
async def register_user():
#     """Serve the React app for the registration page"""
#     index_path = frontend_dist / "index.html"
#     if index_path.exists():
#         return FileResponse(str(index_path))
#     raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in frontend directory.")
    return {"status": " OK"}

@router.get(f"/login")
async def serve_login_page():
#     """Serve the React app for the registration page"""
#     index_path = frontend_dist / "index.html"
#     if index_path.exists():
#         return FileResponse(str(index_path))
#     raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in frontend directory.")
    return {"status": " OK"}
    
@router.post(f"/login")
async def login_user():
#     """Serve the React app for the registration page"""
#     index_path = frontend_dist / "index.html"
#     if index_path.exists():
#         return FileResponse(str(index_path))
#     raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in frontend directory.")
    return {"status": " OK"}

