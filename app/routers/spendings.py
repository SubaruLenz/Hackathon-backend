"""Spending management endpoints."""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.spending import SpendingCreate, SpendingResponse, SpendingUpdate
from app.schemas.visualization import SpendingVisualization
from app.services.spending_service import SpendingService

router = APIRouter(prefix="/spendings", tags=["spendings"])


@router.post("", response_model=SpendingResponse, status_code=status.HTTP_201_CREATED)
async def create_spending(
    spending: SpendingCreate,
    db: Session = Depends(get_db)
) -> SpendingResponse:
    """Create a new spending entry."""
    service = SpendingService(db)
    return service.create_spending(spending)


@router.get("", response_model=List[SpendingResponse])
async def get_spendings(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[SpendingResponse]:
    """Get all spendings, optionally filtered by category."""
    service = SpendingService(db)
    spendings = service.get_spendings(category=category)
    return spendings[skip:skip + limit]


@router.get("/{spending_id}", response_model=SpendingResponse)
async def get_spending(
    spending_id: UUID,
    db: Session = Depends(get_db)
) -> SpendingResponse:
    """Get a specific spending by ID."""
    service = SpendingService(db)
    spending = service.get_spending_by_id(spending_id)
    if not spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spending with id {spending_id} not found"
        )
    return spending


@router.put("/{spending_id}", response_model=SpendingResponse)
async def update_spending(
    spending_id: UUID,
    spending_update: SpendingUpdate,
    db: Session = Depends(get_db)
) -> SpendingResponse:
    """Update an existing spending entry."""
    service = SpendingService(db)
    updated_spending = service.update_spending(spending_id, spending_update)
    if not updated_spending:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spending with id {spending_id} not found"
        )
    return updated_spending


@router.delete("/{spending_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_spending(
    spending_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a spending entry."""
    service = SpendingService(db)
    deleted = service.delete_spending(spending_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spending with id {spending_id} not found"
        )


@router.get("/stats/summary")
async def get_spending_summary(
    date: Optional[date] = Query(None, description="Optional date to filter summary by (YYYY-MM-DD format)"),
    db: Session = Depends(get_db)
):
    """
    Get summary statistics of all spendings.
    
    - **date**: Optional date filter (YYYY-MM-DD format). If provided, returns summary for that specific date only.
    
    Returns summary statistics including total spendings, total amount, breakdown by category, and average amount.
    """
    service = SpendingService(db)
    date_filter = datetime.combine(date, datetime.min.time()) if date else None
    return service.get_summary(date=date_filter)


@router.get("/stats/visualization", response_model=SpendingVisualization)
async def get_spending_visualization(
    year: Optional[int] = None,
    month: Optional[int] = None,
    date: Optional[date] = Query(None, description="Optional date to filter by (YYYY-MM-DD format). Takes precedence over year/month."),
    db: Session = Depends(get_db)
):
    """
    Get categorized spending data with percentages for visualization.
    
    - **year**: Filter by year (e.g., 2025). Ignored if date is provided.
    - **month**: Filter by month (1-12). Requires year to be specified. Ignored if date is provided.
    - **date**: Optional date filter (YYYY-MM-DD format). If provided, takes precedence over year/month filters.
    
    Returns categorized spending with percentages suitable for charts and graphs.
    """
    if date is None:
        if month is not None and year is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Month filter requires year to be specified"
            )
        
        if month is not None and (month < 1 or month > 12):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Month must be between 1 and 12"
            )
    
    service = SpendingService(db)
    date_filter = datetime.combine(date, datetime.min.time()) if date else None
    return service.get_categorized_spending(year=year, month=month, date=date_filter)

