from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


class AdminKeyboards:
    def admin_panel(self, tickets, page: int = 1, page_size: int = 8):
        """
        tickets: list of tuples (ticket_id, ..., category, ..., description, status)
        """

        active_tickets = [t for t in tickets if t[6] == 'В работе']
        completed_tickets = [t for t in tickets if t[6] == 'Завершена']

        start = (page - 1) * page_size
        end = start + page_size
        current_page_tickets = active_tickets[start:end]

        text = (
            f"<b>🤘 Тикет меню 💲</b>\n\n"
            f"<b>🔥Заявок в работе:</b> {len(active_tickets)}\n"
            f"<b>👍Завершенных заявок:</b> {len(completed_tickets)}\n\n"
            f"<b>⚠️ Внимание!</b> <i>Закрытые задачи не могут быть возвращены в работу. "
            f"Пожалуйста, будьте внимательны при их закрытии!</i>\n\n"
        )

        builder = InlineKeyboardBuilder()

        if not current_page_tickets:
            text += "Нет заявок в работе на этой странице."
        else:
            for ticket in current_page_tickets:
                ticket_id = ticket[0]
                category = ticket[2]
                description = ticket[5]
                builder.row(
                    InlineKeyboardButton(
                        text=f"Заявка №{ticket_id} -{category}- {description}",
                        callback_data=f"ticket_{ticket_id}"
                    )
                )

        total_pages = (len(active_tickets) + page_size - 1) // page_size

        if total_pages > 1:
            nav_buttons = []
            if page > 1:
                nav_buttons.append(
                    InlineKeyboardButton(
                        text="🔙 Назад",
                        callback_data=f"admin_panel_page_{page - 1}"
                    )
                )
            if page < total_pages:
                nav_buttons.append(
                    InlineKeyboardButton(
                        text="🔜 Вперёд",
                        callback_data=f"admin_panel_page_{page + 1}"
                    )
                )
            builder.row(*nav_buttons)

        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))

        return text, builder.as_markup()
