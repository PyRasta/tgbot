from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State

from newsletter.application.newsletters.controllers import CreateNewsletterController
from newsletter.domain.newsletters.models import Newsletter
from newsletter.domain.users.models import User
from newsletter.infrastructure.dramatiq.tasks import send_newsletter
from newsletter.infrastructure.tg_bot.constants import CallbackDataEnum
from newsletter.infrastructure.tg_bot.dependencies import use_db_session
from newsletter.infrastructure.tg_bot.keyboards import (
    admin_keyboard,
    get_keyboard,
    moderator_keyboard,
    save_and_send_newsletter_keyboard,
)
from datetime import datetime

from newsletter.infrastructure.tg_bot.newsletters.dependencies import (
    use_newsletters_storage,
)
from newsletter.utils.datetime import get_datetime_now
import logging


newsletters_router = Router()
logger = logging.getLogger(__name__)


class CreateNewsletterStates(StatesGroup):
    text = State()
    send_at = State()
    upload_content = State()
    inlune_buttons = State()
    save_and_send_newsletter = State()


class CreateSetupButtonsState(StatesGroup):
    text = State()
    url = State()


@newsletters_router.callback_query(
    F.data == CallbackDataEnum.CREATE_NEWSLETTER.value,
)
async def create_newsletter(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.set_state(CreateNewsletterStates.text)
    await callback.bot.edit_message_text(
        text="Введите в чат текст сообщения",
        chat_id=callback.message.chat.id,
        message_id=main_message_id,
    )


@newsletters_router.message(F.text, CreateNewsletterStates.text)
async def update_text_newsletter(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(text=message.text)
    await state.set_state(CreateNewsletterStates.upload_content)
    await message.bot.edit_message_text(
        text="Супер, теперь загрузите изображение/видео/гифку",
        chat_id=message.chat.id,
        message_id=main_message_id,
    )
    await message.delete()


@newsletters_router.message(F.photo, CreateNewsletterStates.upload_content)
async def update_image_id(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(image_id=message.photo[0].file_id)
    await state.set_state(CreateSetupButtonsState.text)
    await message.bot.edit_message_text(
        text="Отлично, теперь добавьте кнопку, напишите текст кнопки",
        chat_id=message.chat.id,
        message_id=main_message_id,
    )
    await message.delete()


@newsletters_router.message(F.video, CreateNewsletterStates.upload_content)
async def update_video_id(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(image_id=message.video.file_id)
    await state.set_state(CreateSetupButtonsState.text)
    await message.bot.edit_message_text(
        text="Отлично, теперь добавьте кнопку, напишите текст кнопки",
        chat_id=message.chat.id,
        message_id=main_message_id,
    )
    await message.delete()


@newsletters_router.message(F.animation, CreateNewsletterStates.upload_content)
async def update_animation_id(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(image_id=message.animation.file_id)
    await state.set_state(CreateSetupButtonsState.text)
    await message.bot.edit_message_text(
        text="Отлично, теперь добавьте кнопку, напишите текст кнопки",
        chat_id=message.chat.id,
        message_id=main_message_id,
    )
    await message.delete()


@newsletters_router.message(F.text, CreateSetupButtonsState.text)
async def update_text_button(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(text_button=message.text)
    await state.set_state(CreateSetupButtonsState.url)
    await message.bot.edit_message_text(
        text="Отлично, теперь ссылку к кнопке",
        chat_id=message.chat.id,
        message_id=main_message_id,
    )
    await message.delete()


@newsletters_router.message(F.text, CreateSetupButtonsState.url)
async def update_url_button(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(url_button=message.text)
    await state.set_state(CreateNewsletterStates.save_and_send_newsletter)
    await message.bot.edit_message_text(
        text="Почти всё, осталось отправить сразу либо запланировать время и дату отправки",
        chat_id=message.chat.id,
        message_id=main_message_id,
        reply_markup=save_and_send_newsletter_keyboard(),
    )
    await message.delete()


@newsletters_router.callback_query(
    F.data == CallbackDataEnum.SAVE_AND_SEND_NEWSLETTER.value,
    CreateNewsletterStates.save_and_send_newsletter,
)
async def save_and_send_newsletter(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    image_id = data.get("image_id")
    video_id = data.get("video_id")
    gif_id = data.get("gif_id")
    keyboard = get_keyboard(data.get("text_button"), data.get("url_button"))
    newsletter = Newsletter(
        id=0,
        created_at=get_datetime_now(),
        created_by=User.model_validate(data["current_user"]),
        text=data["text"],
        image_id=image_id,
        video_id=video_id,
        gif_id=gif_id,
        reply_keyboard=keyboard.model_dump() if keyboard is not None else None,
    )
    async for session in use_db_session():
        storage = use_newsletters_storage(session)
        controller = CreateNewsletterController(newsletters_storage=storage)
        newsletter = await controller.execute(newsletter)

    send_newsletter.send_with_options(args=(newsletter.id,))
    await callback.bot.edit_message_text(
        text="Отправлено",
        chat_id=callback.message.chat.id,
        message_id=main_message_id,
    )
