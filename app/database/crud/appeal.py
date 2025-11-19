from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import Appeal
from app.database.schemas.appeal import AppealCreate, AppealUpdate


class AppealService(BaseService[Appeal, AppealCreate, AppealUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Appeal, session)
