from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    app_name: str = "PaySense"
    version: str = "0.1.0"

    # Database
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str

    # AI
    anthropic_api_key: str

    # CORS
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
