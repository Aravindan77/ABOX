from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import decode_access_token
from app.db.supabase_client import get_supabase_client

security = HTTPBearer(auto_error=False)


async def get_current_wallet(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extract and validate wallet address from Bearer JWT token.
    Raises 401 if token is missing or invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please connect your wallet.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["sub"]  # wallet address


async def get_optional_wallet(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str | None:
    """Returns the wallet address if authenticated, else None (for public endpoints)."""
    if credentials is None:
        return None
    payload = decode_access_token(credentials.credentials)
    return payload["sub"] if payload else None


def get_db():
    """Return the Supabase client instance."""
    return get_supabase_client()
