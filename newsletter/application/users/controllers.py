from newsletter.application.users.ports import UsersStoragePort
from newsletter.domain.users.constants import RolesEnum
from newsletter.domain.users.models import User


class CreateUserController:
    def __init__(self, users_storage: UsersStoragePort):
        self._users_storage = users_storage

    async def execute(self, user: User) -> User:
        return await self._users_storage.create(user)


class GetUserController:
    def __init__(self, users_storage: UsersStoragePort):
        self._users_storage = users_storage

    async def execute(self, user_id: int) -> User:
        return await self._users_storage.get_by_id(user_id)


class GetUsersController:
    def __init__(self, users_storage: UsersStoragePort):
        self._users_storage = users_storage

    async def execute(self) -> list[User]:
        return await self._users_storage.get_all()


class ChangeRoleForUserController:
    def __init__(self, users_sotrage: UsersStoragePort):
        self._users_storage = users_sotrage

    async def execute(self, user_id: int, role: RolesEnum) -> None:
        await self._users_storage.change_role_by_id(user_id, role)
