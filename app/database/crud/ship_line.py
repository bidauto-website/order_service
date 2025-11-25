from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.ship_line import ShipLine
from app.database.schemas.ship_line import ShipLineCreate, ShipLineUpdate


class ShipLineService(BaseService[ShipLine, ShipLineCreate, ShipLineUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(ShipLine, session)

    async def get_by_link(self, link: str) -> ShipLine | None:
        stmt = select(ShipLine).where(ShipLine.ship_line == link)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_with_search(
        self,
        search: str | None = None,
        get_stmt: bool = True,
    ):
        stmt = (
            select(ShipLine).where(ShipLine.ship_line.ilike(f"%{search}%"))
            if search
            else select(ShipLine)
        )
        if get_stmt:
            return stmt
        result = await self.session.execute(stmt)
        return result.scalars().all()
