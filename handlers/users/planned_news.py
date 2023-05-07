from aiogram import types
from states.states import States
from loader import dp, bot, session
from utils.db_api.postgres import *
from keyboards.default import navigate_news
import utils


def split_string(string, max_length):
    substrings = []
    start = 0
    length = len(string)

    while start < length:
        substring = string[start:start+max_length]
        substrings.append(substring)
        start += max_length

    return substrings


@dp.callback_query_handler(lambda x: x.data, state=States.ready_newsState)
async def bot_get_planned_news(callback_query: types.CallbackQuery):
    if callback_query.data == 'get':
        await States.planned_newsState.set()
    else:
        await States.startState.set()
        return
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    user_categories = [i.category_id for i in session.query(UserCategory).filter_by(user_id=user.id).all()]
    for new in session.query(News).filter(News.category_id.in_(user_categories), News.user_added_id == 0).all():
        new_user_new = UserNews(
            user_id=user.id,
            news_id=new.id
        )
        session.add(new_user_new)
        session.commit()
    user_news = session.query(News).filter(News.id.in_(
        [i.news_id for i in session.query(UserNews).filter_by(user_id=user.id).all()]
    )).order_by(News.category_id).all()
    user.current_news_id = user_news[0].id
    session.commit()
    new = session.query(Category).filter_by(id=user_news[0].category_id).first().name + ':\n\n' + user_news[0].news
    is_big = False
    if len(new) > 4096:
        substrings = split_string(new, 4096)
        is_big = True
    if not is_big:
        await bot.send_message(callback_query.from_user.id, new, reply_markup=navigate_news)
    else:
        for i, text in enumerate(substrings):
            await bot.send_message(callback_query.from_user.id, text, reply_markup=navigate_news)


@dp.message_handler(state=States.planned_newsState, text='Завершити')
async def bot_cancel_planned_news(message: types.Message):
    await States.startState.set()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    session.query(UserNews).filter_by(user_id=user.id).delete()
    session.commit()
    await message.answer("Перегляд новин завершено", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=States.planned_newsState, text='Далі')
async def bot_navigate_planned_news(message: types.Message):
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    user_categories = session.query(UserCategory).filter_by(user_id=user.id).all()
    user_news = session.query(News).filter(News.id.in_(
        [i.news_id for i in session.query(UserNews).filter_by(user_id=user.id).all()]
    )).order_by(News.category_id).all()
    news_id = [i.id for i in user_news]
    index = news_id.index(user.current_news_id)
    if index < len(news_id) - 1:
        index += 1
        user.current_news_id = news_id[index]
        session.commit()
    else:
        await States.startState.set()
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        session.query(UserNews).filter_by(user_id=user.id).delete()
        session.commit()
        await message.answer("Перегляд новин завершено", reply_markup=types.ReplyKeyboardRemove())
        return
    new_obj = session.query(News).filter_by(id=news_id[index]).first()
    new = session.query(Category).filter_by(id=new_obj.category_id).first().name + ':\n\n' + new_obj.news
    is_big = False
    if len(new) > 4096:
        substrings = split_string(new, 4096)
        is_big = True
    if not is_big:
        await bot.send_message(message.from_user.id, new, reply_markup=navigate_news)
    else:
        for i, text in enumerate(substrings):
            await bot.send_message(message.from_user.id, text, reply_markup=navigate_news)

