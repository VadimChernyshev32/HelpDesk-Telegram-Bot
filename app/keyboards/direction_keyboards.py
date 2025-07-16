from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Tuple

class DirectionKeyboards:
    @staticmethod
    def direction_tickets_menu(user_id: int, tickets: List[Tuple], user_org: str, page: int = 1, page_size: int = 6) -> Tuple[str, InlineKeyboardMarkup]:
        filtered = [t for t in tickets if t[2] == user_org and t[6] == "В работе"]
        closed_count = len([t for t in tickets if t[2] == user_org and t[6] == "Завершена"])

        start = (page - 1) * page_size
        end = start + page_size
        current = filtered[start:end]

        text = (
            f"<b>🤘 Тикет меню 💲</b>\n\n"
            f"<b>🔥Заявок в работе:</b> {len(filtered)}\n"
            f"<b>👍Завершенных заявок:</b> {closed_count}\n\n"
            f"<b>⚠️ Внимание!</b> <i>Закрытые задачи не могут быть возвращены в работу. "
            f"Пожалуйста, будьте внимательны при их закрытии!</i>"
        )

        builder = InlineKeyboardBuilder()
        if current:
            for ticket in current:
                builder.row(InlineKeyboardButton(
                    text=f"Заявка №{ticket[0]} - {ticket[5]}",
                    callback_data=f"ticket_{ticket[0]}"
                ))
        else:
            text += "\n\n<i>Заявки отсутствуют на этой странице.</i>"

        total_pages = (len(filtered) + page_size - 1) // page_size
        if total_pages > 1:
            nav = []
            if page > 1:
                nav.append(InlineKeyboardButton(text="🔙 Назад", callback_data=f"dir_panel_page_{page - 1}"))
            if page < total_pages:
                nav.append(InlineKeyboardButton(text="🔜 Вперёд", callback_data=f"dir_panel_page_{page + 1}"))
            builder.row(*nav)

        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
        return text, builder.as_markup()


    def worker_menu(self, tickets: List[Tuple], worker_id: int, phone_user: str, organization_user: str, status: str,
                    is_director: bool = False, is_manager: bool = False) -> Tuple[str, InlineKeyboardMarkup]:
        text = (
            f"<b>Номер сотрудника:</b> <code>{phone_user}</code>\n"
            f"<b>Организация сотрудника:</b> <code>{organization_user}</code>\n"
            f"<b>Права в боте:</b> <code>{status}</code>"
        )

        builder = InlineKeyboardBuilder()

        # Заявки сотрудника для директора/менеджера
        if is_director or is_manager:
            for ticket in tickets:
                if ticket[6] == "В работе" and ticket[1] == worker_id:
                    builder.row(InlineKeyboardButton(
                        text=f"Заявка №{ticket[0]} - {ticket[5]}",
                        callback_data=f"ticket_{ticket[0]}"
                    ))

        # Управление правами (только директор)
        if status == "worker" and is_director:
            builder.row(InlineKeyboardButton(
                text="📈 Дать права менеджера",
                callback_data=f"update_worker_status_{worker_id}"
            ))
        elif status == "manager" and is_director:
            builder.row(InlineKeyboardButton(
                text="📉 Забрать права менеджера",
                callback_data=f"update_worker_status_{worker_id}"
            ))

        # Удаление сотрудника (только директор)
        if is_director:
            builder.row(InlineKeyboardButton(
                text="❌ Удалить сотрудника",
                callback_data=f"delete_user_{worker_id}"
            ))

        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="my_company"))
        return text, builder.as_markup()


    def update_worker_status(self, worker_id: int) -> Tuple[str, str, InlineKeyboardMarkup]:
        text_for_worker = "Теперь ваш сотрудник стал менеджером"
        text_for_manager = "Теперь ваш менеджер стал сотрудником"

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"worker_menu_{worker_id}"))
        return text_for_worker, text_for_manager, builder.as_markup()


    def direction_menu_add_worker(self) -> Tuple[str, InlineKeyboardMarkup]:
        text = (
            "<b>➕ Добавление сотрудника</b>\n"
            " - Введите номер сотрудника\n\n"
            "<b>Пример:</b> \n<i>+79222222222</i>"
        )

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
        return text, builder.as_markup()
