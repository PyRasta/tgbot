import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from newsletter.application.users.controllers import (
    ChangeRoleForUserController,
    CreateUserController,
    GetUsersController,
)
from newsletter.domain.users.constants import RolesEnum
from newsletter.domain.users.models import User
from newsletter.infrastructure.db.storages.users import AlchemyUsersStorage
from newsletter.infrastructure.tg_bot.constants import CallbackDataEnum
from newsletter.infrastructure.tg_bot.dependencies import use_db_session
from newsletter.infrastructure.tg_bot.keyboards import (
    admin_keyboard,
    get_manage_users_keyboard,
    get_select_role_keyboard,
    moderator_keyboard,
)
from newsletter.infrastructure.tg_bot.users.factory_text import FactoryTexts

logger = logging.getLogger(__name__)
users_router = Router()


class ChangeRoleStates(StatesGroup):
    user_id = State()
    role = State()

@users_router.callback_query(F.data == CallbackDataEnum.VIEW_USERS.value)
async def view_users(callback: CallbackQuery, state: FSMContext):
    async for session in use_db_session():
        data = await state.get_data()
        main_message_id = data.get("main_message_id")
        users_storage = AlchemyUsersStorage(session)
        controller = GetUsersController(users_storage)
        users = await controller.execute()
        view_users_message = FactoryTexts.get_view_users(users)
        await state.update_data(view_users_message=view_users_message)
        await callback.bot.edit_message_text(
            text=view_users_message,
            chat_id=callback.message.chat.id,
            message_id=main_message_id,
            reply_markup=get_manage_users_keyboard()
        )

@users_router.callback_query(F.data == CallbackDataEnum.CHANGE_ROLE.value)
async def change_role(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    view_users_message = data.get("view_users_message")
    await state.set_state(ChangeRoleStates.user_id)
    await callback.bot.edit_message_text(
        text=f"Введите ID юзера\n{view_users_message}",
        chat_id=callback.message.chat.id,
        message_id=main_message_id
    )

@users_router.message(F.text, ChangeRoleStates.user_id)
async def get_user_id(message: Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await state.update_data(user_id=message.text)
    await state.set_state(ChangeRoleStates.role)
    await message.bot.edit_message_text(
        text="Выберите роль",
        chat_id=message.chat.id,
        message_id=main_message_id,
        reply_markup=get_select_role_keyboard()
    )

@users_router.callback_query(F.data.startswith("role_"), ChangeRoleStates.role)
async def set_user_role(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    if user_id is None:
        return

    main_message_id = data.get("main_message_id")
    role_str = callback.data.split("role_")[1]
    try:
        role = RolesEnum(role_str)
    except ValueError:
        await callback.answer("Некорректная роль", show_alert=True)
        return

    async for session in use_db_session():
        users_storage = AlchemyUsersStorage(session)
        controller = ChangeRoleForUserController(users_storage)
        await controller.execute(user_id=int(user_id), role=role)
        await callback.bot.edit_message_text(
            text=f"Роль пользователя с ID {user_id} успешно изменена на {role.value}",
            chat_id=callback.message.chat.id,
            message_id=main_message_id,
            reply_markup=get_manage_users_keyboard()
        )

    await state.clear()

@users_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    data = await state.get_data()
    if main_message_id := data.get("main_message_id"):
        await message.bot.delete_message(
            chat_id=message.chat.id, message_id=main_message_id
        )

    await state.clear()
    async for session in use_db_session():
        users_storage = AlchemyUsersStorage(session)
        controller = CreateUserController(users_storage)
        user = User(id=0, telegram_id=message.chat.id)
        user = await controller.execute(user)
        if user.role == RolesEnum.USER:
            r = await message.answer(f"Привет, {user.role.value}")
        else:
            r = await message.answer(
                f"Привет, {user.role.value}",
                reply_markup=admin_keyboard()
                if user.role == RolesEnum.ADMIN
                else moderator_keyboard(),
            )

        await state.set_data(
            {
                "current_user": user.model_dump(mode="json"),
                "main_message_id": r.message_id,
            }
        )
