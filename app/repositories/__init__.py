from .user_repository import UserRepository
from .ticket_repository import TicketRepository
from .company_repository import CompanyRepository
from .expected_worker_repository import ExpectedWorkerRepository

def init_db():
    UserRepository().create_tables()
    TicketRepository().create_tables()
    CompanyRepository().create_tables()
    ExpectedWorkerRepository().create_tables()
