from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import OrderDepthVideo
from app.database.schemas.order_depth_video import OrderDepthVideoCreate, OrderDepthVideoUpdate


class OrderDepthVideoService(BaseService[OrderDepthVideo, OrderDepthVideoCreate, OrderDepthVideoUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(OrderDepthVideo, session)
