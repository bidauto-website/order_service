from fastapi import APIRouter

from app.routers.private.v1 import container, orders, ship_lines

router = APIRouter(prefix="/v1")
router.include_router(orders.order_router)
router.include_router(ship_lines.ship_lines_router)
router.include_router(container.container_router)

__all__ = ["router"]
