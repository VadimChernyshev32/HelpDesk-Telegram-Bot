from aiogram import F, types
from app.services.ticket_service import TicketService
from app.keyboards.direction_keyboards import DirectionKeyboards
from app.services.user_service import UserService
from app.filters.user_filters import UserPositionFilter
from app.keyboards.common_keyboards import CommonKeyboards


def register_direction_handlers(dp):
    ticket_service = TicketService()
    user_service = UserService()
    keyboards = DirectionKeyboards()
    common_keyboards = CommonKeyboards()

    @dp.callback_query(F.data == 'direction_menu_ticket')
    async def direction_menu_ticket_callback(query: types.CallbackQuery):
        user_id = query.from_user.id

        # Получаем организацию пользователя
        org_info = user_service.get_company_info(user_id)
        user_org = org_info[0] if org_info else None
        if not user_org:
            await query.answer("Организация не найдена!")
            return

        tickets = ticket_service.get_all_tickets()
        text, markup = keyboards.direction_tickets_menu(user_id, tickets, user_org)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data.startswith("dir_panel_page_"))
    async def handle_dir_panel_page(query: types.CallbackQuery):
        page = int(query.data.split("_")[-1])
        user_id = query.from_user.id
        user = user_service.user_repo.get_user_by_id(user_id)
        tickets = ticket_service.get_all_tickets()
        text, markup = keyboards.direction_tickets_menu(user_id, tickets, user.organization_user, page)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(lambda query: query.data.startswith('worker_'))
    async def worker_menu(query: types.CallbackQuery):
        user_id = query.from_user.id
        response = user_service.handle_start(user_id)
        worker_id = int(query.data.split('_')[-1])
        worker_info = user_service.get_user_info_by_id(worker_id)
        if not worker_info:
            await query.message.edit_text("Сотрудник не найден")
            return

        tickets = ticket_service.get_all_tickets()
        text, markup = keyboards.worker_menu(
            tickets=tickets,
            worker_id=worker_id,
            phone_user=worker_info.phone_user,
            organization_user=worker_info.organization_user,
            status=worker_info.status,
            is_director=response["is_director"],
            is_manager=response["is_manager"]
        )
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(lambda query: query.data.startswith('update_worker_status_'))
    async def update_worker_status(query: types.CallbackQuery):
        worker_id = int(query.data.split('_')[-1])
        worker_info = user_service.get_user_info_by_id(worker_id)

        # Переключаем статус работника
        new_status = "manager" if worker_info.status == "worker" else "worker"
        user_service.update_worker_status(worker_id, new_status)

        text_worker, text_manager, markup = keyboards.update_worker_status(worker_id)
        text = text_worker if worker_info.status == "worker" else text_manager

        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data == 'direction_menu_add_worker')
    async def direction_menu_add_worker_callback(query: types.CallbackQuery):
        user_service.update_user_position(query.from_user.id, "direction_menu_add_worker")

        text, markup = keyboards.direction_menu_add_worker()
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.message(UserPositionFilter('direction_menu_add_worker'))
    async def handle_direction_menu_add_worker(message: types.Message):
        phone = message.text.strip()
        if not phone.startswith("+"):
            phone = "+" + phone

        cleaned = phone.replace("+", "")
        if not cleaned.isdigit() or len(cleaned) < 8:
            print(f"Некорректный номер: {phone}")
            await message.answer("❌ Пожалуйста, введите корректный номер телефона.")
            return

        result = user_service.create_expected_worker(
            user_id=message.from_user.id,
            phone=phone
        )
        user_service.update_user_position(message.from_user.id, "main_menu")

        response_text, markup = common_keyboards.back_to_main_menu_message(
            "✅ Сотрудник успешно добавлен в список ожидающих!" if result["success"] else "⚠️ Не удалось добавить сотрудника."
        )
        await message.answer(response_text, reply_markup=markup)
