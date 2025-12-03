import os
from dotenv import load_dotenv

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# CORS configuration
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:5173"
).split(",")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS]

# Development mode
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "false"