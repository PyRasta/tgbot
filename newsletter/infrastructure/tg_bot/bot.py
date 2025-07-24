import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from newsletter.core.config import settings
from newsletter.infrastructure.tg_bot.users.routes import users_router
from newsletter.infrastructure.tg_bot.newsletters.routes import newsletters_router

bot = Bot(
    token=settings.TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
