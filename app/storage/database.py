"""Database storage implementation for spendings."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.spending import Spending
from app.schemas.spending import SpendingResponse


class DatabaseStorage:
    """Database storage for spendings."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, spending: SpendingResponse) -> SpendingResponse:
        """Create a new spending entry."""
        db_spending = Spending(
            id=str(spending.id),
            amount=spending.amount,
            category=spending.category,
            description=spending.description,
            date=spending.date,
            created_at=spending.created_at
        )
        self.db.add(db_spending)
        self.db.commit()
        self.db.refresh(db_spending)
        return self._to_response(db_spending)

    def get_all(self, category: Optional[str] = None) -> List[SpendingResponse]:
        """Get all spendings, optionally filtered by category."""
        query = self.db.query(Spending)
        if category:
            query = query.filter(Spending.category.ilike(f"%{category}%"))
        db_spendings = query.order_by(Spending.date.desc()).all()
        return [self._to_response(s) for s in db_spendings]

    def get_by_id(self, spending_id: UUID) -> Optional[SpendingResponse]:
        """Get a spending by ID."""
        db_spending = self.db.query(Spending).filter(Spending.id == str(spending_id)).first()
        if not db_spending:
            return None
        return self._to_response(db_spending)

    def update(self, spending_id: UUID, updated_spending: SpendingResponse) -> Optional[SpendingResponse]:
        """Update a spending entry."""
        db_spending = self.db.query(Spending).filter(Spending.id == str(spending_id)).first()
        if not db_spending:
            return None

        db_spending.amount = updated_spending.amount
        db_spending.category = updated_spending.category
        db_spending.description = updated_spending.description
        db_spending.date = updated_spending.date

        self.db.commit()
        self.db.refresh(db_spending)
        return self._to_response(db_spending)

    def delete(self, spending_id: UUID) -> bool:
        """Delete a spending entry. Returns True if deleted, False if not found."""
        db_spending = self.db.query(Spending).filter(Spending.id == str(spending_id)).first()
        if not db_spending:
            return False
        self.db.delete(db_spending)
        self.db.commit()
        return True

    def get_all_spendings(self) -> List[SpendingResponse]:
        """Get all spendings without filtering."""
        db_spendings = self.db.query(Spending).order_by(Spending.date.desc()).all()
        return [self._to_response(s) for s in db_spendings]

    def get_spendings_by_date_range(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> List[SpendingResponse]:
        """Get spendings filtered by year and/or month."""
        from sqlalchemy import extract
        from datetime import datetime

        query = self.db.query(Spending)

        if year is not None:
            query = query.filter(extract('year', Spending.date) == year)
        if month is not None:
            query = query.filter(extract('month', Spending.date) == month)

        db_spendings = query.order_by(Spending.date.desc()).all()
        return [self._to_response(s) for s in db_spendings]

    def get_spendings_by_date(self, date: datetime) -> List[SpendingResponse]:
        """Get spendings filtered by a specific date."""
        from sqlalchemy import func

        # Filter by date (ignoring time component)
        target_date = date.date() if isinstance(date, datetime) else date
        query = self.db.query(Spending).filter(
            func.date(Spending.date) == target_date
        )
        db_spendings = query.order_by(Spending.date.desc()).all()
        return [self._to_response(s) for s in db_spendings]

    @staticmethod
    def _to_response(db_spending: Spending) -> SpendingResponse:
        """Convert database model to response schema."""
        return SpendingResponse(
            id=UUID(db_spending.id),
            amount=db_spending.amount,
            category=db_spending.category,
            description=db_spending.description,
            date=db_spending.date,
            created_at=db_spending.created_at
        )

