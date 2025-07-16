from aiogram.filters import Filter
from aiogram.types import Message
from app.services.user_service import UserService

# Сервис для работы с пользователями
user_service = UserService()


class UserPositionFilter(Filter):
    # Проверяет, соответствует ли позиция пользователя заданной
    def __init__(self, position: str):
        self.position = position

    async def __call__(self, message: Message) -> bool:
        return user_service.get_user_position(message.from_user.id) == self.position


class TicketDetailPositionFilter(Filter):
    # Проверяет, начинается ли позиция пользователя с "ticket_details_"
    async def __call__(self, message: Message) -> bool:
        position = user_service.get_user_position(message.from_user.id)
        return position.startswith("ticket_details_")
