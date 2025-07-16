from .base_repository import BaseRepository
from app.models.company import Company


class CompanyRepository(BaseRepository):
    def create_tables(self):
        """
        Создает таблицу companies, если она не существует.
        Столбцы: id (PK), name, location, phone, director_phone.
        """
        query = '''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT,
                phone TEXT,
                director_phone TEXT
            )
        '''
        self.execute_query(query)

    def create_company(self, company: Company):
        """
        Добавляет новую компанию в таблицу companies.
        Использует метод to_tuple() модели Company для данных.
        """
        query = '''
            INSERT INTO companies (name, location, phone, director_phone)
            VALUES (?, ?, ?, ?)
        '''
        self.execute_query(query, company.to_tuple())

    def get_company_by_director(self, director_phone: str) -> Company:
        """
        Получает компанию по номеру телефона директора.
        Возвращает объект Company или None, если не найдено.
        """
        query = "SELECT * FROM companies WHERE director_phone=?"
        result = self.execute_query(query, (director_phone,))
        if result and result[0]:
            return Company.from_tuple(result[0])
        return None

    def get_company_by_name(self, name: str):
        """
        Получает компанию по названию.
        Возвращает объект Company или None, если не найдено.
        """
        print(name)  # Возможно, для отладки
        query = "SELECT * FROM companies WHERE name = ?"
        result = self.execute_query(query, (name,))
        if result and result[0]:
            return Company.from_tuple(result[0])

    def get_all_companies(self):
        """
        Возвращает все записи из таблицы companies.
        Результат — список кортежей (сырые данные из базы).
        """
        query = "SELECT * FROM companies "
        result = self.execute_query(query)
        return result
