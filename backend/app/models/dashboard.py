from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Dashboard(Base, TimestampMixin):
    __tablename__ = "dashboards"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        index=True,
        
    )

    name: Mapped[str] = mapped_column(
        String(255)
    )

    widgets = relationship(
        "Widget",
        back_populates="dashboard",
        cascade="all, delete",
    )