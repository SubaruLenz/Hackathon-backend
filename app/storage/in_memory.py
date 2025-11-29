"""In-memory storage implementation for spendings."""

from typing import List, Optional
from uuid import UUID

from app.schemas.spending import SpendingResponse


class InMemoryStorage:
    """In-memory storage for spendings (replace with database in production)."""

    def __init__(self):
        self._spendings: List[SpendingResponse] = []

    def create(self, spending: SpendingResponse) -> SpendingResponse:
        """Create a new spending entry."""
        self._spendings.append(spending)
        return spending

    def get_all(self, category: Optional[str] = None) -> List[SpendingResponse]:
        """Get all spendings, optionally filtered by category."""
        if category:
            return [
                s for s in self._spendings
                if s.category.lower() == category.lower()
            ]
        return self._spendings.copy()

    def get_by_id(self, spending_id: UUID) -> Optional[SpendingResponse]:
        """Get a spending by ID."""
        return next((s for s in self._spendings if s.id == spending_id), None)

    def update(self, spending_id: UUID, updated_spending: SpendingResponse) -> Optional[SpendingResponse]:
        """Update a spending entry."""
        spending_index = next(
            (i for i, s in enumerate(self._spendings) if s.id == spending_id),
            None
        )
        if spending_index is None:
            return None
        self._spendings[spending_index] = updated_spending
        return updated_spending

    def delete(self, spending_id: UUID) -> bool:
        """Delete a spending entry. Returns True if deleted, False if not found."""
        spending_index = next(
            (i for i, s in enumerate(self._spendings) if s.id == spending_id),
            None
        )
        if spending_index is None:
            return False
        self._spendings.pop(spending_index)
        return True

    def get_all_spendings(self) -> List[SpendingResponse]:
        """Get all spendings without filtering."""
        return self._spendings.copy()


# Global storage instance
storage = InMemoryStorage()

