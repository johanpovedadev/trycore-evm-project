from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.evm import EVMIndicators


class ActivityBase(BaseModel):
    """Base activity schema."""

    name: str = Field(..., min_length=1, max_length=255)
    bac: float = Field(..., gt=0, description="Budget at Completion")
    planned_percentage: float = Field(
        ..., ge=0, le=100, description="Planned progress (0-100%)"
    )
    actual_percentage: float = Field(
        ..., ge=0, le=100, description="Actual progress (0-100%)"
    )
    actual_cost: float = Field(..., ge=0, description="Actual cost incurred")


class ActivityCreate(ActivityBase):
    """Schema for creating an activity."""

    pass


class ActivityUpdate(BaseModel):
    """Schema for updating an activity (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bac: Optional[float] = Field(None, gt=0)
    planned_percentage: Optional[float] = Field(None, ge=0, le=100)
    actual_percentage: Optional[float] = Field(None, ge=0, le=100)
    actual_cost: Optional[float] = Field(None, ge=0)


class ActivityResponse(ActivityBase):
    """Activity response including EVM indicators."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    indicators: EVMIndicators


class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=255)


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)


class ProjectResponse(ProjectBase):
    """Project response with activities and consolidated EVM indicators."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    activities: list[ActivityResponse]
    indicators: EVMIndicators
