"""Service for project business logic."""
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.evm_service import EVMService


class ProjectService:
    """Orchestrates project repository and EVM calculations."""

    @staticmethod
    def create(db: Session, project_create: ProjectCreate) -> ProjectResponse:
        """Create a new project."""
        project = ProjectRepository.create(db, project_create.name)
        return ProjectService._project_to_response(project)

    @staticmethod
    def get_by_id(db: Session, project_id: int) -> ProjectResponse:
        """Get project with consolidated EVM indicators."""
        project = ProjectRepository.get_by_id(db, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        return ProjectService._project_to_response(project)

    @staticmethod
    def list_all(db: Session) -> list[ProjectResponse]:
        """List all projects with consolidated indicators."""
        projects = ProjectRepository.list_all(db)
        return [ProjectService._project_to_response(p) for p in projects]

    @staticmethod
    def update(db: Session, project_id: int, project_update: ProjectUpdate) -> ProjectResponse:
        """Update project."""
        project = ProjectRepository.get_by_id(db, project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        update_data = project_update.model_dump(exclude_unset=True)
        project = ProjectRepository.update(db, project_id, **update_data)
        return ProjectService._project_to_response(project)

    @staticmethod
    def delete(db: Session, project_id: int) -> None:
        """Delete project."""
        if not ProjectRepository.delete(db, project_id):
            raise ValueError(f"Project {project_id} not found")

    @staticmethod
    def _project_to_response(project: Project) -> ProjectResponse:
        """Convert Project ORM to ProjectResponse with EVM indicators.

        Consolidates indicators from all activities.
        """
        from app.services.activity_service import ActivityService

        activity_responses = [
            ActivityService._activity_to_response(activity)
            for activity in project.activities
        ]

        evm_indicators_list = [a.indicators for a in activity_responses]
        consolidated = EVMService.consolidate_indicators(evm_indicators_list)

        return ProjectResponse(
            id=project.id,
            name=project.name,
            created_at=project.created_at,
            activities=activity_responses,
            indicators=consolidated,
        )
