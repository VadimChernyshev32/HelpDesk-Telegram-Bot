from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

class TicketKeyboards:

    def new_ticket(self):
        # Сообщение для пользователя при создании новой заявки
        text = (
            f"<b>📤 Создание новой заявки</b>\n\n"
            f" - 🧩 Пожалуйста, опишите вашу проблему и укажите как можно подробнее.\n\n"
            f"<b>Пример оформления заявки:</b> \n<i>Не работает принтер на 4 ПК, необходимо проверить подключение.</i>"
        )
        builder = InlineKeyboardBuilder()
        # Кнопка "Назад" для возврата в главное меню
        builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
        return text, builder.as_markup()

    def ticket_created(self, ticket_id: int):
        # Сообщение об успешном создании заявки с номером тикета
        text = (
            f'🎉🥳 Успех, ваша заявка зарегистрирована! \n\n'
            f'<b>Номер заявки: </b><code>#{ticket_id}</code>. \n\n'
            f'<i>PS: Отслеживайте статус поставленных задач в разделе</i> <b>"📥 Мои заявки"</b>'
        )
        builder = InlineKeyboardBuilder()
        # Кнопка для перехода в главное меню после создания заявки
        builder.add(InlineKeyboardButton(text="🧑‍💻 Главное меню", callback_data="main_menu"))
        return text, builder.as_markup()

    def my_tickets(self, tickets: list):
        # Если заявок нет, выводим соответствующее сообщение
        if not tickets:
            text = '<b>📥 Мои заявки </b>\n\nУ вас пока нет заявок в работе..'
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
            return text, builder.as_markup()

        # Формируем заголовок и количество заявок
        text = (
            f"<b>📥 Мои заявки в работе</b>\n\n"
            f"<b>Заявок в работе:</b> {len(tickets)}\n\n"
        )
        builder = InlineKeyboardBuilder()

        # Для каждой заявки создаём кнопку с номером и временем заявки
        for ticket in tickets:
            text_button = f"Заявка #{ticket.number_ticket} - {ticket.time_ticket}"
            callback_data = f"ticket_{ticket.number_ticket}"
            # Добавляем кнопку в отдельную строку
            builder.row(InlineKeyboardButton(text=text_button, callback_data=callback_data))

        # Кнопка для просмотра истории заявок
        builder.row(InlineKeyboardButton(text="☑️ История заявок", callback_data="my_ticket_history"))
        # Кнопка назад в главное меню
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))

        return text, builder.as_markup()

    def my_ticket_history(self, tickets: list, user_id: int, page: int = 1, page_size: int = 4):
        # Рассчитываем срез для текущей страницы (пагинация)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        current_page = tickets[start_index:end_index]

        if current_page:
            # Формируем заголовок с номером страницы
            text = f"<b>📨 История ваших завершенных заявок (страница {page}):</b>\n\n"
            # Перебираем заявки текущей страницы и выводим детали
            for t in current_page:
                text += (
                    f"✅\n"
                    f"<b>├ Номер заявки:</b> <code>#{t.number_ticket}</code>\n"
                    f"<b>├ Время создания:</b> {t.time_ticket}\n"
                    f"<b>├ Сообщение:</b> - <em>{t.message_ticket}</em>\n"
                    f"<b>└ Комментарий исполнителя:</b> - <em>{t.ticket_comm}</em>\n\n"
                )
        else:
            # Если заявок нет, информируем пользователя
            text = "🤷‍♂️ Упс... У вас пока нет завершённых заявок."

        keyboard = InlineKeyboardBuilder()
        # Если заявок больше, чем помещается на страницу — добавляем кнопки навигации
        if len(tickets) > page_size:
            if page > 1:
                # Кнопка для перехода на предыдущую страницу
                keyboard.add(InlineKeyboardButton(text="🔙 Предыдущая", callback_data=f"my_ticket_page_{page - 1}"))
            if end_index < len(tickets):
                # Кнопка для перехода на следующую страницу
                keyboard.add(InlineKeyboardButton(text="🔜 Следующая", callback_data=f"my_ticket_page_{page + 1}"))
        # Кнопка назад к списку текущих заявок
        keyboard.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="my_ticket"))
        return text, keyboard.as_markup()

    def ticket_details(self, ticket_info: tuple) -> tuple[str, InlineKeyboardMarkup]:
        # Формируем подробную информацию по тикету с возможностью нажать на пользователя
        text = (f"<b>Детали заявки:</b> <code>#{ticket_info[0]}\n\n</code>"
                f"<b>Пользователь ID:</b> <a href='tg://user?id={ticket_info[1]}'>{ticket_info[1]}</a>\n"
                f"<b>Организация:</b> {ticket_info[2]}\n"
                f"<b>Адрес:</b> {ticket_info[3]}\n\n"
                f"<b>Сообщение от пользователя:</b> - <em>{ticket_info[4]}</em>\n\n"
                f"<b>Время создания:</b> {ticket_info[5]}\n"
                f"<b>Статус:</b> {ticket_info[6]}\n\n"
                f"<em>⚠️ Для завершения задачи введите комментарий. В ответ вам придет сообщение с подтверждением!</em>")

        keyboard = InlineKeyboardBuilder()
        # Кнопка назад в главное меню
        keyboard.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
        return text, keyboard.as_markup()
