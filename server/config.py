import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///feedback.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///velox.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret"
