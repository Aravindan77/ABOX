from typing import Optional, List, dict
from supabase import Client
from datetime import datetime
import uuid


class BugRepository:
    """Data access layer for bug_reports table."""

    def __init__(self, db: Client):
        self.db = db
        self.table = "bug_reports"

    def create(self, data: dict) -> dict:
        data.setdefault("id", str(uuid.uuid4()))
        data.setdefault("created_at", datetime.utcnow().isoformat())
        data.setdefault("status", "pending")
        res = self.db.table(self.table).insert(data).execute()
        return res.data[0] if res.data else {}

    def get_by_id(self, bug_id: str) -> Optional[dict]:
        res = (
            self.db.table(self.table)
            .select("*")
            .eq("id", bug_id)
            .single()
            .execute()
        )
        return res.data

    def list_by_project(
        self,
        project_id: str,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[dict]:
        query = (
            self.db.table(self.table)
            .select("*")
            .eq("project_id", project_id)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
        )
        if status:
            query = query.eq("status", status)
        return query.execute().data or []

    def list_by_researcher(self, wallet_address: str, limit: int = 50) -> List[dict]:
        res = (
            self.db.table(self.table)
            .select("*")
            .eq("researcher_address", wallet_address.lower())
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return res.data or []

    def update_status(self, bug_id: str, status: str, **kwargs) -> dict:
        payload = {"status": status, "updated_at": datetime.utcnow().isoformat(), **kwargs}
        res = (
            self.db.table(self.table)
            .update(payload)
            .eq("id", bug_id)
            .execute()
        )
        return res.data[0] if res.data else {}

    def update(self, bug_id: str, payload: dict) -> dict:
        payload["updated_at"] = datetime.utcnow().isoformat()
        res = (
            self.db.table(self.table)
            .update(payload)
            .eq("id", bug_id)
            .execute()
        )
        return res.data[0] if res.data else {}

    def count_by_researcher(self, wallet_address: str) -> int:
        res = (
            self.db.table(self.table)
            .select("id", count="exact")
            .eq("researcher_address", wallet_address.lower())
            .execute()
        )
        return res.count or 0
