"""
Environment configuration for the FastAPI application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./notes.db")

# Application Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", 8000))

def get_settings():
    """Get application settings"""
    return {
        "secret_key": SECRET_KEY,
        "algorithm": ALGORITHM,
        "access_token_expire_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "database_url": DATABASE_URL,
        "debug": DEBUG,
        "port": PORT
    }
