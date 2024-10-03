# бот реагирует на команды /start и /help, чтобы предоставить базовое введение.
# Он также реагирует на команды /math, /date и /year, чтобы предоставлять факты определенных типов.
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F

from config import API_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Вспомогательная функция для получения факта о числе с помощью Numbers API
def get_number_fact(number, fact_type='trivia'):
    url = f'http://numbersapi.com/{number}/{fact_type}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Sorry, I couldn't get a fact for that number."

# Асинхронная функция для отправки приветственного сообщения
async def send_welcome(message: types.Message):
    await message.answer("Hi! I'm Number Facts Bot!\n"
                         "Send me a number, and I'll tell you something interesting about it.\n"
                         "You can also use /math, /date, or /year followed by a number to get specific types of facts.")

# Асинхронная функция для отправки специфического факта
async def send_specific_fact(message: types.Message):
    command = message.text.split()[0]
    fact_type = command.lstrip('/')
    number = message.text[len(command)+1:].strip()

    if not number:
        await message.reply(f"Please provide a number after the /{fact_type} command.")
        return

    fact = get_number_fact(number, fact_type)
    await message.reply(fact)

# Асинхронная функция для отправки тривиального факта
async def send_trivia_fact(message: types.Message):
    number = message.text.strip()
    if number.isdigit():
        fact = get_number_fact(number)
    else:
        fact = "Please send a valid number."
    await message.reply(fact)

# Регистрация обработчиков
dp.message.register(send_welcome, Command(commands=['start', 'help']))
dp.message.register(send_specific_fact, Command(commands=['math', 'date', 'year']))
dp.message.register(send_trivia_fact, F.text)

# Определяем функцию main
async def main():
    # Запуск бота
    await dp.start_polling(bot)

# Убедитесь, что имя '__main__' используется правильно
if __name__ == '__main__':
    asyncio.run(main())
