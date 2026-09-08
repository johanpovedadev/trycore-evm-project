"""Repository for Activity CRUD operations."""
from sqlalchemy.orm import Session

from app.models.project import Activity


class ActivityRepository:
    """Data access for activities."""

    @staticmethod
    def create(
        db: Session,
        project_id: int,
        name: str,
        bac: str,
        planned_percentage: str,
        actual_percentage: str,
        actual_cost: str,
    ) -> Activity:
        """Create a new activity."""
        activity = Activity(
            project_id=project_id,
            name=name,
            bac=bac,
            planned_percentage=planned_percentage,
            actual_percentage=actual_percentage,
            actual_cost=actual_cost,
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def get_by_id(db: Session, activity_id: int) -> Activity | None:
        """Get activity by ID."""
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def list_by_project(db: Session, project_id: int) -> list[Activity]:
        """List activities for a project."""
        return db.query(Activity).filter(Activity.project_id == project_id).all()

    @staticmethod
    def update(
        db: Session,
        activity_id: int,
        name: str | None = None,
        bac: str | None = None,
        planned_percentage: str | None = None,
        actual_percentage: str | None = None,
        actual_cost: str | None = None,
    ) -> Activity | None:
        """Update an activity."""
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            if name is not None:
                activity.name = name
            if bac is not None:
                activity.bac = bac
            if planned_percentage is not None:
                activity.planned_percentage = planned_percentage
            if actual_percentage is not None:
                activity.actual_percentage = actual_percentage
            if actual_cost is not None:
                activity.actual_cost = actual_cost
            db.commit()
            db.refresh(activity)
        return activity

    @staticmethod
    def delete(db: Session, activity_id: int) -> bool:
        """Delete an activity."""
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            db.delete(activity)
            db.commit()
            return True
        return False
