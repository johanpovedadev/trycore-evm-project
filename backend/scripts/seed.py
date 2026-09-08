"""Seed script to populate demo data."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base
from app.models.project import Project, Activity
from app.core.database import engine


def seed_database():
    """Seed the database with demo project and activities."""
    Base.metadata.create_all(bind=engine)

    db = Session(engine)

    project = Project(name="Proyecto Demo")
    db.add(project)
    db.flush()

    activities_data = [
        {
            "name": "Diseño",
            "bac": "10000",
            "planned_percentage": "60",
            "actual_percentage": "40",
            "actual_cost": "5000",
        },
        {
            "name": "Desarrollo",
            "bac": "20000",
            "planned_percentage": "50",
            "actual_percentage": "45",
            "actual_cost": "8000",
        },
        {
            "name": "Pruebas",
            "bac": "5000",
            "planned_percentage": "30",
            "actual_percentage": "20",
            "actual_cost": "2000",
        },
    ]

    for data in activities_data:
        activity = Activity(
            project_id=project.id,
            name=data["name"],
            bac=data["bac"],
            planned_percentage=data["planned_percentage"],
            actual_percentage=data["actual_percentage"],
            actual_cost=data["actual_cost"],
        )
        db.add(activity)

    db.commit()
    print(f"✅ Seeded project '{project.name}' with {len(activities_data)} activities")
    db.close()


if __name__ == "__main__":
    seed_database()
