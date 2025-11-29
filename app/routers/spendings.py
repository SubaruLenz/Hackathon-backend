"""Spending management endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.spending import SpendingCreate, SpendingResponse, SpendingUpdate
from app.services.spending_service import SpendingService

router = APIRouter(prefix="/spendings", tags=["spendings"])

spending_service = SpendingService()


@router.post("", response_model=SpendingResponse, status_code=status.HTTP_201_CREATED)
async def create_spending(spending: SpendingCreate) -> SpendingResponse:
    """Create a new spending entry."""
    return spending_service.create_spending(spending)


@router.get("", response_model=List[SpendingResponse])
async def get_spendings(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[SpendingResponse]:
    """Get all spendings, optionally filtered by category."""
    spendings = spending_service.get_spendings(category=category)
    return spendings[skip:skip + limit]


@router.get("/{spending_id}", response_model=SpendingResponse)
async def get_spending(spending_id: UUID) -> SpendingResponse:
    """Get a specific spending by ID."""
    spending = spending_service.get_spending_by_id(spending_id)
    if not spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spending with id {spending_id} not found"
        )
    return spending


@router.put("/{spending_id}", response_model=SpendingResponse)
async def update_spending(
    spending_id: UUID,
    spending_update: SpendingUpdate
) -> SpendingResponse:
    """Update an existing spending entry."""
    updated_spending = spending_service.update_spending(spending_id, spending_update)
    if not updated_spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spending with id {spending_id} not found"
        )
    return updated_spending


@router.delete("/{spending_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_spending(spending_id: UUID):
    """Delete a spending entry."""
    deleted = spending_service.delete_spending(spending_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spending with id {spending_id} not found"
        )


@router.get("/stats/summary")
async def get_spending_summary():
    """Get summary statistics of all spendings."""
    return spending_service.get_summary()

