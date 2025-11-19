from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import Container
from app.database.schemas.container import ContainerCreate, ContainerUpdate


class ContainerService(BaseService[Container, ContainerCreate, ContainerUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Container, session)
