import flet as ft
from app.UI.views import TicketsView, WorkersView, AdminView  # Импорт основных представлений из нового расположения
from config import ADMIN_USERS  # Импорт списка админов из конфигурации
from urllib.parse import urlparse, parse_qs  # Для парсинга параметров URL
import traceback  # Для подробного логирования исключений


def main(page: ft.Page):
    print("Initializing main page...")

    # Установка основных параметров страницы
    page.title = "HelpDesk Telegram Bot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"  # Позволяет странице прокручиваться при необходимости

    # Значение по умолчанию для Telegram ID пользователя (для тестирования)
    tg_id = 7486265

    # Попытка получить user_id из параметров URL (например, ?user_id=123)
    try:
        query_params = parse_qs(urlparse(page.route).query)
        print(f"Query params: {query_params}")

        # Если параметр user_id присутствует, используем его, иначе значение по умолчанию
        tg_id = int(query_params.get('user_id', [tg_id])[0])
        print(f"Using tg_id from params: {tg_id}")

    except Exception as e:
        # В случае ошибки выводим информацию и используем значение по умолчанию
        print(f"Error getting user_id from params: {str(e)}")
        print(f"Using default tg_id: {tg_id}")

    # Инициализация представлений (Views) по ключам индексов
    print("Initializing views...")
    views = {
        0: TicketsView(page, tg_id),  # Представление заявок
        1: WorkersView(page, tg_id)   # Представление сотрудников
    }

    # Если пользователь - админ, добавляем админское представление
    if tg_id in ADMIN_USERS:
        views[2] = AdminView(page, tg_id)
        print("Admin view added to views dictionary")

    print(f"Views initialized: {list(views.keys())}")

    # Функция обработки смены вкладки навигации
    def change_content(e):
        try:
            index = e.control.selected_index  # Получаем индекс выбранной вкладки
            if index in views:
                page.controls.clear()  # Очищаем текущие элементы страницы

                # Строим новое содержимое выбранного представления
                content = views[index].build()

                # Если контент - список виджетов, добавляем все сразу
                if isinstance(content, list):
                    page.add(*content)
                else:
                    page.add(content)

                page.update()  # Обновляем страницу

        except Exception as e:
            # При ошибке выводим подробный стек и сообщение об ошибке
            print(f"Error in change_content: {str(e)}")
            traceback.print_exc()
            page.add(ft.Text(f"Ошибка: {str(e)}", color="red"))
            page.update()

    # Формирование списка пунктов навигационного меню
    nav_destinations = [
        ft.NavigationDestination(icon=ft.icons.HELP_OUTLINE, label="Заявки"),
        ft.NavigationDestination(icon=ft.icons.PEOPLE, label="Сотрудники"),
    ]

    # Для админов добавляем пункт "Меню админа"
    if tg_id in ADMIN_USERS:
        nav_destinations.append(
            ft.NavigationDestination(icon=ft.icons.ADMIN_PANEL_SETTINGS, label="Меню админа")
        )

    # Создаем навигационную панель снизу с нужными пунктами и обработчиком смены вкладки
    page.navigation_bar = ft.NavigationBar(
        destinations=nav_destinations,
        on_change=change_content,
        selected_index=0  # По умолчанию открываем первую вкладку (Заявки)
    )

    # Функция для первоначальной загрузки начального содержимого страницы
    def load_initial_view():
        try:
            page.controls.clear()  # Очищаем все виджеты на странице

            # Строим содержимое первого представления (Заявки)
            content = views[0].build()

            if isinstance(content, list):
                page.add(*content)
            else:
                page.add(content)

            page.update()  # Обновляем страницу

        except Exception as e:
            # Логируем ошибки и показываем сообщение пользователю
            print(f"Error loading initial view: {str(e)}")
            traceback.print_exc()
            page.add(ft.Text(f"Ошибка загрузки: {str(e)}", color="red", size=24))
            page.update()

    # Загружаем начальное представление при запуске
    load_initial_view()


if __name__ == "__main__":
    # Запуск Flet-приложения с функцией main в качестве точки входа
    # view=None означает дефолтное поведение по открытию окна
    # порт 80 выбран для запуска веб-сервера
    ft.app(target=main, view=None, port=80)
