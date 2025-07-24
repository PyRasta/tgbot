from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from newsletter.infrastructure.tg_bot.constants import CallbackDataEnum


def moderator_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Создать рассылку", callback_data=CallbackDataEnum.CREATE_NEWSLETTER.value
    )
    return keyboard.as_markup()


def admin_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Посмотреть юзеров", callback_data=CallbackDataEnum.VIEW_USERS.value
    )
    keyboard.button(
        text="Посмотреть запланированные рассылки",
        callback_data=CallbackDataEnum.VIEW_PLAIN_NEWSLETTERS.value,
    )
    return keyboard.as_markup()


def save_and_send_newsletter_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="Запустить сейчас",
        callback_data=CallbackDataEnum.SAVE_AND_SEND_NEWSLETTER.value,
    )
    keyboard.button(
        text="Запланировать время и дату запуска",
        callback_data=CallbackDataEnum.SETUP_DATETIME_FOR_NEWSLETTER.value,
    )
    return keyboard.as_markup()


def get_keyboard(text: str | None, url: str | None) -> InlineKeyboardMarkup | None:
    if text is None or url is None:
        return None

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, url=url)
    return keyboard.as_markup()
