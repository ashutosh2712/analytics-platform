from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
)

from sqlalchemy.orm import relationship

from app.models.base import Base


class Widget(Base):

    __tablename__ = "widgets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    dashboard_id = Column(
        Integer,
        ForeignKey("dashboards.id"),
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    chart_type = Column(
        String,
        nullable=False,
    )

    metric = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    dashboard = relationship(
        "Dashboard",
        back_populates="widgets",
    )