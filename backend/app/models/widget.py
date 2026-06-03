from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import WidgetType


class Widget(Base):
    __tablename__ = "widgets"

    id: Mapped[int] = mapped_column(primary_key=True)

    dashboard_id: Mapped[int] = mapped_column(
        ForeignKey(
            "dashboards.id",
            ondelete="CASCADE",
        )
    )

    widget_type: Mapped[WidgetType] = mapped_column(
        Enum(WidgetType)
    )

    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    dashboard = relationship(
        "Dashboard",
        back_populates="widgets",
    )