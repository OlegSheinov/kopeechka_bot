import asyncio

from aiogram import Dispatcher

from bot import log, create_dispatcher, bot
from bot.handlers import register_handlers


async def start_all_handlers(dp: Dispatcher):
    register_handlers(dp)


@log(info_message="Start Bot!")
async def startup(dispatcher: Dispatcher):
    await start_all_handlers(dispatcher)


@log(info_message="Stop Bot!")
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()


async def start():
    dp = create_dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
