from newsletter.core.config import settings
from datetime import datetime


def get_datetime_now() -> datetime:
    return datetime.now(tz=settings.tz)
