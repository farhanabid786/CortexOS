import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "CortexOS API"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Security Settings
    JWT_SECRET_KEY: str = "cortexos_super_secret_development_key_change_me_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database Settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./cortexos.db"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Gemini API
    GEMINI_API_KEY: str = ""
    
    # Configuration sources
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
