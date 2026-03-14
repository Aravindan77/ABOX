import httpx
import base64
from typing import Optional
from app.core.config import settings


class IPFSService:
    """Upload files and JSON to IPFS via Pinata."""

    BASE = settings.PINATA_BASE_URL

    def _headers(self) -> dict:
        return {
            "pinata_api_key": settings.PINATA_API_KEY,
            "pinata_secret_api_key": settings.PINATA_SECRET_KEY,
        }

    def _is_configured(self) -> bool:
        return bool(settings.PINATA_API_KEY and settings.PINATA_SECRET_KEY)

    async def upload_file(self, file_bytes: bytes, filename: str) -> Optional[str]:
        """Upload raw bytes to Pinata and return the IPFS CID."""
        if not self._is_configured():
            return None
        url = f"{self.BASE}/pinning/pinFileToIPFS"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                url,
                headers=self._headers(),
                files={"file": (filename, file_bytes)},
            )
            resp.raise_for_status()
            return resp.json().get("IpfsHash")

    async def upload_json(self, data: dict, name: str = "bug_report") -> Optional[str]:
        """Upload a JSON dict to Pinata and return the IPFS CID."""
        if not self._is_configured():
            return None
        url = f"{self.BASE}/pinning/pinJSONToIPFS"
        payload = {
            "pinataMetadata": {"name": name},
            "pinataContent": data,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, headers=self._headers(), json=payload)
            resp.raise_for_status()
            return resp.json().get("IpfsHash")

    @staticmethod
    def gateway_url(cid: str) -> str:
        """Return a public IPFS gateway URL for a CID."""
        return f"https://gateway.pinata.cloud/ipfs/{cid}"


ipfs_service = IPFSService()
