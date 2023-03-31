from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.state import State

from bot.handlers.handler_start import get_welcome_message_and_send_message, get_email_and_send_code, \
    get_email_and_send_keyboard
from bot.settings.callback_data import EmailData
from bot.settings.states import MainState


def register_handlers(dp: Dispatcher):
    dp.message.register(get_welcome_message_and_send_message, Command(commands=["start"]), State(state="*"))
    dp.message.register(get_email_and_send_keyboard, MainState.start)
    dp.callback_query.register(get_email_and_send_code, EmailData.filter(), MainState.valid_email)
