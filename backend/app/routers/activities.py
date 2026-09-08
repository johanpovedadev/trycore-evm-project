"""Router for activity endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter(tags=["activities"])


@router.post("/projects/{project_id}/activities", response_model=ActivityResponse, status_code=201)
async def create_activity(
    project_id: int, activity_create: ActivityCreate, db: Session = Depends(get_db)
) -> ActivityResponse:
    """Create a new activity for a project."""
    try:
        return ActivityService.create(db, project_id, activity_create)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/projects/{project_id}/activities", response_model=list[ActivityResponse])
async def list_activities(
    project_id: int, db: Session = Depends(get_db)
) -> list[ActivityResponse]:
    """List all activities for a project."""
    try:
        return ActivityService.list_by_project(db, project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/activities/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int, db: Session = Depends(get_db)
) -> ActivityResponse:
    """Get an activity with EVM indicators."""
    try:
        return ActivityService.get_by_id(db, activity_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")


@router.put("/activities/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int, activity_update: ActivityUpdate, db: Session = Depends(get_db)
) -> ActivityResponse:
    """Update an activity."""
    try:
        return ActivityService.update(db, activity_id, activity_update)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/activities/{activity_id}", status_code=204)
async def delete_activity(activity_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an activity."""
    try:
        ActivityService.delete(db, activity_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
