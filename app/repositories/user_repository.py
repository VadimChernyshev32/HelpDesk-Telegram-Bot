from .base_repository import BaseRepository
from app.models.user import User
from app.models.expectedworker import ExpectedWorker
import json
import datetime

class UserRepository(BaseRepository):
    # Создание таблицы пользователей, если она не существует
    def create_tables(self):
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                phone_user TEXT,
                organization_user TEXT,
                organization_address TEXT,
                organization_phone TEXT,
                status TEXT,
                pos TEXT,
                data_reg TEXT,
                profile TEXT
            )
        '''
        self.execute_query(query)

    # Получение пользователя по Telegram ID
    def get_user_by_id(self, user_id: int) -> User:
        query = 'SELECT * FROM users WHERE tg_id=?'
        result = self.execute_query(query, (user_id,))
        if result and result[0]:
            return User.from_tuple(result[0])  # Преобразуем кортеж в объект User
        return None

    # Создание нового пользователя
    def create_user(self, user: User):
        query = '''
            INSERT INTO users (tg_id, phone_user, organization_user, 
            organization_address, organization_phone, status, pos, data_reg, profile) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, user.to_tuple())  # Преобразуем объект в кортеж для вставки

    # Обновление позиции (экрана/состояния) пользователя
    def update_user_position(self, user_id: int, position: str):
        query = "UPDATE users SET pos = ? WHERE tg_id = ?"
        self.execute_query(query, (position, user_id))

    # Обновление статуса (роли) пользователя
    def update_worker_status(self, worker_id: int, status: str):
        query = "UPDATE users SET status = ? WHERE tg_id = ?"
        self.execute_query(query, (status, worker_id))

    # Обновление определённого поля JSON-профиля пользователя
    def update_profile_data(self, user_id: int, field: str, value: str):
        query = 'SELECT profile FROM users WHERE tg_id=?'
        result = self.execute_query(query, (user_id,))
        if result and result[0][0]:
            profile = json.loads(result[0][0])  # Распарсить JSON-строку
            profile[field] = value              # Обновить нужное поле
            update_query = "UPDATE users SET profile = ? WHERE tg_id = ?"
            self.execute_query(update_query, (json.dumps(profile), user_id))  # Сохранить обратно

    # Получить текущую позицию (экран) пользователя
    def get_user_position(self, user_id: int) -> str:
        query = "SELECT pos FROM users WHERE tg_id=?"
        result = self.execute_query(query, (user_id,))
        return result[0][0] if result and result[0] else "main_menu"

    # Получение информации об организации пользователя
    def get_organization_info(self, user_id: int):
        query = "SELECT organization_user, organization_address, organization_phone FROM users WHERE tg_id=?"
        result = self.execute_query(query, (user_id,))
        return result[0] if result else ("Не указано", "Не указано", "Не указано")

    # Получить номер телефона пользователя
    def get_user_phone(self, user_id: int) -> str:
        query = "SELECT phone_user FROM users WHERE tg_id=?"
        result = self.execute_query(query, (user_id,))
        return result[0][0] if result and result[0] else ""

    # Обновление данных об организации пользователя
    def update_user_organization(self, user_id: int, org_name: str, org_address: str, org_phone: str):
        query = """
            UPDATE users 
            SET organization_user = ?,
                organization_address = ?,
                organization_phone = ?
            WHERE tg_id = ?
        """
        self.execute_query(query, (org_name, org_address, org_phone, user_id))

    # Получить список всех пользователей
    def get_all_users(self):
        query = "SELECT * FROM users"
        result = self.execute_query(query)
        return [User.from_tuple(row) for row in result] if result else []

    # Получить всех пользователей по статусу и компании
    def get_users_by_status_company(self, status: str, organization_name: str) -> list[User]:
        """
        Возвращает список пользователей с указанным статусом и организацией.
        """
        query = "SELECT * FROM users WHERE status = ? AND organization_user = ?"
        result = self.execute_query(query, (status, organization_name))
        return [User.from_tuple(row) for row in result] if result else []

    # Получить всех пользователей по статусу
    def get_all_users_by_status(self, status: str) -> list[User]:
        """
        Возвращает список пользователей с указанным статусом.
        """
        query = "SELECT * FROM users WHERE status = ?"
        result = self.execute_query(query, (status,))
        return [User.from_tuple(row) for row in result] if result else []

    # Проверка, есть ли у пользователя определённый статус
    def is_user_with_status(self, user_id: int, status: str) -> bool:
        query = "SELECT 1 FROM users WHERE tg_id = ? AND status = ? LIMIT 1"
        result = self.execute_query(query, (user_id, status))
        return bool(result)

    # Получить всех пользователей конкретной компании
    def get_all_people_company(self, organization_name: str) -> list[User]:
        """
        Возвращает всех пользователей, относящихся к указанной компании.
        """
        query = "SELECT * FROM users WHERE organization_user = ?"
        result = self.execute_query(query, (organization_name,))
        return [User.from_tuple(row) for row in result] if result else []

    # Создание записи о «ожидаемом работнике»
    def create_expected_worker(self, expected_worker: ExpectedWorker) -> int:
        query = """
            INSERT INTO expected_worker (phone, organization, created_at)
            VALUES (?, ?, ?)
        """
        self.execute_query(query, expected_worker.to_tuple())

        return bool(query)  # Вернёт True, так как запрос существует, но это не проверка успеха вставки
