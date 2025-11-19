from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.order import AppealMessageRoleEnum


class AppealMessageBase(BaseModel):
    appeal_id: int = Field(..., description="Appeal ID")
    message: str | None = Field(default=None, description="Message text")
    role: AppealMessageRoleEnum = Field(..., description="Message author role")
    seen: bool = Field(default=False, description="Seen marker")


class AppealMessageCreate(AppealMessageBase):
    pass


class AppealMessageUpdate(BaseModel):
    appeal_id: int | None = None
    message: str | None = None
    role: AppealMessageRoleEnum | None = None
    seen: bool | None = None


class AppealMessageRead(AppealMessageBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
