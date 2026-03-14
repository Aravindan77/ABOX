from supabase import create_client, Client
from functools import lru_cache
from app.core.config import settings


@lru_cache()
def get_supabase_client() -> Client:
    """Return a cached Supabase client using the anon/public key."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in your .env file"
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


@lru_cache()
def get_supabase_admin() -> Client:
    """Return a cached Supabase client using the service-role key (admin access)."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in your .env file"
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
