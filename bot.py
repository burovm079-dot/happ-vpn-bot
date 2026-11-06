import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Как подключить HAPP")],
        [KeyboardButton(text="ℹ️ Статус сервиса")],
    ],
    resize_keyboard=True,
)


async def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "replace_with_your_telegram_bot_token":
        raise RuntimeError(
            "Не задан BOT_TOKEN. Создайте .env на основе .env.example "
            "и добавьте токен от BotFather."
        )

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message) -> None:
        await message.answer(
            "Привет! Это бот проекта HAPP VPN.\n\n"
            "Сейчас проект находится в разработке: VPN-серверы и "
            "персональные конфигурации ещё не подключены. "
            "Я сообщу здесь, когда сервис будет готов.",
            reply_markup=keyboard,
        )

    @dp.message(Command("help"))
    async def help_command(message: Message) -> None:
        await message.answer(
            "Доступные команды:\n"
            "/start — открыть главное меню\n"
            "/help — помощь\n\n"
            "Пока бот работает в ознакомительном режиме."
        )

    @dp.message(F.text == "📱 Как подключить HAPP")
    async def happ_info(message: Message) -> None:
        await message.answer(
            "HAPP — приложение-клиент для VPN-конфигураций. "
            "Когда серверная часть будет настроена, здесь появится "
            "персональная ссылка подписки. Сейчас такой ссылки ещё нет."
        )

    @dp.message(F.text == "ℹ️ Статус сервиса")
    async def status(message: Message) -> None:
        await message.answer(
            "Статус: разработка.\n"
            "Telegram-бот: базовый каркас готов.\n"
            "VPN-серверы и выдача конфигураций: не настроены."
        )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
