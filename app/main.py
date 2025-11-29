"""Main FastAPI application."""

from fastapi import FastAPI

from app.routers import health, spendings

app = FastAPI(
    title="Budget Tracker API",
    description="A FastAPI application for tracking budget and spendings",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(spendings.router)

