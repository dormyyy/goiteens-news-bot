from aiogram import types
from states.states import States
from loader import dp, bot, session
from utils.db_api.postgres import *


@dp.message_handler(state=States.startState, commands=['subscription'])
async def bot_subscription(message: types.Message):
    await States.subscriptionState.set()
    keyboard_off = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Вимкнути', callback_data='off')]
        ], resize_keyvoard=True
    )
    keyboard_on = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Увімкнути', callback_data='on')]
        ], resize_keyvoard=True
    )
    keyboard_on.inline_keyboard.extend([[types.InlineKeyboardButton(text='Не змінювати', callback_data='cancel')]])
    keyboard_off.inline_keyboard.extend([[types.InlineKeyboardButton(text='Не змінювати', callback_data='cancel')]])
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if user.subscribed:
        await message.answer("На разі ваші повідомлення увімкнені, якщо ви бажаєте їх вимкнути, натисніть «Вимкнути»",
                             reply_markup=keyboard_off)
    else:
        await message.answer("На разі ваші повідомлення вимкнені, якщо ви бажаєте їх увімкнути, натисніть «Увімкнути»",
                             reply_markup=keyboard_on)


@dp.callback_query_handler(text='cancel', state=States.subscriptionState)
async def bot_cancel_bot_subscription(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Повідомлення не змінені. Чекайте своїх новин, або /get_news - отримати їх негайно!")
    await States.startState.set()


@dp.callback_query_handler(lambda x: x.data, state=States.subscriptionState)
async def bot_сhange_subscription(callback_query: types.CallbackQuery):
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    if callback_query.data == 'on':
        user.subscribed = True
    else:
        user.subscribed = False
    session.commit()
    await States.startState.set()
    await bot.send_message(callback_query.from_user.id, f"Налаштування сповіщеннь були успішно змінені!")
