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


@dp.message_handler(state=States.startState, commands=['get_news'])
async def bot_get_news(message: types.Message):
    await message.answer("Зачекайте...")
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    user_categories = session.query(UserCategory).filter_by(user_id=user.id).all()
    if not user_categories:
        await message.answer("Оберіть категорії новин, які бажаєте отримувати: /choose_categories")
        return
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
    new = session.query(Category).filter_by(id=user_news[0].category_id).first().name + ':\n\n' + user_news[0].news
    is_big = False
    if len(new) > 4096:
        substrings = split_string(new, 4096)
        is_big = True
    if not is_big:
        await bot.send_message(message.from_user.id, new, reply_markup=navigate_news)
    else:
        for i, text in enumerate(substrings):
            await bot.send_message(message.from_user.id, text, reply_markup=navigate_news)
    await States.newsState.set()


@dp.message_handler(state=States.newsState, text='Завершити')
async def bot_cancel_news(message: types.Message):
    await States.startState.set()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    session.query(UserNews).filter_by(user_id=user.id).delete()
    session.query(News).filter_by(user_added_id=user.id).delete()
    session.commit()
    await message.answer("Перегляд новин завершено", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=States.newsState, text='Далі')
async def bot_navigate_news(message: types.Message):
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
        session.query(News).filter_by(user_added_id=user.id).delete()
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
