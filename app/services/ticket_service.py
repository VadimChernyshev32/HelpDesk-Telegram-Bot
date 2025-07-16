from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository
from app.models.ticket import Ticket


class TicketService:
    def __init__(self):
        # Инициализация репозиториев для работы с тикетами и пользователями
        self.ticket_repo = TicketRepository()
        self.user_repo = UserRepository()

    def create_ticket(self, user_id: int, message_text: str) -> dict:
        # Получаем информацию об организации пользователя
        org_info = self.user_repo.get_organization_info(user_id)
        if not org_info:
            # Если информация не найдена, подставляем заглушки
            org_name = "Не указано"
            org_address = "Не указано"
        else:
            org_name, org_address, _ = org_info  # Распаковка кортежа

        # Создаем объект тикета с помощью фабричного метода
        ticket = Ticket.new_ticket(
            user_id=user_id,
            organization=org_name,
            address=org_address,
            message=message_text
        )

        # Сохраняем тикет в БД и получаем его ID
        ticket_id = self.ticket_repo.create_ticket(ticket)

        # Получаем телефон пользователя
        user_info = self.user_repo.get_user_by_id(user_id)
        phone = user_info.phone if user_info and hasattr(user_info, 'phone') else "не указан"

        # Формируем текстовое сообщение для администратора
        admin_message = (
            f"📬 Новая заявка #{ticket_id}\n"
            f"От: {phone}\n"
            f"Организация: {org_name}\n"
            f"Адрес: {org_address}\n"
            f"Сообщение: {message_text}"
        )

        # Возвращаем ID тикета и сообщение для администратора
        return {
            "ticket_id": ticket_id,
            "admin_message": admin_message
        }

    def get_ticket_info(self, ticket_id: int) -> tuple:
        # Получаем тикет по ID
        ticket = self.ticket_repo.get_ticket_by_id(ticket_id)
        if not ticket:
            return None

        # Возвращаем основные поля тикета как кортеж
        return (
            ticket.number_ticket,
            ticket.tg_id_ticket,
            ticket.organization,
            ticket.addres_ticket,
            ticket.message_ticket,
            ticket.time_ticket,
            ticket.state_ticket,
            ticket.ticket_comm
        )

    def get_user_tickets(self, user_id: int, status: str = None):
        # Получаем тикеты пользователя, при необходимости фильтруем по статусу
        return self.ticket_repo.get_user_tickets(user_id, status)

    def get_all_tickets(self):
        # Получаем все тикеты из базы данных
        return self.ticket_repo.get_all_tickets()

    def get_completed_tickets(self, user_id: int) -> list:
        # Возвращает список завершенных тикетов пользователя
        return [
            ticket for ticket in self.ticket_repo.get_user_tickets(user_id)
            if ticket.state_ticket == "Завершена"
        ]

    def get_ticket_by_status(self, status: str) -> list[Ticket]:
        """
        Получить список всех тикетов с заданным статусом.

        :param status: Статус тикета (например, 'В работе', 'Завершена')
        :return: Список тикетов
        """
        tickets = self.ticket_repo.get_ticket_by_status(status)
        return tickets if tickets else []

    def get_ticket_by_status_and_company(self, status: str, company: str):
        # Получаем тикеты по статусу и названию компании
        tickets = self.ticket_repo.get_ticket_by_status_and_company(status, company)
        return tickets if tickets else []

    def complete_ticket_with_comment(self, ticket_id: int, comment: str) -> bool:
        # Получаем тикет по ID
        ticket = self.ticket_repo.get_ticket_by_id(ticket_id)
        if not ticket:
            return False

        # Добавляем комментарий и меняем статус на "Завершена"
        ticket.ticket_comm = comment
        ticket.state_ticket = "Завершена"

        # Обновляем тикет в базе данных
        return self.ticket_repo.update_ticket(ticket)
