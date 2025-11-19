import grpc.aio
from AuthTools.Permissions.dependencies import require_permissions
from fastapi import APIRouter, Depends, Body
from rfc9457 import NotFoundProblem, BadRequestProblem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.config import Permissions
from app.database.crud import OrderService
from app.database.db.session import get_async_db
from app.database.schemas import OrderCreate, OrderRead
from app.rpc_client.calculator import DetailedInfoService, CalculatorRpcClient
from app.schemas.order import OrderIn

router = APIRouter(prefix="/order", tags=["Orders"])


@router.post("/", response_model=OrderRead,
             description=f"Create order, required permissions: {Permissions.ORDER_ALL_WRITE.value}",
             dependencies=[Depends(require_permissions(Permissions.ORDER_ALL_WRITE))])
async def create_order(data: OrderIn = Body(...), db: AsyncSession = Depends(get_async_db)):
    order_service = OrderService(db)

    if await order_service.exists_by_lot_id(data.lot_id):
        raise BadRequestProblem("Order with this lot_id already exists")

    if await order_service.exists_by_vin(data.vin):
        raise BadRequestProblem("Order with this VIN already exists")

    async with CalculatorRpcClient() as calculator_client:
        try:
            calculator_data = await calculator_client.get_calculator_with_ids(
                price=data.vehicle_value,
                auction=data.auction,
                vehicle_type=data.vehicle_type,
                fee_type_id=data.fee_type_id,
                location_id=data.location_id,

            )

            print(calculator_data)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NotFoundProblem(e.details())
            raise BadRequestProblem(e.details())



    try:
        order = await order_service.create(
            OrderCreate(
                **data.model_dump(),
                location_name=calculator_data.location.name,
                location_city=calculator_data.location.city,
                location_state=calculator_data.location.state,
                location_postal_code=calculator_data.location.postal_code,
                terminal_name=calculator_data.terminal_name,
                fee_type_name=calculator_data.fee_type.fee_type
            )
        )
    except IntegrityError:
        await db.rollback()
        raise BadRequestProblem("Order already exists")

    return order
