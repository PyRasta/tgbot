import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from newsletter.core.config import settings
from newsletter.infrastructure.tg_bot.users.routes import users_router
from newsletter.infrastructure.tg_bot.newsletters.routes import newsletters_router
from newsletter.infrastructure.tg_bot.bot import bot


async def main():
    dp = Dispatcher(storage=RedisStorage.from_url(settings.REDIS_URL))

    dp.include_router(users_router)
    dp.include_router(newsletters_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
