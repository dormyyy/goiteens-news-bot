from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import bot
from states.states import States
from loader import dp, session
from loader import bot as bot_a
from utils.db_api.postgres import *


@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    await States.startState.set()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        new_user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            subscribed=True,
            notification_time=9
        )
        session.add(new_user)
        session.commit()
        await message.answer(f"Привіт, {message.from_user.full_name}! Я телеграм бот, який буде надсилати тобі свіжі \
новини відповідно до твоїх побажань. Для вибору категорій новин, /choose_categories")
    else:
        await message.answer(f"Радий знову вітати, {message.from_user.full_name}! Для вибору категорій новин, \
/choose_categories")


@dp.message_handler(state=None)
async def bot_no_state(message: types.Message):
    await message.answer("Ви ще не почали роботу з ботом, або сесія була завершена! /start - запустити бота")


@dp.message_handler(commands=['start', 'get_news', 'choose_categories', 'choose_time', 'subscription'], state='*')
async def bot_none(message: types.Message):
    await message.answer('Ви уже працюєте з функціоналом, щоб викликати цю команду, завершіть активну дію!')


@dp.message_handler(state='*')
async def bot_none(message: types.Message):
    await message.answer('Це не команда! Спробуйте /help або /start')


@dp.callback_query_handler(lambda x: x.data, state='*')
async def bot_callback_none(callback_query: types.CallbackQuery):
    await bot_a.send_message(callback_query.from_user.id, 'Ця дія більше не активна! Спробуйте /help або /start')
