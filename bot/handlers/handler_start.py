import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


async def get_welcome_message_and_send_message(message: Message, state: FSMContext):
    text = "Приветствуем вас. Введите ваш email, полученный от ...\n\n" \
           "Я проверю ваш код."
    await message.answer(text)


async def get_email_and_send_code(message: Message, state: FSMContext):
    if await is_valid_email(message.text):
        async with ClientSession() as session:
            async with session.post("http://0.0.0.0:8000/get_email_id", json={'email': message.text}) as response:
                email_id = await response.json()
            async with session.post("http://0.0.0.0:8000/get_code_from_id",
                                   json={'email_id': email_id}) as response:
                value_response = await response.json()
                if value_response == "WAIT_LINK":
                    text = "Ваше письмо еще не получено сервисом. Пожалуйста, повторите попытку через несколько минут!"
                elif value_response == "ACTIVATION_CANCELED":
                    text = "Ваша почта была отменена. Активируйте"
                else:
                    text = f"Ваш код, полученный с сайта: <code>{int(value_response)}</code>"
        await message.answer(text)

