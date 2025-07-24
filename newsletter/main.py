import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from newsletter.core.config import settings
from newsletter.infrastructure.tg_bot.bot import bot
from newsletter.infrastructure.tg_bot.newsletters.routes import newsletters_router
from newsletter.infrastructure.tg_bot.users.routes import users_router


async def main():
    dp = Dispatcher(storage=RedisStorage.from_url(settings.REDIS_URL))

    dp.include_router(users_router)
    dp.include_router(newsletters_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
