"""Schemas for spending visualization data."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CategorySpending(BaseModel):
    """Spending data for a single category."""

    category: str = Field(..., description="Category name")
    amount: float = Field(..., description="Total amount spent in this category")
    percentage: float = Field(..., description="Percentage of total spending (0-100)")
    count: int = Field(..., description="Number of spending entries in this category")


class SpendingVisualization(BaseModel):
    """Visualization data for categorized spending."""

    total_amount: float = Field(..., description="Total amount of all spendings")
    total_count: int = Field(..., description="Total number of spending entries")
    year: Optional[int] = Field(None, description="Filter year (if applied)")
    month: Optional[int] = Field(None, description="Filter month (if applied)")
    categories: List[CategorySpending] = Field(
        ..., description="List of spending by category with percentages"
    )

