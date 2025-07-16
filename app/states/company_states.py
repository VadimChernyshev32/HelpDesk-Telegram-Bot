from aiogram.fsm.state import StatesGroup, State


# Класс формы компании для пошагового ввода данных с помощью FSM (Finite State Machine)
class CompanyForm(StatesGroup):
    # Состояние для ввода названия компании
    name = State()

    # Состояние для ввода адреса (локации) компании
    location = State()

    # Состояние для ввода номера телефона компании
    phone = State()

    # Состояние для ввода ФИО директора компании
    director = State()
