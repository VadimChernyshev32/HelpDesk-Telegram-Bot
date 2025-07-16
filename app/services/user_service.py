from app.repositories.user_repository import UserRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.expected_worker_repository import ExpectedWorkerRepository

from app.models.user import User
from app.models.expectedworker import ExpectedWorker

from config import ADMIN_USERS


class UserService:
    def __init__(self):
        # Инициализация репозиториев
        self.user_repo = UserRepository()
        self.company_repo = CompanyRepository()
        self.ticket_repo = TicketRepository()
        self.expected_worker_repo = ExpectedWorkerRepository()

    @staticmethod
    def is_user_admin(user_id: int) -> bool:
        # Проверка, является ли пользователь администратором
        return user_id in ADMIN_USERS

    def is_user_director(self, user_id: int) -> bool:
        # Проверка, является ли пользователь директором
        return self.user_repo.is_user_with_status(user_id, "director")

    def is_user_manager(self, user_id: int) -> bool:
        # Проверка, является ли пользователь менеджером
        return self.user_repo.is_user_with_status(user_id, "manager")

    def handle_start(self, user_id: int):
        """
        Метод вызывается при старте общения с пользователем.
        Проверяет статус, организацию и возвращает информацию для основного меню.
        """
        self.refresh_user_status_and_organization(user_id)

        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            # Если пользователь не зарегистрирован, запросить контакт
            return {
                "action": "request_phone",
                "message": "Добро пожаловать! Поделитесь контактом."
            }

        # Получаем информацию об организации
        org_name, org_address, org_phone = self.user_repo.get_organization_info(user_id)

        # Получаем количество активных и завершённых заявок
        open_tickets = len(self.ticket_repo.get_user_tickets(user_id, "В работе"))
        closed_tickets = len(self.ticket_repo.get_user_tickets(user_id, "Завершена"))

        # Возвращаем данные для отображения основного меню
        return {
            "action": "show_main_menu",
            "user": user,
            "org_name": org_name,
            "org_address": org_address,
            "org_phone": org_phone,
            "open_tickets": open_tickets,
            "closed_tickets": closed_tickets,
            "is_admin": self.is_user_admin(user_id),
            "is_director": self.is_user_director(user_id),
            "is_manager": self.is_user_manager(user_id)
        }

    def create_expected_worker(self, user_id: int, phone: str) -> dict:
        """
        Добавляет нового ожидаемого сотрудника в организацию пользователя.
        """
        org_info = self.user_repo.get_organization_info(user_id)
        org_name, *_ = org_info  # Получаем название организации

        # Создаём объект ожидаемого сотрудника
        expected_worker = ExpectedWorker.new_expected_worker(
            phone=phone,
            organization=org_name
        )

        # Сохраняем в базе
        self.user_repo.create_expected_worker(expected_worker)

        return {
            "success": True,
            "message": "Сотрудник добавлен в список ожидающих"
        }

    def refresh_user_status_and_organization(self, user_id: int):
        """
        Обновляет статус пользователя и его организацию на основе номера телефона.
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return

        phone = user.phone_user

        # 1. Проверка: является ли пользователь директором компании
        company = self.company_repo.get_company_by_director(phone)
        if company:
            # Обновляем статус и организацию
            self.user_repo.update_worker_status(user_id, "director")
            self.user_repo.update_user_organization(
                user_id,
                org_name=company.name,
                org_address=company.location,
                org_phone=company.phone
            )
            return

        # 2. Проверка по списку ожидаемых сотрудников
        expected_workers = self.expected_worker_repo.get_all_records_by_phone(phone)
        if expected_workers:
            org_name = expected_workers[0][2]  # Название организации
            company = self.company_repo.get_company_by_name(org_name)
            if company:
                # Обновляем статус и организацию
                self.user_repo.update_worker_status(user_id, "worker")
                self.user_repo.update_user_organization(
                    user_id,
                    org_name=company.name,
                    org_address=company.location,
                    org_phone=company.phone
                )

    def handle_contact(self, user_id: int, phone: str):
        """
        Обработка контакта, присланного пользователем.
        Регистрирует пользователя.
        """
        user = User.new_user(user_id, phone)
        self.user_repo.create_user(user)
        return {"action": "registration_success"}

    def get_user_position(self, user_id: int) -> str:
        # Получить должность пользователя
        return self.user_repo.get_user_position(user_id)

    def update_user_position(self, user_id: int, position: str):
        # Обновить должность пользователя
        self.user_repo.update_user_position(user_id, position)

    def update_worker_status(self, worker_id: int, status: str):
        # Обновить статус работника (например: worker, manager, etc.)
        self.user_repo.update_worker_status(worker_id, status)

    def get_company_info(self, user_id: int):
        # Получить информацию об организации пользователя
        return self.user_repo.get_organization_info(user_id)

    def get_all_users(self):
        # Получить список всех пользователей
        return self.user_repo.get_all_users()

    def get_users_by_status(self, status: str, org_name: str):
        # Получить список пользователей с определенным статусом в заданной организации
        return self.user_repo.get_users_by_status_company(status, org_name)

    def get_all_people_in_company(self, org_name: str):
        # Получить всех людей, зарегистрированных в указанной компании
        return self.user_repo.get_all_people_company(org_name)

    def get_user_info_by_id(self, user_id: int):
        # Получить информацию о пользователе по его ID
        return self.user_repo.get_user_by_id(user_id)
