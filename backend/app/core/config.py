from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Anti-Gravity Bug Bounty Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # Blockchain / Web3
    POLYGON_RPC_URL: str = "https://polygon-rpc.com"
    MUMBAI_RPC_URL: str = "https://rpc-mumbai.maticvigil.com"
    BOUNTY_VAULT_ADDRESS: str = ""
    PLATFORM_WALLET_PRIVATE_KEY: str = ""

    # IPFS (Pinata)
    PINATA_API_KEY: str = ""
    PINATA_SECRET_KEY: str = ""
    PINATA_BASE_URL: str = "https://api.pinata.cloud"

    # AI / ML
    CONFIDENCE_THRESHOLD_AUTO_APPROVE: float = 0.85
    MAX_REPORT_SIZE_KB: int = 5120  # 5 MB

    # Security
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Email (optional notifications)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
