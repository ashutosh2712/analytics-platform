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


class Dashboard(Base):

    __tablename__ = "dashboards"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
    )

    name = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    widgets = relationship(
        "Widget",
        back_populates="dashboard",
    )