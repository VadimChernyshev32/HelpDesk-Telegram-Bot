from aiogram import F, types
from aiogram.fsm.context import FSMContext

from app.services.company_service import CompanyService
from app.keyboards.company_keyboards import CompanyKeyboards
from app.keyboards.common_keyboards import CommonKeyboards
from app.states.company_states import CompanyForm
from app.services.user_service import UserService


def register_company_handlers(dp):
    company_service = CompanyService()
    keyboards = CompanyKeyboards()
    user_service = UserService()
    common_keyboards = CommonKeyboards()

    @dp.callback_query(F.data == 'my_company')
    async def my_company_callback(query: types.CallbackQuery):
        user_service.update_user_position(query.from_user.id, "my_company")
        user_id = query.from_user.id
        company_info = company_service.get_company_info(user_id)
        text, markup = keyboards.my_company(company_info)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(lambda query: query.data.startswith('company_page_'))
    async def handle_company_page_callback(query: types.CallbackQuery):
        page = int(query.data.split('_')[-1])  # Номер страницы
        await query.answer()  # Убираем крутилку
        company_info = company_service.get_company_info(query.from_user.id)
        text, markup = keyboards.my_company(company_info, page=page, page_size=6)
        await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

    @dp.callback_query(F.data == 'make_company')
    async def create_company_callback(query: types.CallbackQuery, state: FSMContext):
        await state.set_state(CompanyForm.name)
        await query.message.answer("Введите название компании")

    @dp.message(CompanyForm.name)
    async def handle_company_name(message: types.Message, state: FSMContext):
        await state.update_data(company_name=message.text)
        await state.set_state(CompanyForm.location)
        await message.answer("Введите адрес компании")

    @dp.message(CompanyForm.location)
    async def handle_company_location(message: types.Message, state: FSMContext):
        await state.update_data(company_location=message.text)
        await state.set_state(CompanyForm.phone)
        await message.answer("Введите контактный телефон")

    @dp.message(CompanyForm.phone)
    async def handle_company_phone(message: types.Message, state: FSMContext):
        await state.update_data(company_phone=message.text)
        await state.set_state(CompanyForm.director)
        await message.answer("Введите телефон директора")

    @dp.message(CompanyForm.director)
    async def handle_company_director(message: types.Message, state: FSMContext):
        await state.update_data(company_director=message.text)
        data = await state.get_data()

        # Создаём компанию, обрабатываем ошибки
        company, message_text = company_service.create_company(data, message.from_user.id)
        if not company:
            await message.answer(f"Ошибка: {message_text}")
            return

        text, markup = common_keyboards.back_to_main_menu_message(message_text)
        await message.answer(text, reply_markup=markup)
        await state.clear()
