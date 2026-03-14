from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from app.core.dependencies import get_current_wallet, get_db
from app.db.repositories.project_repository import ProjectRepository

router = APIRouter(prefix="/projects", tags=["projects"])


class CreateProjectPayload(BaseModel):
    name: str
    description: str
    scope: str
    bounty_pool_matic: float = 0.0
    max_severity: str = "critical"
    website_url: Optional[str] = None
    logo_url: Optional[str] = None


class UpdateProjectPayload(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scope: Optional[str] = None
    active: Optional[bool] = None
    website_url: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: CreateProjectPayload,
    wallet: str = Depends(get_current_wallet),
    db=Depends(get_db),
):
    repo = ProjectRepository(db)
    project = repo.create({
        "owner_address": wallet.lower(),
        "name": payload.name,
        "description": payload.description,
        "scope": payload.scope,
        "bounty_pool_matic": payload.bounty_pool_matic,
        "max_severity": payload.max_severity,
        "website_url": payload.website_url,
        "logo_url": payload.logo_url,
    })
    return {"message": "Project created.", "project": project}


@router.get("/")
async def list_projects(
    my_projects: bool = False,
    limit: int = 50,
    offset: int = 0,
    wallet: Optional[str] = Depends(get_current_wallet),
    db=Depends(get_db),
):
    repo = ProjectRepository(db)
    if my_projects and wallet:
        projects = repo.list_by_owner(wallet)
    else:
        projects = repo.list_active(limit=limit, offset=offset)
    return {"projects": projects, "total": len(projects)}


@router.get("/{project_id}")
async def get_project(project_id: str, db=Depends(get_db)):
    project = ProjectRepository(db).get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.patch("/{project_id}")
async def update_project(
    project_id: str,
    payload: UpdateProjectPayload,
    wallet: str = Depends(get_current_wallet),
    db=Depends(get_db),
):
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    if project["owner_address"] != wallet.lower():
        raise HTTPException(status_code=403, detail="Only the project owner can update it.")
    updated = repo.update(project_id, payload.dict(exclude_none=True))
    return {"message": "Project updated.", "project": updated}
