from datetime import datetime

from newsletter.core.config import settings


def get_datetime_now() -> datetime:
    return datetime.now(tz=settings.tz)
