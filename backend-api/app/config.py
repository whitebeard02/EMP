"""EMP application configuration."""
import os

from pydantic_settings import BaseSettings
from supabase import create_client, Client
from typing import Optional


class Settings(BaseSettings):
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()

_admin_client: Optional[Client] = None
_anon_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """Anon key client (respecting RLS, for public-safe operations)."""
    global _anon_client
    if _anon_client is None:
        _anon_client = create_client(settings.supabase_url, settings.supabase_anon_key)
    return _anon_client


def get_supabase_admin_client() -> Client:
    """Service role client (bypasses RLS; use only in backend)."""
    global _admin_client
    if _admin_client is None:
        _admin_client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
        )
    return _admin_client
