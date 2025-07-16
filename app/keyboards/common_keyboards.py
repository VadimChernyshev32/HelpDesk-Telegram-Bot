from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


class CommonKeyboards:
    @staticmethod
    def back_to_main_menu_message(message_text: str):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
        return message_text, builder.as_markup()
