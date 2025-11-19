from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ..mixins import IdMixin

if TYPE_CHECKING:
    from app.database.models import Order


class Container(IdMixin, Base):
    __tablename__ = "containers"

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    ship_line: Mapped[str] = mapped_column(nullable=False, default="Unknown")
    vessel: Mapped[str] = mapped_column(nullable=False, default="Unknown")
    container_key: Mapped[str] = mapped_column(unique=True, nullable=False)

    # --- external calculator fields ---
    # -- destination
    destination_id: Mapped[int] = mapped_column(nullable=False)
    destination_name: Mapped[str] = mapped_column(nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="container")
