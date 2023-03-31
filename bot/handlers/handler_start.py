import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession

from bot.settings.callback_data import EmailData
from bot.settings.states import MainState


async def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


async def get_welcome_message_and_send_message(message: Message, state: FSMContext):
    text = "Приветствуем вас! Введите ваш email от аккаунта Facebook."
    await state.set_state(MainState.start)
    await message.answer(text)


async def get_email_and_send_keyboard(message: Message, state: FSMContext):
    if await is_valid_email(message.text):
        text = "Запросите код на почту, а затем нажмите «Получить код»."
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Получить код", callback_data=EmailData(email=message.text))
        await state.set_state(MainState.valid_email)
        await message.answer(text, reply_markup=keyboard.as_markup())
    else:
        text = "Некорректный email. Повторите попытку!"
        await message.answer(text)


async def get_email_and_send_code(query: CallbackQuery, state: FSMContext, callback_data: EmailData):
    async with ClientSession() as session:
        async with session.post("http://0.0.0.0:8000/get_email_id", json={'email': callback_data.email}) as response:
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
    await query.message.edit_text(text)
