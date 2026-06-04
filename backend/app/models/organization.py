from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    memberships = relationship(
        "Membership",
        back_populates="organization",
        lazy="selectin",
    )

    api_keys = relationship(
        "ApiKey",
        back_populates="organization",
    )