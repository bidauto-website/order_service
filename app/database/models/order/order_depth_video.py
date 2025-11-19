from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ..mixins import IdMixin

if TYPE_CHECKING:
    from app.database.models import Order


class OrderDepthVideo(IdMixin, Base):
    __tablename__ = "order_depth_video"

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False, unique=True)
    video_url: Mapped[str | None] = mapped_column(String, nullable=True)
    requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="depth_video")
