from pydantic import BaseModel, ConfigDict

from newsletter.domain.users.constants import RolesEnum


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    role: RolesEnum = RolesEnum.USER
