from aiogram import F, types
from app.services.ticket_service import TicketService
from app.keyboards.admin_keyboards import AdminKeyboards
from app.services.user_service import UserService


def register_admin_handlers(dp):
    ticket_service = TicketService()
    keyboards = AdminKeyboards()
    user_service = UserService()

    @dp.callback_query(F.data == 'admin_panel')
    async def admin_panel_callback(query: types.CallbackQuery):
        if not UserService.is_user_admin(query.from_user.id):
            await query.answer("⛔️ Доступ запрещен!")
            return

        # Получаем все тикеты
        tickets = ticket_service.get_all_tickets()

        # Формируем и отправляем интерфейс админ-панели
        text, markup = keyboards.admin_panel(tickets)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data.startswith("admin_panel_page_"))
    async def handle_admin_panel_pagination(query: types.CallbackQuery):
        page = int(query.data.split("_")[-1])
        tickets = ticket_service.get_all_tickets()
        text, markup = keyboards.admin_panel(tickets, page)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
