from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models.order import AppealMessage
from app.database.schemas.appeal_message import AppealMessageCreate, AppealMessageUpdate


class AppealMessageService(BaseService[AppealMessage, AppealMessageCreate, AppealMessageUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(AppealMessage, session)
