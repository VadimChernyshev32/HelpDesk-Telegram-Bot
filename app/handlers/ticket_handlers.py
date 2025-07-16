from aiogram import F, types
from app.services.ticket_service import TicketService
from app.keyboards.ticket_keyboards import TicketKeyboards
from app.keyboards.common_keyboards import CommonKeyboards
from app.services.user_service import UserService
from app.filters.user_filters import UserPositionFilter
from config import ADMIN_MESSAGE


def register_ticket_handlers(dp, bot):  # Добавляем bot для отправки сообщений
    ticket_service = TicketService()
    keyboards = TicketKeyboards()
    user_service = UserService()
    common_keyboards = CommonKeyboards()

    @dp.callback_query(F.data == 'new_ticket')
    async def new_ticket_callback(query: types.CallbackQuery):
        user_service.update_user_position(query.from_user.id, "new_ticket")
        text, markup = keyboards.new_ticket()
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.message(UserPositionFilter('new_ticket'))
    async def handle_ticket_message(message: types.Message):
        response = ticket_service.create_ticket(message.from_user.id, message.text)

        if response:
            user_service.update_user_position(message.from_user.id, "ticket_sent")

            text, markup = keyboards.ticket_created(response["ticket_id"])
            await message.answer(text, reply_markup=markup, parse_mode="HTML")

            # Отправляем администратору уведомление о новой заявке
            await bot.send_message(ADMIN_MESSAGE, response["admin_message"])
        else:
            await message.answer("Ошибка при создании заявки")

    @dp.callback_query(F.data == 'my_ticket')
    async def my_tickets_callback(query: types.CallbackQuery):
        user_id = query.from_user.id
        tickets = ticket_service.get_user_tickets(user_id, "В работе")
        text, markup = keyboards.my_tickets(tickets)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data == 'my_ticket_history')
    async def my_ticket_history_entry_callback(query: types.CallbackQuery):
        user_id = query.from_user.id
        tickets = ticket_service.get_completed_tickets(user_id)
        text, markup = keyboards.my_ticket_history(tickets, user_id, page=1)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data.startswith('ticket_'))
    async def handle_ticket_details_callback(query: types.CallbackQuery):
        ticket_id = query.data.split('_')[1]
        ticket_info = ticket_service.get_ticket_info(ticket_id)

        if not ticket_info:
            await query.answer("Тикет не найден")
            return

        user_service.update_user_position(query.from_user.id, f'ticket_details_{ticket_id}')
        text, markup = keyboards.ticket_details(ticket_info)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data.startswith('my_ticket_page_'))
    async def handle_ticket_history_pagination(query: types.CallbackQuery):
        page = int(query.data.split('_')[3])
        user_id = query.from_user.id
        completed_tickets = ticket_service.get_completed_tickets(user_id)
        text, markup = keyboards.my_ticket_history(completed_tickets, user_id, page)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
        await query.answer()

    from app.filters.user_filters import TicketDetailPositionFilter

    @dp.message(TicketDetailPositionFilter())
    async def handle_ticket_comment(message: types.Message):
        position = user_service.get_user_position(message.from_user.id)
        ticket_id = int(position.split("_")[-1])  # Получаем ID тикета из позиции пользователя

        comment = message.text.strip()
        success = ticket_service.complete_ticket_with_comment(ticket_id, comment)

        if success:
            user_service.update_user_position(message.from_user.id, "main_menu")
            text, markup = common_keyboards.back_to_main_menu_message("✅ Комментарий добавлен и тикет завершён.")
        else:
            text, markup = common_keyboards.back_to_main_menu_message("⚠️ Не удалось завершить тикет.")

        await message.answer(text, reply_markup=markup)
