import grpc.aio
from AuthTools.Permissions.dependencies import require_permissions
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from rfc9457 import NotFoundProblem, BadRequestProblem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_pagination.ext.sqlalchemy import paginate
from app.config import Permissions
from app.core.utils import get_cheapest_terminal_prices, create_pagination_page
from app.database.crud import OrderService
from app.database.db.session import get_async_db
from app.database.schemas import OrderCreate, OrderRead, InvoiceItemCreate
from app.rpc_client.auth import AuthRpcClient
from app.rpc_client.calculator import CalculatorRpcClient
from app.rpc_client.gen.python.calculator.v1.calculator_pb2 import CalculatorOut, City
from app.schemas.order import OrderIn

order_router = APIRouter(prefix="/order", tags=["Orders"])


@order_router.post("", response_model=OrderRead,
             description=f"Create order, required permissions: {Permissions.ORDER_ALL_WRITE.value}",
             dependencies=[Depends(require_permissions(Permissions.ORDER_ALL_WRITE))])
async def create_order(data: OrderIn = Body(...), db: AsyncSession = Depends(get_async_db)):
    order_service = OrderService(db)

    if await order_service.exists_by_lot_id(data.lot_id):
        raise BadRequestProblem("Order with this lot_id already exists")

    if await order_service.exists_by_vin(data.vin):
        raise BadRequestProblem("Order with this VIN already exists")

    async with AuthRpcClient() as auth_client:
        try:
            await auth_client.get_user(data.user_uuid)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise NotFoundProblem(e.details())
            raise BadRequestProblem(e.details())

    async with CalculatorRpcClient() as calculator_client:
        try:
            calculator_data = await calculator_client.get_calculator_with_ids(
                price=data.vehicle_value,
                auction=data.auction,
                vehicle_type=data.vehicle_type,
                fee_type_id=data.fee_type_id,
                location_id=data.location_id,

            )
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
            ), flush=True
        )
        default_calculator = calculator_data.calculator.calculator
        items = [
            InvoiceItemCreate(
                name=f'{data.vehicle_name} ({data.vin})',
                amount=data.vehicle_value,
                order_id=order.id,
            ),
            InvoiceItemCreate(name='Broker Fee', amount=default_calculator.broker_fee, order_id=order.id),
        ]
        items.extend(
            InvoiceItemCreate(name=fee.name, amount=fee.price, order_id=order.id)
            for fee in default_calculator.additional.fees
            if fee.price
        )

        cheapest_terminal = get_cheapest_terminal_prices(default_calculator)
        if cheapest_terminal:
            transportation_city, ocean_city = cheapest_terminal
            terminal_name = transportation_city.name
            items.append(
                InvoiceItemCreate(
                    name=f"Transportation ({terminal_name})",
                    amount=transportation_city.price,
                    order_id=order.id,
                )
            )
            items.append(
                InvoiceItemCreate(
                    name=f"Ocean Shipping ({terminal_name})",
                    amount=ocean_city.price,
                    order_id=order.id,
                )
            )

        await order_service.create_invoice_items_batch(order.id, items)

        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise BadRequestProblem("Order already exists")
    return order

OrdersPage = create_pagination_page(OrderRead)

class OrderSearch(BaseModel):
    search: str | None = None

@order_router.get(
    '',
    response_model=OrdersPage,
    description=f"Get all orders, required permissions: {Permissions.ORDER_ALL_READ.value}",
    dependencies=[Depends(require_permissions(Permissions.ORDER_ALL_READ))]
)
async def get_orders(data: OrderSearch = Depends(), db: AsyncSession = Depends(get_async_db)):
    order_service = OrderService(db)
    smtp = await order_service.get_all_with_search(data.search)
    return await paginate(db, smtp)



