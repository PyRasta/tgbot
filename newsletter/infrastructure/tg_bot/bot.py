
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from newsletter.core.config import settings

bot = Bot(
    token=settings.TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
