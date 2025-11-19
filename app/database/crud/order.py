from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import Order
from app.database.schemas.order import OrderCreate, OrderUpdate


class OrderService(BaseService[Order, OrderCreate, OrderUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def exists_by_lot_id(self, lot_id: int) -> bool:
        query = select(Order.id).where(Order.lot_id == lot_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def exists_by_vin(self, vin: str) -> bool:
        query = select(Order.id).where(Order.vin == vin)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None


