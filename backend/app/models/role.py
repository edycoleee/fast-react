import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base
from backend.app.models.associations import role_permissions, user_roles
from backend.app.models.mixins import TimestampMixin


class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    users = relationship("User", secondary=user_roles, back_populates="roles", lazy="selectin")
    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles", lazy="selectin"
    )

