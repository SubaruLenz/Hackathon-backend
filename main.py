"""Main entry point for the Budget Tracker API.

This file imports the app from the app package for backward compatibility.
Run with: uvicorn main:app --reload
"""

from app.main import app

__all__ = ["app"]

