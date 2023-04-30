from aiogram import types
from states.states import States
from loader import dp, bot, session
from utils.db_api.postgres import *


@dp.message_handler(state=States.startState, commands=['choose_categories'])
async def bot_сhoose_category(message: types.Message):
    await States.categoryState.set()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    categories = session.query(Category).all()
    categories = {i.title: i.name for i in categories}
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=value + ' - ' + '✅' if session.query(UserCategory).filter_by(
                user_id=user.id, category_id=session.query(Category).filter_by(title=key).first().id
            ).first() else value + ' - ' + '❌', callback_data=key)] for key, value in categories.items()
        ], resize_keyboard=True
    )
    keyboard.inline_keyboard.extend([[types.InlineKeyboardButton(text='Зберегти', callback_data='cancel')]])
    await message.answer(f"Оберіть категорії:", reply_markup=keyboard)


@dp.callback_query_handler(text='cancel', state=States.categoryState)
async def bot_cancel_category(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Категорії збережено. Щоб обрати час отримання новин /choose_time")
    await States.startState.set()


@dp.callback_query_handler(lambda x: x.data, state=States.categoryState)
async def bot_сhange_category(callback_query: types.CallbackQuery):
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    category = session.query(Category).filter_by(title=callback_query.data).first()
    user_category = session.query(UserCategory).filter_by(user_id=user.id, category_id=category.id).first()
    if not user_category:
        new_user_category = UserCategory(
            user_id=user.id,
            category_id=category.id
        )
        session.add(new_user_category)
        session.commit()
    else:
        session.delete(user_category)
        session.commit()
    categories = session.query(Category).all()
    categories = {i.title: i.name for i in categories}
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=value + ' - ' + '✅' if session.query(UserCategory).filter_by(
                user_id=user.id, category_id=session.query(Category).filter_by(title=key).first().id
            ).first() else value + ' - ' + '❌', callback_data=key)] for key, value in categories.items()
        ], resize_keyboard=True
    )
    keyboard.inline_keyboard.extend([[types.InlineKeyboardButton(text='Зберегти', callback_data='cancel')]])
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=keyboard)
