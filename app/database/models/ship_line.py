from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IdMixin


class ShipLine(IdMixin, Base):
    __tablename__ = "ship_lines"

    ship_line: Mapped[str] = mapped_column(String, nullable=False)
