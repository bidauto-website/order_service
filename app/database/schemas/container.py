from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ContainerBase(BaseModel):
    destination_id: int = Field(..., description="ID направления доставки")
    destination_name: str = Field(..., description="Название направления доставки")
    ship_line: str = Field(default="Unknown", description="Судоходная линия")
    vessel: str = Field(default="Unknown", description="Судно")
    container_key: str = Field(..., min_length=1, description="Уникальный идентификатор контейнера")


class ContainerCreate(ContainerBase):
    pass


class ContainerUpdate(BaseModel):
    destination_id: int | None = None
    destination_name: str | None = None
    ship_line: str | None = None
    vessel: str | None = None
    container_key: str | None = None


class ContainerRead(ContainerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
