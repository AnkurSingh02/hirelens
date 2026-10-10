from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    # App Settings
    environment: str = os.getenv("ENVIRONMENT", "development")
    cors_origins: List[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",")

    # Model Settings
    llm_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "all-MiniLM-L6-v2"

    # Rate Limiting
    rate_limit: str = "10/minute"

    # File Upload
    max_file_size_mb: int = 10
    allowed_extensions: List[str] = [".pdf"]

    class Config:
        env_file = ".env"


settings = Settings()