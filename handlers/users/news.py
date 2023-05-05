from aiogram import types
from states.states import States
from loader import dp, bot, session
from utils.db_api.postgres import *
from sqlalchemy import MetaData
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


@dp.message_handler(state=States.startState, commands=['get_news'])
async def bot_get_news(message: types.Message):
    await message.answer("Зачекайте...")
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    user_categories = session.query(UserCategory).filter_by(user_id=user.id).all()
    categories_id = [i.category_id for i in user_categories]
    categories = {i.title: i for i in session.query(Category).filter(Category.id.in_(categories_id)).all()}
    news = {i: [] for i in categories.keys()}
    funcs = utils.parse.func_list
    for name, func in funcs:
        if name in news.keys():
            news[name] = func()
    session.query(UserNews).filter_by(user_id=user.id).delete()
    session.query(News).filter_by(user_added_id=user.id).delete()
    session.commit()
    for category, news_list in news.items():
        for i, new in enumerate(news_list):
            if i == 5:
                break
            new_new = News(
                category_id=categories[category].id,
                news=new,
                user_added_id=user.id
            )
            session.add(new_new)
        session.commit()
    for new in session.query(News).filter_by(user_added_id=user.id).all():
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
    new = user_news[0].news
    is_big = False
    if len(new) > 4096:
        substrings = split_string(new, 4096)
        is_big = True
    if not is_big:
        await bot.send_message(message.from_user.id, user_news[0].news)
    else:
        for i, text in enumerate(substrings):
            await bot.send_message(message.from_user.id, text)
    await States.newsState.set()
