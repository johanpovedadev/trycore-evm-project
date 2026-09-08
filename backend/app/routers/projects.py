"""Router for project endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_create: ProjectCreate, db: Session = Depends(get_db)
) -> ProjectResponse:
    """Create a new project."""
    try:
        return ProjectService.create(db, project_create)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=list[ProjectResponse])
async def list_projects(db: Session = Depends(get_db)) -> list[ProjectResponse]:
    """List all projects with consolidated EVM indicators."""
    return ProjectService.list_all(db)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int, db: Session = Depends(get_db)
) -> ProjectResponse:
    """Get a project with its activities and consolidated EVM indicators."""
    try:
        return ProjectService.get_by_id(db, project_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)
) -> ProjectResponse:
    """Update a project."""
    try:
        return ProjectService.update(db, project_id, project_update)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a project."""
    try:
        ProjectService.delete(db, project_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
