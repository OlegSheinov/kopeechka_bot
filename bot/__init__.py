import asyncio
import functools
import logging
import os
from logging.handlers import RotatingFileHandler

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage


def setup_logger(logfile, level):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = RotatingFileHandler(logfile, maxBytes=10 ** 6, backupCount=5)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

    logger = logging.getLogger(logfile)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


info_log = setup_logger('logs/info.log', logging.INFO)
error_log = setup_logger('logs/error.log', logging.ERROR)


def log(info_message=None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with LoggingContext(info_log, message=info_message):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    async with LoggingContext(error_log):
                        error_log.error(e)

        return wrapper

    return decorator


class LoggingContext:
    def __init__(self, logger, level=logging.INFO, message=None):
        self.logger = logger
        self.level = level
        self.message = message

    async def __aenter__(self):
        if self.message is not None:
            self.logger.log(self.level, self.message)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.logger.log(logging.ERROR, exc_value)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


def create_bot():
    api_token = os.getenv('API_TOKEN')
    return Bot(token=api_token, parse_mode=ParseMode.HTML)


def create_storage():
    return RedisStorage.from_url("redis://localhost:6379/2")


def create_dispatcher():
    dp = Dispatcher()
    return dp


bot = create_bot()
