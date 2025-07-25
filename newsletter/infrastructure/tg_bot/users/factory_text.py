from newsletter.domain.users.models import User


class FactoryTexts:
    @staticmethod
    def get_view_users(users: list[User]) -> str:
        message = f"Всего юзеров: {len(users)}\n"
        message += "\n".join([f"ID: {user.id}, Роль: {user.role.value}" for user in users])
        return message
