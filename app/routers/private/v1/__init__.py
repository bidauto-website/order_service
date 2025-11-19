from fastapi import APIRouter

from app.routers.private.v1 import orders

router = APIRouter(prefix="/v1")
router.include_router(orders.router)

__all__ = ["router"]
