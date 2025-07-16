from .base_repository import BaseRepository
from app.models.ticket import Ticket


class TicketRepository(BaseRepository):
    def create_tables(self):
        query = '''
            CREATE TABLE IF NOT EXISTS ticket (
                number_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id_ticket INTEGER,
                organization TEXT,
                addres_ticket TEXT,
                message_ticket TEXT,
                time_ticket TEXT,
                state_ticket TEXT,
                ticket_comm TEXT
            )
        '''
        self.execute_query(query)

    def create_ticket(self, ticket: Ticket) -> int:
        query = '''
            INSERT INTO ticket (tg_id_ticket, organization, addres_ticket, 
            message_ticket, time_ticket, state_ticket, ticket_comm)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, ticket.to_tuple())
        return self.get_last_ticket_id()

    def get_last_ticket_id(self) -> int:
        query = "SELECT number_ticket FROM ticket ORDER BY number_ticket DESC LIMIT 1"
        result = self.execute_query(query)
        return result[0][0] if result and result[0] else 0

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        query = "SELECT * FROM ticket WHERE number_ticket=?"
        result = self.execute_query(query, (ticket_id,))
        if result and result[0]:
            return Ticket.from_tuple(result[0])
        return None

    def get_all_tickets(self) -> list:
        query = "SELECT * FROM ticket"
        result = self.execute_query(query)
        return result if result else []



    def update_ticket_status(self, ticket_id: int, status: str):
        query = "UPDATE ticket SET state_ticket=? WHERE number_ticket=?"
        self.execute_query(query, (status, ticket_id))

    def update_ticket_comment(self, ticket_id: int, comment: str):
        query = "UPDATE ticket SET ticket_comm=? WHERE number_ticket=?"
        self.execute_query(query, (comment, ticket_id))

    def get_user_tickets(self, user_id: int, status: str = None) -> list[Ticket]:
        if status:
            query = "SELECT * FROM ticket WHERE tg_id_ticket=? AND state_ticket=?"
            result = self.execute_query(query, (user_id, status))
        else:
            query = "SELECT * FROM ticket WHERE tg_id_ticket=?"
            result = self.execute_query(query, (user_id,))

        return [Ticket.from_tuple(row) for row in result] if result else []

    def get_ticket_by_status(self, status: str) -> list[Ticket]:
        """
        Возвращает список всех заявок с указанным статусом.

        Args:
            status (str): Статус заявки (например: 'В работе', 'Завершена').

        Returns:
            list[Ticket]: Список заявок в виде объектов Ticket.
        """
        query = "SELECT * FROM ticket WHERE state_ticket = ?"
        result = self.execute_query(query, (status,))
        return [Ticket.from_tuple(row) for row in result] if result else []

    def get_ticket_by_status_and_company(self, status: str, company: str) -> list[Ticket]:

        query = "SELECT * FROM ticket WHERE state_ticket = ? and  organization = ?"
        result = self.execute_query(query, (status,company))
        return [Ticket.from_tuple(row) for row in result] if result else []

    def update_ticket(self, ticket: Ticket) -> bool:
        query = """
            UPDATE ticket
            SET state_ticket = ?, ticket_comm = ?
            WHERE number_ticket = ?
        """
        self.execute_query(query, (ticket.state_ticket, ticket.ticket_comm, ticket.number_ticket))
        return True



