from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppealBase(BaseModel):
    order_id: int = Field(..., description="Order ID")
    reason: str = Field(..., description="Appeal reason")
    solved: bool = Field(default=False, description="Whether appeal solved")


class AppealCreate(AppealBase):
    pass


class AppealUpdate(BaseModel):
    order_id: int | None = None
    reason: str | None = None
    solved: bool | None = None


class AppealRead(AppealBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
