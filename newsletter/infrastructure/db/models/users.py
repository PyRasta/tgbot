from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy.types import String, Enum, BigInteger

from newsletter.domain.users.constants import RolesEnum
from newsletter.infrastructure.db.models.base import ModelBase


class DatabaseUser(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    role: Mapped[RolesEnum] = mapped_column(Enum(RolesEnum), default=RolesEnum.USER)
