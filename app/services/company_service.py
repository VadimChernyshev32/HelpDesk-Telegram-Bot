from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.models.company import Company
from app.services.expected_worker_service import ExpectedWorkerService
import phonenumbers


class CompanyService:
    def __init__(self):
        # Инициализация репозиториев и сервисов
        self.company_repo = CompanyRepository()
        self.user_repo = UserRepository()
        self.worker_repo = ExpectedWorkerService()

    def create_company(self, company_data: dict, user_id: int):
        # Проверка: существует ли уже компания с таким директором
        if self.company_repo.get_company_by_director(company_data['company_director']):
            return None, "Компания с таким номером директора уже существует"

        # Валидация номера телефона компании
        try:
            phone = phonenumbers.parse(company_data['company_phone'], "RU")
            if not phonenumbers.is_valid_number(phone):
                return None, "Некорректный номер телефона"
            # Приведение номера к международному формату
            company_data['company_phone'] = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
        except:
            return None, "Ошибка формата телефона"

        # Создание объекта Company из данных формы
        company = Company.from_form_data(company_data)
        # Сохранение компании в базу данных
        self.company_repo.create_company(company)

        # Обновление информации о пользователе (привязка к организации)
        self.user_repo.update_user_organization(
            user_id,
            company_data['company_name'],
            company_data['company_location'],
            company_data['company_phone']
        )

        return company, "Компания успешно создана"

    def get_company_info(self, user_id: int):
        # Получение информации об организации пользователя
        return self.user_repo.get_organization_info(user_id)

    def get_all_companies(self):
        # Получение всех компаний из базы данных
        return self.company_repo.get_all_companies()

    def get_rendered_people(self, org_name: str) -> list[tuple[str, str]]:
        """
        Формирует список сотрудников компании для отображения.
        Возвращает список кортежей: (строка описания, идентификатор для взаимодействия).
        """
        rendered_people = []

        # Получение сотрудников по ролям
        directors = self.user_repo.get_users_by_status_company("director", org_name)
        managers = self.user_repo.get_users_by_status_company("manager", org_name)
        workers = self.user_repo.get_users_by_status_company("worker", org_name)
        potential = self.worker_repo.get_all_by_company(org_name)

        # Добавление директоров
        rendered_people += [
            (f"Директор: {d.phone_user}", f"worker_{d.tg_id}")
            for d in directors
        ]

        # Добавление менеджеров
        rendered_people += [
            (f"Менеджер: {m.phone_user}", f"worker_{m.tg_id}")
            for m in managers
        ]

        # Добавление обычных сотрудников
        rendered_people += [
            (f"Сотрудник: {w.phone_user}", f"worker_{w.tg_id}")
            for w in workers
        ]

        # Добавление ожидаемых сотрудников (не зарегистрированы)
        rendered_people += [
            (f"Ожидаем входа: {pw[1]}", f"wait_{pw[0]}")
            for pw in potential
        ]

        return rendered_people

    def get_rendered_people_for_admin(self) -> list[tuple[str, str]]:
        """
        Формирует список всех сотрудников всех компаний для администратора.
        """
        rendered_people = []

        # Получение сотрудников по ролям (всех)
        directors = self.user_repo.get_all_users_by_status("director")
        managers = self.user_repo.get_all_users_by_status("manager")
        workers = self.user_repo.get_all_users_by_status("worker")
        potential = self.worker_repo.get_all_by_company("ТехноПромСервис")  # TODO: заменить на динамическое получение

        # Добавление директоров
        rendered_people += [
            (f"Директор: {d.phone_user}", f"worker_{d.tg_id}")
            for d in directors
        ]

        # Добавление менеджеров
        rendered_people += [
            (f"Менеджер: {m.phone_user}", f"worker_{m.tg_id}")
            for m in managers
        ]

        # Добавление обычных сотрудников
        rendered_people += [
            (f"Сотрудник: {w.phone_user}", f"worker_{w.tg_id}")
            for w in workers
        ]

        # Добавление ожидаемых сотрудников (ждут регистрации)
        rendered_people += [
            (f"Ожидаем входа: {pw[1]}", f"wait_{pw[0]}")
            for pw in potential
        ]

        return rendered_people
