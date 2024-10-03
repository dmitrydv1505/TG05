# - **Обработчик команды `/start`**: Отвечает приветственным сообщением.
# - **Обработчик команды `/activity`**: Проверяет аргументы команды и делает запрос к API BoredAPI

import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import API_TOKEN

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я ваш бот для поиска активностей. Используйте /activity чтобы найти что-то интересное!"
    )

# Обработчик команды /activity
@dp.message(Command("activity"))
async def activity_handler(message: Message):
    # Получаем аргументы команды
    args = message.text.split()[1:]  # Исправлено получение аргументов
    query_type = args[0].lower() if args else None

    # Определяем URL в зависимости от аргумента
    if query_type == "diy":
        url = "http://www.boredapi.com/api/activity?type=diy"
    else:
        url = "http://www.boredapi.com/api/activity?minparticipants=5&maxparticipants=8"

    # Делаем запрос к API
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Формируем сообщение
                message_text = (
                    f"Активность: {data['activity']}\n"
                    f"Тип: {data['type']}\n"
                    f"Количество участников: {data['participants']}\n"
                    f"Сложность: {data['accessibility']}"
                )
                await message.answer(message_text)
            else:
                await message.answer("Не удалось получить данные. Попробуйте позже.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':  # Исправлено условие
    import asyncio
    asyncio.run(main())