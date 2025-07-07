"""Application package for the management API."""

from .main import app


def create_app():
    """Return the FastAPI application instance."""
    return app


__all__ = ["app", "create_app"]
