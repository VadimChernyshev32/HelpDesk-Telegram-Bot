import sqlite3


class BaseRepository:
    # Путь к файлу базы данных SQLite
    DB_PATH = 'app/database.db'

    def execute_query(self, query, params=None):
        """
        Выполняет SQL-запрос с опциональными параметрами.

        Если переданы параметры, они используются в запросе.
        Автоматически коммитит изменения в базу.
        Возвращает все полученные результаты (fetchall).
        """
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()
