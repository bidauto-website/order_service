from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import Order
from app.database.schemas.order import OrderCreate, OrderUpdate


class OrderService(BaseService[Order, OrderCreate, OrderUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)
