from pydantic import BaseModel, ConfigDict
from datetime import datetime
from newsletter.domain.users.models import User
from typing import Any


class NewsletterDTO(BaseModel):
    id: int = 0
    created_at: datetime | None = None
    created_by: User | None = None
    send_at: datetime | None = None
    text: str | None = None
    image_id: int | None = None
    video_id: int | None = None
    gif_id: int | None = None
    reply_keyboard: dict[str, Any] | None = None
