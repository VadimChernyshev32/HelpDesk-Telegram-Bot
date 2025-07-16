from dataclasses import dataclass


@dataclass
class Company:
    # Основные поля класса Company с типами данных
    name: str               # Название компании
    location: str           # Местоположение / адрес компании
    phone: str              # Телефон компании
    director_phone: str     # Телефон директора компании
    id: int = None          # Уникальный идентификатор компании, по умолчанию None

    @classmethod
    def from_tuple(cls, data: tuple):
        """
        Создает экземпляр Company из кортежа данных.
        Предполагается, что кортеж идет в порядке:
        (id, name, location, phone, director_phone)
        """
        return cls(
            id=data[0],
            name=data[1],
            location=data[2],
            phone=data[3],
            director_phone=data[4]
        )

    def to_tuple(self):
        """
        Преобразует объект Company в кортеж.
        Используется для удобства передачи данных в БД или иные сервисы.
        Обратите внимание, id не включается в кортеж.
        """
        return (
            self.name,
            self.location,
            self.phone,
            self.director_phone
        )

    @classmethod
    def from_form_data(cls, data: dict):
        """
        Создает экземпляр Company из словаря с данными формы.
        Ожидаются ключи: company_name, company_location, company_phone, company_director.
        Если какого-то ключа нет, то подставляется пустая строка.
        """
        return cls(
            name=data.get('company_name', ''),
            location=data.get('company_location', ''),
            phone=data.get('company_phone', ''),
            director_phone=data.get('company_director', '')
        )
