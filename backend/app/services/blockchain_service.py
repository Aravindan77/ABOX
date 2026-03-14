"""
Blockchain Service - Interacts with the BountyVault smart contract on Polygon.
"""
import json
import os
from pathlib import Path
from typing import Optional
from web3 import Web3
from app.core.config import settings


# Load ABI from the frontend contracts directory
_ABI_PATH = Path(__file__).parent.parent.parent.parent / "frontend" / "contracts" / "BountyVault.json"


def _load_abi() -> list:
    if _ABI_PATH.exists():
        with open(_ABI_PATH) as f:
            data = json.load(f)
            return data.get("abi", data)  # handle both raw ABI and Hardhat artifact
    return []


class BlockchainService:
    def __init__(self):
        rpc = (
            settings.MUMBAI_RPC_URL
            if settings.ENVIRONMENT != "production"
            else settings.POLYGON_RPC_URL
        )
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self._contract = None

    @property
    def contract(self):
        if self._contract is None and settings.BOUNTY_VAULT_ADDRESS:
            abi = _load_abi()
            if abi:
                self._contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(settings.BOUNTY_VAULT_ADDRESS),
                    abi=abi,
                )
        return self._contract

    def is_available(self) -> bool:
        return bool(
            self.w3.is_connected()
            and settings.BOUNTY_VAULT_ADDRESS
            and settings.PLATFORM_WALLET_PRIVATE_KEY
        )

    def get_bounty_pool(self, project_id: str) -> int:
        """Return the available bounty pool in Wei for a project."""
        if not self.contract:
            return 0
        try:
            return self.contract.functions.getBountyPool(project_id).call()
        except Exception:
            return 0

    def submit_bug_on_chain(
        self,
        bug_id: str,
        researcher: str,
        ipfs_cid: str,
        ai_confidence: int,  # 0-100
    ) -> Optional[str]:
        """
        Call submitBug() on the BountyVault and return the tx hash.
        Returns None if blockchain interaction is not available.
        """
        if not self.is_available() or not self.contract:
            return None
        try:
            account = self.w3.eth.account.from_key(settings.PLATFORM_WALLET_PRIVATE_KEY)
            nonce = self.w3.eth.get_transaction_count(account.address)
            tx = self.contract.functions.submitBug(
                bug_id,
                Web3.to_checksum_address(researcher),
                ipfs_cid,
                ai_confidence,
            ).build_transaction({
                "from": account.address,
                "nonce": nonce,
                "gas": 300_000,
                "gasPrice": self.w3.to_wei("50", "gwei"),
            })
            signed = self.w3.eth.account.sign_transaction(tx, settings.PLATFORM_WALLET_PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            return tx_hash.hex()
        except Exception as e:
            print(f"[BlockchainService] submit_bug_on_chain error: {e}")
            return None

    def release_bounty(self, bug_id: str, researcher: str, amount_wei: int) -> Optional[str]:
        """Transfer bounty to a researcher wallet. Returns tx hash or None."""
        if not self.is_available() or not self.contract:
            return None
        try:
            account = self.w3.eth.account.from_key(settings.PLATFORM_WALLET_PRIVATE_KEY)
            nonce = self.w3.eth.get_transaction_count(account.address)
            tx = self.contract.functions.releaseBounty(
                bug_id,
                Web3.to_checksum_address(researcher),
                amount_wei,
            ).build_transaction({
                "from": account.address,
                "nonce": nonce,
                "gas": 200_000,
                "gasPrice": self.w3.to_wei("50", "gwei"),
            })
            signed = self.w3.eth.account.sign_transaction(tx, settings.PLATFORM_WALLET_PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            return tx_hash.hex()
        except Exception as e:
            print(f"[BlockchainService] release_bounty error: {e}")
            return None


blockchain_service = BlockchainService()
