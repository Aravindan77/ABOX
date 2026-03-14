from typing import Optional, List
from supabase import Client
from datetime import datetime
import uuid


class ProjectRepository:
    """Data access layer for projects table."""

    def __init__(self, db: Client):
        self.db = db
        self.table = "projects"

    def create(self, data: dict) -> dict:
        data.setdefault("id", str(uuid.uuid4()))
        data.setdefault("created_at", datetime.utcnow().isoformat())
        data.setdefault("active", True)
        data.setdefault("total_bugs", 0)
        data.setdefault("resolved_bugs", 0)
        res = self.db.table(self.table).insert(data).execute()
        return res.data[0] if res.data else {}

    def get_by_id(self, project_id: str) -> Optional[dict]:
        res = (
            self.db.table(self.table)
            .select("*")
            .eq("id", project_id)
            .single()
            .execute()
        )
        return res.data

    def list_active(self, limit: int = 50, offset: int = 0) -> List[dict]:
        res = (
            self.db.table(self.table)
            .select("*")
            .eq("active", True)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return res.data or []

    def list_by_owner(self, owner_address: str) -> List[dict]:
        res = (
            self.db.table(self.table)
            .select("*")
            .eq("owner_address", owner_address.lower())
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []

    def update(self, project_id: str, payload: dict) -> dict:
        payload["updated_at"] = datetime.utcnow().isoformat()
        res = (
            self.db.table(self.table)
            .update(payload)
            .eq("id", project_id)
            .execute()
        )
        return res.data[0] if res.data else {}

    def increment_bug_count(self, project_id: str, resolved: bool = False) -> dict:
        project = self.get_by_id(project_id)
        if not project:
            return {}
        updates = {"total_bugs": (project.get("total_bugs") or 0) + 1}
        if resolved:
            updates["resolved_bugs"] = (project.get("resolved_bugs") or 0) + 1
        return self.update(project_id, updates)
