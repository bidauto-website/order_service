from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.enums.auction import AuctionEnum
from app.enums.order import InvoiceTypeEnum, OrderStatusEnum


class OrderBase(BaseModel):
    auction: AuctionEnum | None = Field(default=None, description="Аукцион-источник")
    order_date: datetime | None = Field(
        default=None,
        description="Дата создания заказа (если не указанa, БД выставит текущее время)",
    )
    lot_id: int = Field(..., description="Идентификатор лота")
    vehicle_value: int = Field(..., ge=0, description="Стоимость автомобиля")
    invoice_type: InvoiceTypeEnum = Field(
        default=InvoiceTypeEnum.NAVI_GRUPE_INVOICE,
        description="Тип инвойса",
    )
    vehicle_type: str = Field(default="CAR", description="Тип ТС")
    vin: str = Field(..., min_length=1, description="VIN транспортного средства")
    vehicle_name: str = Field(..., min_length=1, description="Модель/название автомобиля")
    keys: bool = Field(default=False, description="Есть ключи")
    damage: bool = Field(default=False, description="ТС повреждено")
    color: str = Field(default="Unknown", description="Цвет ТС")
    auto_generated: bool = Field(default=False, description="Заказ создан автоматически")
    fee_type: str = Field(..., description="Название типа комиссии")
    delivery_status: OrderStatusEnum = Field(
        default=OrderStatusEnum.PENDING_PAYMENT,
        description="Статус доставки",
    )

    location_id: int = Field(..., description="ID локации")
    location_name: str = Field(..., description="Название локации")
    location_city: str | None = Field(default=None, description="Город локации")
    location_state: str | None = Field(default=None, description="Штат/регион локации")
    location_postal_code: str | None = Field(
        default=None,
        description="Почтовый индекс локации",
    )

    terminal_id: int = Field(..., description="ID терминала")
    terminal_name: str = Field(..., description="Название терминала")
    fee_type_id: int = Field(..., description="ID типа комиссии")
    fee_type_name: str = Field(..., description="Название типа комиссии из калькулятора")

    container_id: int | None = Field(default=None, description="ID контейнера (если привязан)")
    user_uuid: str = Field(..., description="UUID пользователя, создавшего заказ")


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    auction: AuctionEnum | None = None
    order_date: datetime | None = None
    lot_id: int | None = None
    vehicle_value: int | None = None
    invoice_type: InvoiceTypeEnum | None = None
    vehicle_type: str | None = None
    vin: str | None = None
    vehicle_name: str | None = None
    keys: bool | None = None
    damage: bool | None = None
    color: str | None = None
    auto_generated: bool | None = None
    fee_type: str | None = None
    delivery_status: OrderStatusEnum | None = None

    location_id: int | None = None
    location_name: str | None = None
    location_city: str | None = None
    location_state: str | None = None
    location_postal_code: str | None = None

    terminal_id: int | None = None
    terminal_name: str | None = None
    fee_type_id: int | None = None
    fee_type_name: str | None = None

    container_id: int | None = None
    user_uuid: str | None = None


class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
