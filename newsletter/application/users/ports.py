from abc import ABC, abstractmethod

from newsletter.domain.users.constants import RolesEnum
from newsletter.domain.users.models import User


class UsersStoragePort(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User: ...

    @abstractmethod
    async def get_all(self) -> list[User]: ...

    @abstractmethod
    async def change_role_by_id(self, user_id: int, role: RolesEnum) -> None: ...
