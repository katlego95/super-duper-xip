from functools import lru_cache

from app.config import get_settings
from supabase import Client, create_client

settings = get_settings()


@lru_cache()
def get_supabase_client() -> Client:
    """Get Supabase client instance (singleton)"""
    return create_client(
        supabase_url=settings.supabase_url, supabase_key=settings.supabase_service_key
    )


@lru_cache()
def get_supabase_anon_client() -> Client:
    """Get Supabase client with anon key (for auth)"""
    return create_client(
        supabase_url=settings.supabase_url, supabase_key=settings.supabase_anon_key
    )
