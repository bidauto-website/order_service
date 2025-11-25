from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import Container
from app.database.schemas.container import ContainerCreate, ContainerUpdate


class ContainerService(BaseService[Container, ContainerCreate, ContainerUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Container, session)

    async def get_by_container_key(self, container_key: str) -> Container | None:
        stmt = select(Container).where(Container.container_key == container_key)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_with_search(
        self,
        search: str | None = None,
        get_stmt: bool = True,
    ):
        stmt = (
            select(Container).where(
                or_(
                    Container.container_key.ilike(f"%{search}%"),
                    Container.destination_name.ilike(f"%{search}%"),
                    Container.ship_line.ilike(f"%{search}%"),
                    Container.vessel.ilike(f"%{search}%"),
                )
            )
            if search
            else select(Container)
        )
        if get_stmt:
            return stmt
        result = await self.session.execute(stmt)
        return result.scalars().all()
