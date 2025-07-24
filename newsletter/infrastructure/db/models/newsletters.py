from datetime import datetime
from typing import Any
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from newsletter.infrastructure.db.models.base import ModelBase
from newsletter.infrastructure.db.models.users import DatabaseUser


class DatabaseNewsletter(ModelBase):
    __tablename__ = "newsletters"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime())
    created_by_id: Mapped[int] = mapped_column(
        ForeignKey(DatabaseUser.id, ondelete="CASCADE")
    )
    created_by: Mapped[DatabaseUser] = relationship()
    send_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    text: Mapped[str] = mapped_column(Text())
    image_id: Mapped[str] = mapped_column(String(255), nullable=True)
    video_id: Mapped[str] = mapped_column(String(255), nullable=True)
    gif_id: Mapped[str] = mapped_column(String(255), nullable=True)
    reply_keyboard: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)


class DatabaseSentNewsletter(ModelBase):
    __tablename__ = "sent_newsletter"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime())
    target_id: Mapped[int] = mapped_column(
        ForeignKey(DatabaseUser.id, ondelete="CASCADE")
    )
    target: Mapped[DatabaseUser] = relationship()
    newsletter_id: Mapped[int] = mapped_column(
        ForeignKey(DatabaseNewsletter.id, ondelete="CASCADE")
    )
    newsletter: Mapped[DatabaseNewsletter] = relationship()
    is_success: Mapped[bool] = mapped_column(Boolean)
