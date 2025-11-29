"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Budget Tracker API"}


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

