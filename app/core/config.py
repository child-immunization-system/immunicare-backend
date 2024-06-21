import os
from typing import Optional
from pydantic import DirectoryPath, EmailStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEFAULT_DATABASE: str = os.getenv("DEFAULT_DATABASE")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # FRONTEND_URL: str

settings = Settings()