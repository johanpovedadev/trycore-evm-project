"""Service for activity business logic."""

from sqlalchemy.orm import Session

from app.core.converters import activity_to_evm_input
from app.models.project import Activity
from app.repositories.activity_repository import ActivityRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.evm_service import EVMService


class ActivityService:
    """Orchestrates activity repository and EVM calculations."""

    @staticmethod
    def create(db: Session, project_id: int, activity_create: ActivityCreate) -> ActivityResponse:
        """Create a new activity for a project."""
        project = ProjectRepository.get_by_id(db, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        activity = ActivityRepository.create(
            db,
            project_id=project_id,
            name=activity_create.name,
            bac=str(activity_create.bac),
            planned_percentage=str(activity_create.planned_percentage),
            actual_percentage=str(activity_create.actual_percentage),
            actual_cost=str(activity_create.actual_cost),
        )
        return ActivityService._activity_to_response(activity)

    @staticmethod
    def get_by_id(db: Session, activity_id: int) -> ActivityResponse:
        """Get activity with EVM indicators."""
        activity = ActivityRepository.get_by_id(db, activity_id)
        if not activity:
            raise ValueError(f"Activity {activity_id} not found")
        return ActivityService._activity_to_response(activity)

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[ActivityResponse]:
        """List activities for a project."""
        project = ProjectRepository.get_by_id(db, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        activities = ActivityRepository.list_by_project(db, project_id)
        return [ActivityService._activity_to_response(a) for a in activities]

    @staticmethod
    def update(db: Session, activity_id: int, activity_update: ActivityUpdate) -> ActivityResponse:
        """Update an activity."""
        activity = ActivityRepository.get_by_id(db, activity_id)
        if not activity:
            raise ValueError(f"Activity {activity_id} not found")

        update_data = activity_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(activity, key, str(value) if key in ["bac", "planned_percentage", "actual_percentage", "actual_cost"] else value)

        db.commit()
        db.refresh(activity)
        return ActivityService._activity_to_response(activity)

    @staticmethod
    def delete(db: Session, activity_id: int) -> None:
        """Delete an activity."""
        if not ActivityRepository.delete(db, activity_id):
            raise ValueError(f"Activity {activity_id} not found")

    @staticmethod
    def _activity_to_response(activity: Activity) -> ActivityResponse:
        """Convert Activity ORM to ActivityResponse with EVM indicators.

        Uses EVMService for calculations (never duplicates logic).
        """
        evm_input = activity_to_evm_input(activity)
        indicators = EVMService.calculate_indicators(evm_input)

        return ActivityResponse(
            id=activity.id,
            project_id=activity.project_id,
            name=activity.name,
            bac=float(activity.bac),
            planned_percentage=float(activity.planned_percentage),
            actual_percentage=float(activity.actual_percentage),
            actual_cost=float(activity.actual_cost),
            created_at=activity.created_at,
            updated_at=activity.updated_at,
            indicators=indicators,
        )
