from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EVMInput(BaseModel):
    """Input data for EVM calculations (independent of persistence)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    bac: Decimal = Field(..., gt=0, description="Budget At Completion")
    planned_percentage: Decimal = Field(
        ..., ge=0, le=100, description="Planned progress (0-100%)"
    )
    actual_percentage: Decimal = Field(
        ..., ge=0, le=100, description="Actual progress (0-100%)"
    )
    actual_cost: Decimal = Field(..., ge=0, description="Actual cost incurred")

    @field_validator("bac", mode="before")
    @classmethod
    def convert_bac(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v

    @field_validator("planned_percentage", "actual_percentage", mode="before")
    @classmethod
    def convert_percentages(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v

    @field_validator("actual_cost", mode="before")
    @classmethod
    def convert_cost(cls, v):
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v


class EVMIndicators(BaseModel):
    """EVM indicators calculated from input data."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_encoders={Decimal: str},
    )

    bac: Decimal
    pv: Decimal
    ev: Decimal
    ac: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Optional[Decimal] = None
    spi: Optional[Decimal] = None
    eac: Optional[Decimal] = None
    vac: Optional[Decimal] = None


class EVMActivityResponse(BaseModel):
    """Response model for activity with EVM indicators."""

    model_config = ConfigDict(str_strip_whitespace=True)

    activity_id: Optional[int] = None
    name: Optional[str] = None
    indicators: EVMIndicators


class EVMProjectResponse(BaseModel):
    """Response model for project consolidated EVM indicators."""

    model_config = ConfigDict(str_strip_whitespace=True)

    project_id: Optional[int] = None
    name: Optional[str] = None
    total_activities: int
    indicators: EVMIndicators
