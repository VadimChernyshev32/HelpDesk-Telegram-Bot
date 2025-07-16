from aiogram import Bot, Dispatcher  # Импорт основных классов для работы с Telegram Bot API
from app.handlers import register_handlers  # Импорт функции регистрации обработчиков сообщений
from config import BOT_TOKEN  # Токен бота из конфигурационного файла
import asyncio  # Для запуска асинхронного цикла событий
import logging  # Для логирования событий и ошибок
import sys  # Стандартный модуль, здесь не используется явно, можно убрать


async def main():
    # Создаем объект бота с указанным токеном
    bot = Bot(token=BOT_TOKEN)

    # Создаем диспетчер для регистрации и обработки событий/сообщений бота
    dp = Dispatcher()

    # Импортируем и инициализируем базу данных (например, подключение, миграции и т.п.)
    from app.repositories import init_db
    init_db()

    # Регистрируем все необходимые обработчики в диспетчере, передавая ему объект бота
    register_handlers(dp, bot)

    # Импортируем репозитории для работы с таблицами базы данных
    from app.repositories.user_repository import UserRepository
    from app.repositories.ticket_repository import TicketRepository
    from app.repositories.company_repository import CompanyRepository
    from app.repositories.expected_worker_repository import ExpectedWorkerRepository

    # Создаем таблицы, если их еще нет (инициализация схемы БД)
    UserRepository().create_tables()
    TicketRepository().create_tables()
    CompanyRepository().create_tables()
    ExpectedWorkerRepository().create_tables()

    # Запускаем процесс опроса Telegram для обработки входящих сообщений и событий
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Настройка базового логирования: уровень INFO и формат вывода логов с детализацией
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    # Запуск главной асинхронной функции в цикле событий
    asyncio.run(main())
