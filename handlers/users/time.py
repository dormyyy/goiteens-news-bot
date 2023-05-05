from aiogram import types
from states.states import States
from loader import dp, bot, session
from utils.db_api.postgres import *


@dp.message_handler(state=States.startState, commands=['choose_time'])
async def bot_сhoose_time(message: types.Message):
    await States.timeState.set()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    times = {
        9: '9:00',
        13: '13:00',
        17: '17:00',
        21: '21:00'
    }
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=value, callback_data=str(key)) for key, value in times.items()
             if key != user.notification_time]
        ], resize_keyvoard=True
    )
    keyboard.inline_keyboard.extend([[types.InlineKeyboardButton(text='Не змінювати', callback_data='cancel')]])
    await message.answer(f"На разі у вас обраний час: {times.get(user.notification_time)}")
    await message.answer(f"Якщо ви хочете змінити час, оберіть його у списку, інкаше натисніть «Не змінювати»",
                         reply_markup=keyboard)


@dp.callback_query_handler(text='cancel', state=States.timeState)
async def bot_cancel_time(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Час отримання не змінено. Чекайте на ваші новини, або /get_news - отримати їх негайно!")
    await States.startState.set()


@dp.callback_query_handler(lambda x: x.data, state=States.timeState)
async def bot_сhange_time(callback_query: types.CallbackQuery):
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    times = {
        9: '9:00',
        13: '13:00',
        17: '17:00',
        21: '21:00'
    }
    time = int(callback_query.data)
    user.notification_time = time
    session.commit()
    await States.startState.set()
    await bot.send_message(callback_query.from_user.id,
                           f"Час отримання змінено на {times.get(time)}.\
Чекайте на ваші новини, або /get_news - отримати їх негайно!")
