from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from config import UI_URL  # Импорт URL для web-приложения (UI)

class UserKeyboards:

    @staticmethod
    def request_phone_keyboard():
        # Клавиатура для запроса телефона у пользователя с кнопкой "Отправить номер"
        # request_contact=True - Телеграм попросит пользователя отправить свой контакт
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Отправить номер", request_contact=True)]],
            resize_keyboard=True,  # Клавиатура автоматически подстраивается под размер экрана
            one_time_keyboard=True  # После нажатия клавиатура скрывается
        )

    @staticmethod
    def format_main_menu_text(org_name, org_address, org_phone, open_tickets, closed_tickets):
        # Формируем текст главного меню с информацией о компании и количестве заявок
        return (
            f"<b>🧑‍💻 Главное меню</b>\n\n"
            f"📋 <b>Компания:</b> {org_name}\n"
            f"☎️ <b>Телефон:</b> {org_phone}\n"
            f"📍 <b>Адрес:</b> {org_address}\n\n"
            f"📬 <b>Открытых:</b> {open_tickets}   "
            f"📭 <b>Закрытых:</b> {closed_tickets}\n\n"
            "👇 Выберите действие:"
        )

    def main_menu(self, is_admin: bool, is_director: bool, is_manager: bool, user_id: int):
        # Создание инлайн-клавиатуры главного меню с учетом роли пользователя и id
        builder = InlineKeyboardBuilder()

        # Первая строка: кнопки создания новой заявки и просмотра своих заявок
        builder.row(
            InlineKeyboardButton(text="📤 Новая заявка", callback_data="new_ticket"),
            InlineKeyboardButton(text="📥 Мои заявки", callback_data="my_ticket")
        )
        # Вторая строка: кнопка для просмотра информации о компании пользователя
        builder.row(InlineKeyboardButton(text="🏢 Моя компания", callback_data="my_company"))

        # Третья строка: кнопка для перехода к web-приложению (UI), передаем user_id в URL
        builder.row(InlineKeyboardButton(
            text="📊 UI",
            web_app=WebAppInfo(url=f"{UI_URL}?user_id={user_id}")
        ))

        # Если пользователь директор или менеджер — показываем дополнительные кнопки управления заявками и сотрудниками
        if is_director or is_manager:
            builder.row(InlineKeyboardButton(text="👨‍💻 Контроль заявок", callback_data="direction_menu_ticket"))
            builder.row(InlineKeyboardButton(text="➕ Добавление сотрудника", callback_data="direction_menu_add_worker"))

        # Если пользователь администратор — показываем расширенное меню админа с кнопками управления тикетами и компаниями
        if is_admin:
            builder.row(InlineKeyboardButton(text="🤘 Тикет меню", callback_data="admin_panel"))
            builder.add(InlineKeyboardButton(text="➕ Компания", callback_data="make_company"))

        # Возвращаем сформированную клавиатуру в виде InlineKeyboardMarkup
        return builder.as_markup()

    def statistics_keyboard(self, user_id: int):
        # Клавиатура с одной кнопкой для перехода в web-приложение со статистикой по user_id
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="📊 Статистика",
            web_app=WebAppInfo(url=f"{UI_URL}?user_id={user_id}")
        ))
        return builder.as_markup()
