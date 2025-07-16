from aiogram import F, types
from aiogram.filters import Command
from app.services.user_service import UserService
from app.keyboards.user_keyboards import UserKeyboards
from app.services.ticket_service import TicketService
import phonenumbers
from phonenumbers import PhoneNumberFormat, NumberParseException


def register_user_handlers(dp):
    user_service = UserService()
    keyboards = UserKeyboards()
    ticket_service = TicketService()

    @dp.message(Command('start'))
    async def send_start(message: types.Message):
        response = user_service.handle_start(message.from_user.id)

        if response["action"] == "request_phone":
            await message.answer(
                response["message"],
                reply_markup=keyboards.request_phone_keyboard()
            )
        elif response["action"] == "show_main_menu":
            text = keyboards.format_main_menu_text(
                response["org_name"],
                response["org_address"],
                response["org_phone"],
                response["open_tickets"],
                response["closed_tickets"]
            )
            markup = keyboards.main_menu(
                is_admin=response["is_admin"],
                is_director=response["is_director"],
                is_manager=response["is_manager"],
                user_id=message.from_user.id
            )

            await message.answer(text, reply_markup=markup, parse_mode="HTML")

    @dp.message(F.contact)
    async def handle_contact(message: types.Message):
        raw_phone = message.contact.phone_number

        try:
            phone_obj = phonenumbers.parse(raw_phone, "RU")
            if not phonenumbers.is_valid_number(phone_obj):
                await message.answer("❌ Номер телефона недействителен. Попробуйте снова.")
                return
            phone = phonenumbers.format_number(phone_obj, PhoneNumberFormat.E164)  # +7922...
        except NumberParseException:
            await message.answer("❌ Ошибка обработки номера. Убедитесь, что он введён корректно.")
            return

        response = user_service.handle_contact(message.from_user.id, phone)

        if response["action"] == "registration_success":
            await message.answer(
                "✅ Регистрация успешна! Нажмите /start",
                reply_markup=types.ReplyKeyboardRemove()
            )

    @dp.message(Command('statistics'))
    async def show_statistics(message: types.Message):
        user_id = message.from_user.id
        markup = keyboards.statistics_keyboard(user_id)
        await message.answer("Статистика", reply_markup=markup)

    @dp.callback_query(F.data == 'main_menu')
    async def main_menu_callback(query: types.CallbackQuery):
        user_id = query.from_user.id
        response = user_service.handle_start(user_id)

        user_service.update_user_position(user_id, "main_menu")

        if response["action"] == "show_main_menu":
            text = keyboards.format_main_menu_text(
                response["org_name"],
                response["org_address"],
                response["org_phone"],
                response["open_tickets"],
                response["closed_tickets"]
            )
            markup = keyboards.main_menu(
                is_admin=response["is_admin"],
                is_director=response["is_director"],
                is_manager=response["is_manager"],
                user_id=user_id
            )

            await query.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
