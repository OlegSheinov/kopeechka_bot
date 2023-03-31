from aiogram.filters.callback_data import CallbackData


class EmailData(CallbackData, prefix="email"):
    email: str
