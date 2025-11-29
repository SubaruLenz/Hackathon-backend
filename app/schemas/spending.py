"""Schemas for spending-related data transfer objects."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SpendingCreate(BaseModel):
    """DTO for creating a new spending entry."""

    amount: float = Field(..., gt=0, description="Amount spent (must be positive)")
    category: str = Field(..., min_length=1, description="Category of the spending")
    description: Optional[str] = Field(None, description="Optional description of the spending")
    date: Optional[datetime] = Field(default_factory=datetime.now, description="Date of the spending")


class SpendingUpdate(BaseModel):
    """DTO for updating an existing spending entry."""

    amount: Optional[float] = Field(None, gt=0, description="Amount spent (must be positive)")
    category: Optional[str] = Field(None, min_length=1, description="Category of the spending")
    description: Optional[str] = Field(None, description="Description of the spending")
    date: Optional[datetime] = Field(None, description="Date of the spending")


class SpendingResponse(BaseModel):
    """DTO for returning spending information."""

    id: UUID
    amount: float
    category: str
    description: Optional[str]
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

