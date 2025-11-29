"""Service layer for spending business logic."""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.schemas.spending import SpendingCreate, SpendingResponse, SpendingUpdate
from app.schemas.visualization import CategorySpending, SpendingVisualization
from app.storage.database import DatabaseStorage


class SpendingService:
    """Service for managing spending operations."""

    def __init__(self, db: Session):
        self.storage = DatabaseStorage(db)

    def create_spending(self, spending_data: SpendingCreate) -> SpendingResponse:
        """Create a new spending entry."""
        new_spending = SpendingResponse(
            id=uuid4(),
            amount=spending_data.amount,
            category=spending_data.category,
            description=spending_data.description,
            date=spending_data.date or datetime.now(),
            created_at=datetime.now()
        )
        return self.storage.create(new_spending)

    def get_spendings(self, category: Optional[str] = None) -> List[SpendingResponse]:
        """Get all spendings, optionally filtered by category."""
        return self.storage.get_all(category=category)

    def get_spending_by_id(self, spending_id: UUID) -> Optional[SpendingResponse]:
        """Get a spending by ID."""
        return self.storage.get_by_id(spending_id)

    def update_spending(
        self,
        spending_id: UUID,
        spending_update: SpendingUpdate
    ) -> Optional[SpendingResponse]:
        """Update an existing spending entry."""
        existing_spending = self.storage.get_by_id(spending_id)
        if not existing_spending:
            return None

        update_data = spending_update.model_dump(exclude_unset=True)
        updated_spending = SpendingResponse(
            id=existing_spending.id,
            amount=update_data.get("amount", existing_spending.amount),
            category=update_data.get("category", existing_spending.category),
            description=update_data.get("description", existing_spending.description),
            date=update_data.get("date", existing_spending.date),
            created_at=existing_spending.created_at
        )
        return self.storage.update(spending_id, updated_spending)

    def delete_spending(self, spending_id: UUID) -> bool:
        """Delete a spending entry."""
        return self.storage.delete(spending_id)

    def get_summary(self) -> Dict:
        """Get summary statistics of all spendings."""
        all_spendings = self.storage.get_all_spendings()
        
        if not all_spendings:
            return {
                "total_spendings": 0,
                "total_amount": 0.0,
                "by_category": {},
                "average_amount": 0.0
            }

        total_amount = sum(s.amount for s in all_spendings)
        category_totals: Dict[str, float] = {}
        for spending in all_spendings:
            category_totals[spending.category] = (
                category_totals.get(spending.category, 0) + spending.amount
            )

        return {
            "total_spendings": len(all_spendings),
            "total_amount": total_amount,
            "by_category": category_totals,
            "average_amount": total_amount / len(all_spendings)
        }

    def get_categorized_spending(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> SpendingVisualization:
        """
        Calculate categorized spending with percentages for visualization.
        
        Args:
            year: Optional year filter (e.g., 2025)
            month: Optional month filter (1-12)
            
        Returns:
            SpendingVisualization with categorized data and percentages
        """
        # Get filtered spendings
        spendings = self.storage.get_spendings_by_date_range(year=year, month=month)
        
        if not spendings:
            return SpendingVisualization(
                total_amount=0.0,
                total_count=0,
                year=year,
                month=month,
                categories=[]
            )

        # Calculate totals
        total_amount = sum(s.amount for s in spendings)
        total_count = len(spendings)

        # Group by category and calculate totals
        category_data: Dict[str, Dict[str, float]] = {}
        for spending in spendings:
            if spending.category not in category_data:
                category_data[spending.category] = {"amount": 0.0, "count": 0}
            category_data[spending.category]["amount"] += spending.amount
            category_data[spending.category]["count"] += 1

        # Create category spending list with percentages
        categories = []
        for category, data in sorted(category_data.items(), key=lambda x: x[1]["amount"], reverse=True):
            percentage = (data["amount"] / total_amount * 100) if total_amount > 0 else 0.0
            categories.append(
                CategorySpending(
                    category=category,
                    amount=round(data["amount"], 2),
                    percentage=round(percentage, 2),
                    count=data["count"]
                )
            )

        return SpendingVisualization(
            total_amount=round(total_amount, 2),
            total_count=total_count,
            year=year,
            month=month,
            categories=categories
        )

