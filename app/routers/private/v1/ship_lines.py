from AuthTools.Permissions.dependencies import require_permissions
from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from rfc9457 import BadRequestProblem
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Permissions
from app.core.utils import create_pagination_page
from app.database.crud import ShipLineService
from app.database.db.session import get_async_db
from app.database.schemas import ShipLineCreate, ShipLineRead

ship_lines_router = APIRouter(prefix='/ship-lines', tags=['Ship Lines'])
ShipLinesPage = create_pagination_page(ShipLineRead)

class ShipLineSearch(BaseModel):
    search: str | None = None


@ship_lines_router.post('',
                        description=f'Create ship line: {Permissions.SHIP_LINE_WRITE.value}',
                        dependencies=[Depends(require_permissions(Permissions.SHIP_LINE_WRITE))]
                        )
async def create_ship_line(data: ShipLineCreate = Depends(), db: AsyncSession = Depends(get_async_db)):
    service = ShipLineService(db)
    if await service.get_by_link(data.ship_line):
        raise BadRequestProblem("Ship line with this link already exists")
    return await service.create(data)


@ship_lines_router.get(
    '',
    response_model=ShipLinesPage,
    description=f"Get ship lines, required permissions: {Permissions.SHIP_LINE_READ.value}",
    dependencies=[Depends(require_permissions(Permissions.SHIP_LINE_READ))]
)
async def get_ship_lines(
    data: ShipLineSearch = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    service = ShipLineService(db)
    stmt = await service.get_all_with_search(data.search)
    return await paginate(db, stmt)

