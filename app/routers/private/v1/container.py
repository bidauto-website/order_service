import grpc.aio
from AuthTools.Permissions.dependencies import require_permissions
from fastapi import APIRouter, Depends, Body
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel, Field
from rfc9457 import BadRequestProblem, NotFoundProblem
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Permissions
from app.core.utils import create_pagination_page
from app.database.crud import ContainerService
from app.database.db.session import get_async_db
from app.database.schemas import ContainerCreate, ContainerRead, ContainerUpdate
from app.rpc_client.calculator import DetailedInfoService
from app.schemas.container import ContainerIn

container_router = APIRouter(prefix="/container", tags=["Container"])
ContainersPage = create_pagination_page(ContainerRead)


class ContainerSearch(BaseModel):
    search: str | None = Field(None, description="Search by container key, destination name, ship line, vessel")


@container_router.post(
    "",
    response_model=ContainerRead,
    description=f"Create container, required permissions: {Permissions.CONTAINER_WRITE.value}",
    dependencies=[Depends(require_permissions(Permissions.CONTAINER_WRITE))],
)
async def create_container(
    data: ContainerIn = Body(...),
    db: AsyncSession = Depends(get_async_db),
):
    service = ContainerService(db)
    if await service.get_by_container_key(data.container_key):
        raise BadRequestProblem("Container with this key already exists")

    try:
        async with DetailedInfoService() as detailed_info_service:
            destination_detailed = await detailed_info_service.get_detailed_destination(destination_id=data.destination_id)
    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise NotFoundProblem("Destination not found")
        raise BadRequestProblem(e.details())
    try:
        return await service.create(ContainerCreate(**data.model_dump(), destination_name=destination_detailed.name))
    except IntegrityError:
        raise BadRequestProblem("This container already exists")


@container_router.put(
    "/{container_id}",
    response_model=ContainerRead,
    description=f"Update container, required permissions: {Permissions.CONTAINER_WRITE.value}",
    dependencies=[Depends(require_permissions(Permissions.CONTAINER_WRITE))],
)
async def update_container(
    container_id: int,
    data: ContainerUpdate = Body(...),
    db: AsyncSession = Depends(get_async_db),
):
    service = ContainerService(db)
    container = await service.get_with_not_found_exception(container_id, "Container")
    update_data = data.model_dump(exclude_unset=True)

    if "container_key" in update_data and update_data["container_key"] != container.container_key:
        if await service.get_by_container_key(update_data["container_key"]):
            raise BadRequestProblem("Container with this key already exists")

    if "destination_id" in update_data:
        try:
            async with DetailedInfoService() as detailed_info_service:
                destination_detailed = await detailed_info_service.get_detailed_destination(
                    destination_id=update_data["destination_id"]
                )
            update_data["destination_name"] = destination_detailed.name
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NotFoundProblem("Destination not found")
            raise BadRequestProblem(e.details())

    try:
        updated_container = await service.update(container_id, ContainerUpdate(**update_data))
    except IntegrityError:
        raise BadRequestProblem("This container already exists")

    if not updated_container:
        raise NotFoundProblem("Container not found")
    return updated_container


@container_router.get(
    "",
    response_model=ContainersPage,
    description=f"Get containers, required permissions: {Permissions.CONTAINER_READ.value}",
    dependencies=[Depends(require_permissions(Permissions.CONTAINER_READ))],
)
async def get_containers(
    params: ContainerSearch = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    service = ContainerService(db)
    stmt = await service.get_all_with_search(params.search)
    return await paginate(db, stmt)


@container_router.get(
    "/{container_id}",
    response_model=ContainerRead,
    description=f"Get container by id, required permissions: {Permissions.CONTAINER_READ.value}",
    dependencies=[Depends(require_permissions(Permissions.CONTAINER_READ))],
)
async def get_container(
    container_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    service = ContainerService(db)
    return await service.get_with_not_found_exception(container_id, "Container")
