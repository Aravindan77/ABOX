from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
from datetime import datetime, timedelta
from typing import Optional
import jwt

from app.core.config import settings


def verify_wallet_signature(address: str, message: str, signature: str) -> bool:
    """
    Verify an Ethereum wallet signature.
    Returns True if the signature was produced by the owner of `address`.
    """
    try:
        msg = encode_defunct(text=message)
        recovered = Account.recover_message(msg, signature=signature)
        return recovered.lower() == address.lower()
    except Exception:
        return False


def create_nonce_message(address: str, nonce: str) -> str:
    """Generate the canonical sign-in message for a wallet."""
    return (
        f"Sign in to Anti-Gravity Bug Bounty Platform\n\n"
        f"Wallet: {address}\n"
        f"Nonce: {nonce}\n"
        f"Issued at: {datetime.utcnow().isoformat()}Z"
    )


def create_access_token(wallet_address: str, extra: Optional[dict] = None) -> str:
    """Create a JWT token for an authenticated wallet address."""
    payload = {
        "sub": wallet_address.lower(),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token. Returns the payload or None on failure."""
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def checksum_address(address: str) -> str:
    """Return EIP-55 checksum address."""
    return Web3.to_checksum_address(address)
