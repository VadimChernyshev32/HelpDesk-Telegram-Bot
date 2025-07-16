from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ticket:
    tg_id_ticket: int       # Telegram ID пользователя, создавшего заявку
    organization: str       # Название организации, к которой относится заявка
    addres_ticket: str      # Адрес, связанный с заявкой (например, место инцидента)
    message_ticket: str     # Сообщение/описание заявки
    time_ticket: str        # Время создания заявки в виде строки
    state_ticket: str       # Статус заявки ("В работе", "Закрыта" и т.п.)
    ticket_comm: str        # Комментарии по заявке
    number_ticket: int = None  # Номер заявки (идентификатор в базе), по умолчанию None

    @classmethod
    def from_tuple(cls, data: tuple):
        """
        Создает экземпляр Ticket из кортежа данных.
        Ожидаемый формат кортежа:
        (number_ticket, tg_id_ticket, organization, addres_ticket, message_ticket, time_ticket, state_ticket, ticket_comm)
        """
        return cls(
            number_ticket=data[0],
            tg_id_ticket=data[1],
            organization=data[2],
            addres_ticket=data[3],
            message_ticket=data[4],
            time_ticket=data[5],
            state_ticket=data[6],
            ticket_comm=data[7]
        )

    def to_tuple(self):
        """
        Преобразует объект Ticket в кортеж, готовый к сохранению.
        Поле number_ticket не включается, так как оно может быть автоматически присвоено БД.
        """
        return (
            self.tg_id_ticket,
            self.organization,
            self.addres_ticket,
            self.message_ticket,
            self.time_ticket,
            self.state_ticket,
            self.ticket_comm
        )

    @classmethod
    def new_ticket(cls, user_id: int, organization: str, address: str, message: str):
        """
        Создает новую заявку с текущим временем и статусом "В работе".
        Изначально number_ticket None, так как заявка ещё не сохранена в базе.
        """
        return cls(
            tg_id_ticket=user_id,
            organization=organization,
            addres_ticket=address,
            message_ticket=message,
            time_ticket=str(datetime.now()),  # Текущее время в строковом формате
            state_ticket="В работе",
            ticket_comm=""
        )
