from aiogram import executor
from sqlalchemy.orm import sessionmaker
import time
from loader import dp, bot, session
import handlers
from utils.db_api.postgres import *
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
