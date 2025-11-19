from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ..mixins import IdMixin

if TYPE_CHECKING:
    from app.database.models import AppealMessage, Order


class Appeal(IdMixin, Base):
    __tablename__ = "appeals"

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False, unique=True)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    solved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="appeal")
    messages: Mapped[List["AppealMessage"]] = relationship(
        "AppealMessage", back_populates="appeal", cascade="all, delete-orphan"
    )
