"""Service layer for spending business logic."""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.schemas.spending import SpendingCreate, SpendingResponse, SpendingUpdate
from app.storage.in_memory import storage


class SpendingService:
    """Service for managing spending operations."""

    @staticmethod
    def create_spending(spending_data: SpendingCreate) -> SpendingResponse:
        """Create a new spending entry."""
        new_spending = SpendingResponse(
            id=uuid4(),
            amount=spending_data.amount,
            category=spending_data.category,
            description=spending_data.description,
            date=spending_data.date or datetime.now(),
            created_at=datetime.now()
        )
        return storage.create(new_spending)

    @staticmethod
    def get_spendings(category: Optional[str] = None) -> List[SpendingResponse]:
        """Get all spendings, optionally filtered by category."""
        return storage.get_all(category=category)

    @staticmethod
    def get_spending_by_id(spending_id: UUID) -> Optional[SpendingResponse]:
        """Get a spending by ID."""
        return storage.get_by_id(spending_id)

    @staticmethod
    def update_spending(
        spending_id: UUID,
        spending_update: SpendingUpdate
    ) -> Optional[SpendingResponse]:
        """Update an existing spending entry."""
        existing_spending = storage.get_by_id(spending_id)
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
        return storage.update(spending_id, updated_spending)

    @staticmethod
    def delete_spending(spending_id: UUID) -> bool:
        """Delete a spending entry."""
        return storage.delete(spending_id)

    @staticmethod
    def get_summary() -> Dict:
        """Get summary statistics of all spendings."""
        all_spendings = storage.get_all_spendings()
        
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

