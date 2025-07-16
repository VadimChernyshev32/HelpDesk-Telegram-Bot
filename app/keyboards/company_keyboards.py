from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.services.user_service import UserService
from app.services.company_service import CompanyService


class CompanyKeyboards:
    def __init__(self):
        # Инициализация сервисов для работы с пользователями и компаниями
        self.user_service = UserService()
        self.company_service = CompanyService()

    def my_company(self, company_info, page=1, page_size=6):
        # Распаковка информации о компании: название, адрес, телефон
        org_name, org_address, org_phone = company_info

        # Получение списка сотрудников компании для отображения
        # people — список кортежей (название кнопки, callback_data)
        people = self.company_service.get_rendered_people(org_name)

        # Сопоставляем роли сотрудников с соответствующими эмодзи для наглядности
        emoji_map = {
            "Директор": "🧔🏻‍♂️ ",
            "Менеджер": "👨🏻‍💻 ",
            "Сотрудник": "👨🏻‍💼 ",
            "Ожидаем входа": "⏳ "
        }

        decorated_people = []
        # Проходим по списку сотрудников и добавляем эмодзи перед ролью,
        # если роль присутствует в emoji_map
        for label, callback in people:
            for role, emoji in emoji_map.items():
                if label.startswith(role):
                    decorated_people.append((f"{emoji}{label}", callback))
                    break
            else:
                # Если роль не найдена в emoji_map, добавляем без изменений
                decorated_people.append((label, callback))

        # Определяем диапазон сотрудников, которые попадут на текущую страницу пагинации
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        current_page_people = decorated_people[start_index:end_index]

        # Формируем текст с основной информацией о компании
        text = (
            f"<b>🗄 Информация о компании</b>\n\n"
            f"<b>🏢 Компания: </b> {org_name}\n"
            f"<b>☎️ Контактный номер:</b> {org_phone}\n"
            f"<b>🗺️ Адрес:</b> {org_address}\n\n"
            f"<b>📋 Список сотрудников:</b>"
        )

        # Создаем билдер клавиатуры
        builder = InlineKeyboardBuilder()

        # Добавляем кнопки с сотрудниками текущей страницы
        for label, callback in current_page_people:
            builder.row(InlineKeyboardButton(text=label, callback_data=callback))

        # Если сотрудников больше, чем помещается на странице, добавляем навигацию по страницам
        if len(people) > page_size:
            nav = []
            if page > 1:
                # Кнопка "Предыдущая страница", если не первая страница
                nav.append(InlineKeyboardButton(text="🔙 Предыдущая", callback_data=f"company_page_{page - 1}"))
            if end_index < len(people):
                # Кнопка "Следующая страница", если есть еще сотрудники после текущей страницы
                nav.append(InlineKeyboardButton(text="🔜 Следующая", callback_data=f"company_page_{page + 1}"))
            builder.row(*nav)  # Добавляем навигационные кнопки в одну строку

        # Кнопка для возврата в главное меню
        builder.row(InlineKeyboardButton(text="⬅️ В меню", callback_data="main_menu"))

        # Возвращаем сформированный текст и клавиатуру в формате InlineKeyboardMarkup
        return text, builder.as_markup()
