"""Converters between ORM models and domain schemas."""
from decimal import Decimal

from app.models.project import Activity
from app.schemas.evm import EVMInput


def activity_to_evm_input(activity: Activity) -> EVMInput:
    """Convert Activity ORM model to EVMInput domain model.

    This is the explicit conversion point where database persistence
    becomes domain business logic.
    """
    return EVMInput(
        bac=Decimal(activity.bac),
        planned_percentage=Decimal(activity.planned_percentage),
        actual_percentage=Decimal(activity.actual_percentage),
        actual_cost=Decimal(activity.actual_cost),
    )
