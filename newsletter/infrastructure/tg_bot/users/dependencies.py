from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from newsletter.application.users.controllers import CreateUserController
from newsletter.application.users.ports import UsersStoragePort
from newsletter.infrastructure.db.storages.users import AlchemyUsersStorage
from newsletter.infrastructure.tg_bot.dependencies import use_db_session


def use_users_storage(
    session: Annotated[AsyncSession, Depends(use_db_session)],
) -> UsersStoragePort:
    return AlchemyUsersStorage(session)


def use_create_user_controller(
    users_storage: Annotated[UsersStoragePort, Depends(use_users_storage)],
) -> CreateUserController:
    return CreateUserController(users_storage=users_storage)
