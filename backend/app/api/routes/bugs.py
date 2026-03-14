from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import Optional, List
import uuid

from app.core.dependencies import get_current_wallet, get_db
from app.db.repositories.bug_repository import BugRepository
from app.db.repositories.project_repository import ProjectRepository
from app.db.repositories.user_repository import UserRepository
from app.services.ipfs_service import ipfs_service
from app.services.reputation_engine import recalculate_for_user, get_trust_tier

router = APIRouter(prefix="/bugs", tags=["bugs"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def submit_bug(
    project_id: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    severity: str = Form(...),
    steps_to_reproduce: str = Form(...),
    expected_behavior: str = Form(default=""),
    actual_behavior: str = Form(default=""),
    evidence_file: Optional[UploadFile] = File(default=None),
    wallet: str = Depends(get_current_wallet),
    db=Depends(get_db),
):
    bug_repo = BugRepository(db)
    project_repo = ProjectRepository(db)

    project = project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    # Upload evidence to IPFS
    ipfs_cid = None
    if evidence_file:
        file_bytes = await evidence_file.read()
        ipfs_cid = await ipfs_service.upload_file(file_bytes, evidence_file.filename)

    bug = bug_repo.create({
        "project_id": project_id,
        "researcher_address": wallet.lower(),
        "title": title,
        "description": description,
        "severity": severity,
        "steps_to_reproduce": steps_to_reproduce,
        "expected_behavior": expected_behavior,
        "actual_behavior": actual_behavior,
        "ipfs_cid": ipfs_cid,
        "status": "pending",
    })

    project_repo.increment_bug_count(project_id)
    return {"message": "Bug report submitted successfully.", "bug": bug}


@router.get("/")
async def list_bugs(
    project_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    wallet: Optional[str] = Depends(get_current_wallet),
    db=Depends(get_db),
):
    bug_repo = BugRepository(db)
    if project_id:
        bugs = bug_repo.list_by_project(project_id, status=status_filter)
    else:
        bugs = bug_repo.list_by_researcher(wallet)
    return {"bugs": bugs, "total": len(bugs)}


@router.get("/{bug_id}")
async def get_bug(bug_id: str, wallet: str = Depends(get_current_wallet), db=Depends(get_db)):
    bug = BugRepository(db).get_by_id(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug report not found.")
    if bug["researcher_address"] != wallet.lower():
        raise HTTPException(status_code=403, detail="Access denied.")
    return bug


@router.patch("/{bug_id}/status")
async def update_bug_status(
    bug_id: str,
    new_status: str,
    reason: Optional[str] = None,
    bounty_amount: Optional[float] = None,
    wallet: str = Depends(get_current_wallet),
    db=Depends(get_db),
):
    allowed = {"pending", "approved", "rejected", "spam", "human_review", "paid"}
    if new_status not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {allowed}")

    bug_repo = BugRepository(db)
    bug = bug_repo.get_by_id(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found.")

    updates: dict = {"status": new_status}
    if reason:
        updates["review_notes"] = reason
    if bounty_amount is not None:
        updates["bounty_amount"] = bounty_amount

    updated = bug_repo.update(bug_id, updates)

    # Recalculate researcher trust score
    researcher = bug["researcher_address"]
    user_repo = UserRepository(db)
    history = bug_repo.list_by_researcher(researcher, limit=200)
    new_score = recalculate_for_user({}, history)
    user_repo.update_trust_score(researcher, new_score)

    return {"message": "Bug status updated.", "bug": updated, "new_trust_score": new_score}
