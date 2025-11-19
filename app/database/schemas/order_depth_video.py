from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrderDepthVideoBase(BaseModel):
    order_id: int = Field(..., description="Order ID")
    video_url: str | None = Field(default=None, description="Video URL")
    requested: bool = Field(default=False, description="Whether video was requested")


class OrderDepthVideoCreate(OrderDepthVideoBase):
    pass


class OrderDepthVideoUpdate(BaseModel):
    order_id: int | None = None
    video_url: str | None = None
    requested: bool | None = None


class OrderDepthVideoRead(OrderDepthVideoBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
