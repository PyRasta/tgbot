from pydantic import TypeAdapter
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from newsletter.application.users.ports import UsersStoragePort
from newsletter.domain.users.constants import RolesEnum
from newsletter.domain.users.exceptions import UserNotFoundError
from newsletter.domain.users.models import User
from newsletter.infrastructure.db.models.users import DatabaseUser


class AlchemyUsersStorage(UsersStoragePort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> User:
        exists_user = await self._get_by_telegram_id(user.telegram_id)
        if exists_user is not None:
            return exists_user

        query = (
            insert(DatabaseUser)
            .values(**user.model_dump(mode="json", exclude={"id"}))
            .returning(DatabaseUser.id)
        )
        result = await self._session.execute(query)
        user_id = result.scalar_one()
        user.id = user_id
        return user

    async def _get_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(DatabaseUser).where(DatabaseUser.telegram_id == telegram_id)
        result = await self._session.execute(query)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            return None

        return User.model_validate(db_user)

    async def get_all(self) -> list[User]:
        query = select(DatabaseUser)
        result = await self._session.execute(query)
        return TypeAdapter(list[User]).validate_python(result.scalars())

    async def get_by_id(self, user_id: int) -> User:
        query = select(DatabaseUser).where(DatabaseUser.id == user_id)
        result = await self._session.execute(query)
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise UserNotFoundError(f"Не найден пользователь с id={user_id}")

        return User.model_validate(db_user)

    async def change_role_by_id(self, user_id: int, role: RolesEnum) -> None:
        query = update(DatabaseUser).where(DatabaseUser.id == user_id).values(role=role)
        result = await self._session.execute(query)
        if not result.rowcount:
            raise UserNotFoundError(f"Не найден пользователь с id={user_id}")
