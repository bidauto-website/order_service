from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ContainerBase(BaseModel):
    destination_id: int = Field(..., description="Delivery destination ID")
    ship_line: str = Field(default="Unknown", description="Shipping line")
    vessel: str = Field(default="Unknown", description="Vessel name")
    container_key: str = Field(..., min_length=1, description="Unique container identifier")


class ContainerCreate(ContainerBase):
    destination_name: str = Field(..., description="Delivery destination name")


class ContainerUpdate(BaseModel):
    destination_id: int | None = None
    destination_name: str | None = None
    ship_line: str | None = None
    vessel: str | None = None
    container_key: str | None = None


class ContainerRead(ContainerCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
