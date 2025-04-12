from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Linux Patch Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/patch_management"
    )
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    
    # SSH Configuration
    SSH_KEY_DIR: str = os.getenv("SSH_KEY_DIR", "/etc/patch_management/ssh_keys")
    
    # File Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/var/lib/patch_management/uploads")
    
    # Web Server
    WEB_PORT: int = 443
    WEB_HOST: str = "0.0.0.0"
    
    class Config:
        case_sensitive = True

settings = Settings() 