from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from newsletter.application.users.controllers import CreateUserController
from newsletter.domain.users.constants import RolesEnum
from newsletter.domain.users.models import User
from newsletter.infrastructure.db.storages.users import AlchemyUsersStorage
from newsletter.infrastructure.tg_bot.dependencies import use_db_session
from newsletter.infrastructure.tg_bot.keyboards import (
    admin_keyboard,
    moderator_keyboard,
)


users_router = Router()


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
