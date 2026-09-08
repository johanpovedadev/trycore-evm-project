"""Repository for Project CRUD operations."""
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    """Data access for projects."""

    @staticmethod
    def create(db: Session, name: str) -> Project:
        """Create a new project."""
        project = Project(name=name)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_by_id(db: Session, project_id: int) -> Project | None:
        """Get project by ID."""
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def list_all(db: Session) -> list[Project]:
        """List all projects."""
        return db.query(Project).all()

    @staticmethod
    def update(db: Session, project_id: int, name: str) -> Project | None:
        """Update project name."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.name = name
            db.commit()
            db.refresh(project)
        return project

    @staticmethod
    def delete(db: Session, project_id: int) -> bool:
        """Delete project."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            db.delete(project)
            db.commit()
            return True
        return False
