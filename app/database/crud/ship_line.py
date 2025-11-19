from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.ship_line import ShipLine
from app.database.schemas.ship_line import ShipLineCreate, ShipLineUpdate


class ShipLineService(BaseService[ShipLine, ShipLineCreate, ShipLineUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(ShipLine, session)
