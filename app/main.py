"""Main FastAPI application."""

from fastapi import FastAPI

from app.database import init_db
from app.models import Spending  # noqa: F401 - Import to register models
from app.routers import health, spendings

app = FastAPI(
    title="Budget Tracker API",
    description="A FastAPI application for tracking budget and spendings",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()


# Include routers
app.include_router(health.router)
app.include_router(spendings.router)

