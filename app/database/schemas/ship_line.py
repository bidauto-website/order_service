from pydantic import BaseModel, ConfigDict, Field


class ShipLineBase(BaseModel):
    ship_line: str = Field(..., description="Ship line name")


class ShipLineCreate(ShipLineBase):
    pass


class ShipLineUpdate(BaseModel):
    ship_line: str | None = None


class ShipLineRead(ShipLineBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
