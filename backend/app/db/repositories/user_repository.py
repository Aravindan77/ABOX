from typing import Optional, List
from supabase import Client
from datetime import datetime
import uuid


class UserRepository:
    """Data access layer for users table."""

    def __init__(self, db: Client):
        self.db = db
        self.table = "users"

    def get_by_wallet(self, wallet_address: str) -> Optional[dict]:
        res = (
            self.db.table(self.table)
            .select("*")
            .eq("wallet_address", wallet_address.lower())
            .maybe_single()
            .execute()
        )
        return res.data

    def create_or_update(self, wallet_address: str, data: dict = {}) -> dict:
        existing = self.get_by_wallet(wallet_address)
        now = datetime.utcnow().isoformat()
        if existing:
            res = (
                self.db.table(self.table)
                .update({**data, "last_seen": now})
                .eq("wallet_address", wallet_address.lower())
                .execute()
            )
        else:
            payload = {
                "id": str(uuid.uuid4()),
                "wallet_address": wallet_address.lower(),
                "created_at": now,
                "last_seen": now,
                "trust_score": 50.0,
                "total_submissions": 0,
                "accepted_submissions": 0,
                "rejected_submissions": 0,
                "total_earned_matic": 0.0,
                **data,
            }
            res = self.db.table(self.table).insert(payload).execute()
        return res.data[0] if res.data else {}

    def update_nonce(self, wallet_address: str, nonce: str) -> dict:
        return self.create_or_update(wallet_address, {"auth_nonce": nonce})

    def increment_submission(self, wallet_address: str, accepted: bool) -> dict:
        user = self.get_by_wallet(wallet_address)
        if not user:
            return {}
        updates = {"total_submissions": (user.get("total_submissions") or 0) + 1}
        if accepted:
            updates["accepted_submissions"] = (user.get("accepted_submissions") or 0) + 1
        else:
            updates["rejected_submissions"] = (user.get("rejected_submissions") or 0) + 1
        res = (
            self.db.table(self.table)
            .update(updates)
            .eq("wallet_address", wallet_address.lower())
            .execute()
        )
        return res.data[0] if res.data else {}

    def update_trust_score(self, wallet_address: str, score: float) -> dict:
        res = (
            self.db.table(self.table)
            .update({"trust_score": round(score, 2)})
            .eq("wallet_address", wallet_address.lower())
            .execute()
        )
        return res.data[0] if res.data else {}

    def leaderboard(self, limit: int = 20) -> List[dict]:
        res = (
            self.db.table(self.table)
            .select("wallet_address, trust_score, accepted_submissions, total_earned_matic")
            .order("trust_score", desc=True)
            .limit(limit)
            .execute()
        )
        return res.data or []
