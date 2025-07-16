import json
from dataclasses import dataclass
from datetime import datetime  # Для работы с текущим временем


@dataclass
class User:
    tg_id: int                 # Telegram ID пользователя
    phone_user: str            # Телефон пользователя
    organization_user: str     # Название организации пользователя
    organization_address: str  # Адрес организации
    organization_phone: str    # Телефон организации
    status: str                # Статус пользователя (например, роль или состояние)
    pos: str                   # Позиция или текущий раздел интерфейса пользователя
    data_reg: str              # Дата регистрации пользователя в формате строки
    profile: dict              # Дополнительные данные профиля в виде словаря

    @classmethod
    def from_tuple(cls, data: tuple):
        """
        Создает объект User из кортежа данных.
        Преобразует JSON-строку профиля в словарь.
        """
        return cls(
            tg_id=data[0],
            phone_user=data[1],
            organization_user=data[2],
            organization_address=data[3],
            organization_phone=data[4],
            status=data[5],
            pos=data[6],
            data_reg=data[7],
            profile=json.loads(data[8]) if data[8] else {}
        )

    def to_tuple(self):
        """
        Преобразует объект User в кортеж для сохранения,
        сериализуя словарь profile в JSON-строку.
        """
        return (
            self.tg_id,
            self.phone_user,
            self.organization_user,
            self.organization_address,
            self.organization_phone,
            self.status,
            self.pos,
            self.data_reg,
            json.dumps(self.profile)
        )

    @classmethod
    def new_user(cls, tg_id: int, phone: str):
        """
        Создает нового пользователя с дефолтными значениями
        для организации, статуса и позиции.
        Дата регистрации - текущее время.
        """
        return cls(
            tg_id=tg_id,
            phone_user=phone,
            organization_user="none",
            organization_address="none",
            organization_phone="none",
            status="undefined",
            pos="main_menu",
            data_reg=str(datetime.now()),  # Сохраняем время регистрации в строковом формате
            profile={}
        )
