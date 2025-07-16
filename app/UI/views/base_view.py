# Импортируем библиотеку Flet для создания пользовательского интерфейса
import flet as ft

# Импортируем сервисы пользователей, заявок и компаний
from app.services import user_service, ticket_service, company_service

# Импортируем модуль для вывода ошибок
import traceback

# Базовый класс для всех представлений (view), используется для переиспользования логики
class BaseView:
    def __init__(self, page: ft.Page, tg_id: int):
        # Сохраняем переданные параметры страницы и Telegram ID
        self.page = page
        self.tg_id = tg_id

        try:
            # Инициализируем сервисы пользователей, заявок и компаний
            self.user_service = user_service.UserService()
            self.ticket_service = ticket_service.TicketService()
            self.company_service = company_service.CompanyService()
        except Exception as e:
            # Если произошла ошибка при инициализации сервисов — выводим стек ошибки
            traceback.print_exc()

        # Устанавливаем радиусы отображения секций на круговой диаграмме
        self.normal_radius = 50  # обычный радиус
        self.hover_radius = 65   # радиус при наведении

    def build(self):
        # Метод должен быть переопределён в подклассах
        raise NotImplementedError("Subclasses must implement this method")
