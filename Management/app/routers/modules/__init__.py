"""Routers for agent modules."""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user

from .collection import router as collection_router
from .execution import router as execution_router

router = APIRouter(
    prefix="/agents/{agent_id}/modules",
    tags=["modules"],
    dependencies=[Depends(get_current_user)],
)

router.include_router(execution_router, prefix="/execution")
router.include_router(collection_router, prefix="/collection")

__all__ = ["router"]
