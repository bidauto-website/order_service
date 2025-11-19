from pydantic import BaseModel, ConfigDict, Field


class InvoiceItemBase(BaseModel):
    name: str = Field(..., min_length=1, description="Название услуги/позиций")
    amount: int = Field(..., ge=0, description="Стоимость позиции в валюте инвойса")
    is_extra_fee: bool = Field(..., description="Флаг доплаты (extra fee)")
    order_id: int = Field(..., description="ID заказа, к которому относится позиция")


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemUpdate(BaseModel):
    name: str | None = None
    amount: int | None = None
    is_extra_fee: bool | None = None
    order_id: int | None = None


class InvoiceItemRead(InvoiceItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
