from aiogram.types import InlineKeyboardMarkup
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AsyncIO

from newsletter.application.newsletters.controllers import (
    CreateSentNewsletterController,
    GetNewsletterController,
)
from newsletter.application.users.controllers import GetUsersController
from newsletter.core.config import settings
from newsletter.domain.newsletters.models import SentNewsletter
from newsletter.utils.datetime import get_datetime_now
import logging


redis_broker = RedisBroker(url=settings.REDIS_URL)
redis_broker.add_middleware(AsyncIO())
dramatiq.set_broker(redis_broker)
logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=0)
async def send_newsletter(newsletter_id: int):
    from newsletter.infrastructure.tg_bot.dependencies import use_db_session
    from newsletter.infrastructure.tg_bot.newsletters.dependencies import (
        use_newsletters_storage,
        use_sent_newsletters_storage,
    )
    from newsletter.infrastructure.tg_bot.users.dependencies import use_users_storage
    from newsletter.infrastructure.tg_bot.bot import bot

    async for session in use_db_session():
        sent_newsletters_storage = use_sent_newsletters_storage(session)
        newsletters_storage = use_newsletters_storage(session)
        users_storage = use_users_storage(session)
        create_sent_newsletter_controller = CreateSentNewsletterController(
            sent_newsletter_storage=sent_newsletters_storage
        )
        get_users_controller = GetUsersController(users_storage)
        get_newsletter_controller = GetNewsletterController(newsletters_storage)
        users = await get_users_controller.execute()
        newsletter = await get_newsletter_controller.execute(newsletter_id)
        keyboard = InlineKeyboardMarkup.model_validate(newsletter.reply_keyboard)
        for user in users:
            sent_newsletter = SentNewsletter(
                id=0,
                created_at=get_datetime_now(),
                target=user,
                newsletter=newsletter,
                is_success=True,
            )
            try:
                if newsletter.image_id is not None:
                    await bot.send_photo(chat_id=user.telegram_id, photo=newsletter.image_id, caption=newsletter.text, reply_markup=keyboard)
                if newsletter.video_id is not None:
                    await bot.send_video(chat_id=user.telegram_id, video=newsletter.video_id, caption=newsletter.text, reply_markup=keyboard)
                if newsletter.gif_id is not None:
                    await bot.send_animation(chat_id=user.telegram_id, animation=newsletter.gif_id, caption=newsletter.text, reply_markup=keyboard)
                else:
                    await bot.send_message(chat_id=user.telegram_id, text=newsletter.text, reply_markup=keyboard)
            except Exception as error:
                sent_newsletter.is_success = False
                logger.exception(error)

            await create_sent_newsletter_controller.execute(sent_newsletter)
