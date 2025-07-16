from .base_repository import BaseRepository


class ExpectedWorkerRepository(BaseRepository):
    def create_tables(self):
        """
        Создает таблицу expected_worker, если её нет.
        Поля: id (PK), phone, organization, created_at (время создания, по умолчанию текущее время).
        """
        query = '''
            CREATE TABLE IF NOT EXISTS expected_worker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL,
                organization TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(query)

    def get_all_by_company(self, company: str) -> list:
        """
        Возвращает список всех ожидающих сотрудников конкретной компании.
        """
        query = 'SELECT * FROM expected_worker WHERE organization = ?'
        return self.execute_query(query, (company,))

    def get_all(self) -> list:
        """
        Возвращает список всех ожидающих сотрудников по всем компаниям.
        """
        query = 'SELECT * FROM expected_worker'
        return self.execute_query(query)

    def count_by_company(self, org: str) -> int:
        """
        Возвращает количество ожидающих сотрудников для указанной компании.
        """
        query = 'SELECT COUNT(*) FROM expected_worker WHERE organization = ?'
        result = self.execute_query(query, (org,))
        return result[0][0] if result else 0

    def get_all_records_by_phone(self, phone: str):
        """
        Возвращает все записи по номеру телефона ожидающего сотрудника.
        """
        query = "SELECT * FROM expected_worker WHERE phone = ?"
        return self.execute_query(query, (phone,))
