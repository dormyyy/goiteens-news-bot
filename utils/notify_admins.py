import logging
from loader import dp, bot, session
from utils.db_api.postgres import *
from aiogram import Dispatcher
from data.config import ADMINS
from states.states import States


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Запуск бота, /start")

        except Exception as err:
            logging.exception(err)
    for user in session.query(User).all():
        try:
            state = dp.current_state(user=user.telegram_id)
            current_state = await state.get_state()
            await state.set_state(States.startState)
        except Exception as err:
            logging.exception(err)
