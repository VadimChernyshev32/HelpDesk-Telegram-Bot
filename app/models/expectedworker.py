from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExpectedWorker:
    id: int                  # Уникальный идентификатор ожидаемого работника
    phone: str               # Телефон работника
    organization: str        # Название организации, куда ожидается работник
    created_at: str          # Время создания записи в формате строки

    @classmethod
    def from_tuple(cls, data: tuple):
        """
        Создает экземпляр ExpectedWorker из кортежа данных.
        Параметр data — кортеж вида (id, phone, organization, created_at)
        """
        return cls(
            id=data[0],
            phone=data[1],
            organization=data[2],
            created_at=data[3]
        )

    def to_tuple(self):
        """
        Преобразует объект ExpectedWorker в кортеж.
        Используется для передачи данных, например, в базу данных.
        id не включается, т.к. обычно он создается автоматически.
        """
        return (self.phone, self.organization, self.created_at)

    @classmethod
    def new_expected_worker(cls, phone: str, organization: str):
        """
        Создает новый объект ExpectedWorker с текущим временем создания.
        id изначально None, так как запись еще не сохранена в БД.
        """
        return cls(
            id=None,
            phone=phone,
            organization=organization,
            created_at=str(datetime.now())  # Время в строковом формате
        )
