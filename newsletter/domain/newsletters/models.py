from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any
from newsletter.domain.users.models import User


class Newsletter(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    created_by: User
    send_at: datetime | None = None
    text: str
    image_id: str | None = None
    video_id: str | None = None
    gif_id: str | None = None
    reply_keyboard: dict[str, Any] | None = None


class SentNewsletter(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    target: User
    newsletter: Newsletter
    is_success: bool
