from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.state import State

from bot.handlers.handler_start import get_welcome_message_and_send_message, get_email_and_send_code


def register_handlers(dp: Dispatcher):
    dp.message.register(get_welcome_message_and_send_message, Command(commands=["start"]), State(state="*"))
    dp.message.register(get_email_and_send_code, State(state="*"))
