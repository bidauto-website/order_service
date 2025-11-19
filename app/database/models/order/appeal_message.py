from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.order import AppealMessageRoleEnum
from ..base import Base
from ..mixins import IdMixin


if TYPE_CHECKING:
    from app.database.models import Appeal


class AppealMessage(IdMixin, Base):
    __tablename__ = "appeal_messages"

    appeal_id: Mapped[int] = mapped_column(ForeignKey("appeals.id"), nullable=False)
    message: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[AppealMessageRoleEnum] = mapped_column(Enum(AppealMessageRoleEnum), nullable=False)
    seen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    appeal: Mapped["Appeal"] = relationship("Appeal", back_populates="messages")
