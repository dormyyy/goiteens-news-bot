from aiogram import executor
from sqlalchemy.orm import sessionmaker
import time, os, asyncio
import schedule
from utils.db_api.postgres import *
from threading import Thread
from loader import dp, bot, session
import handlers, utils
from states.states import States
from keyboards.inline import confirmation
from utils.db_api.postgres import *
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def get_user_ids(time) -> list:
    users = session.query(User).filter_by(subscribed=True, notification_time=time).all()
    return [i.telegram_id for i in users]


def load_news(time: int):
    categories = {i.title: i for i in session.query(Category).all()}
    news = {i: [] for i in categories.keys()}
    funcs = utils.parse.func_list
    for name, func in funcs:
        if name in news.keys():
            news[name] = func()
    old_news = session.query(News).filter_by(required_time=time, user_added_id=0)
    old_news_id = [i.id for i in old_news.all()]
    session.query(UserNews).filter(UserNews.news_id.in_(old_news_id)).delete()
    session.query(News).filter_by(required_time=time, user_added_id=0).delete()
    session.commit()
    for category, news_list in news.items():
        for i, new in enumerate(news_list):
            if i >= 5:
                break
            new_new = News(
                category_id=categories[category].id,
                news=new,
                required_time=time
            )
            session.add(new_new)
        session.commit()


async def send(user_ids):
    for user in user_ids:
        state = dp.current_state(user=user)
        current_state = await state.get_state()
        if current_state == States.startState.state:
            await state.set_state(States.ready_newsState)
            await bot.send_message(user, "Ваші новини готові!", reply_markup=confirmation)
        else:
            await bot.send_message(user, "Ваші новини не отримані, тому що ви зайняті іншою дією, \
або не обрали категорії отримуваних новин(/choose_categories). Після завершення дії, /get_news - отримати свіжі новини!")


async def load_21():
    load_news(21)
    user_ids = get_user_ids(21)
    await send(user_ids)


def news_21():
    send_fut = asyncio.run_coroutine_threadsafe(load_21(), loop)
    send_fut.result()


async def load_17():
    load_news(17)
    user_ids = get_user_ids(17)
    await send(user_ids)


def news_17():
    send_fut = asyncio.run_coroutine_threadsafe(load_17(), loop)
    send_fut.result()


async def load_13():
    load_news(13)
    user_ids = get_user_ids(13)
    await send(user_ids)


def news_13():
    send_fut = asyncio.run_coroutine_threadsafe(load_13(), loop)
    send_fut.result()


async def load_9():
    load_news(9)
    user_ids = get_user_ids(9)
    await send(user_ids)


def news_9():
    send_fut = asyncio.run_coroutine_threadsafe(load_9(), loop)
    send_fut.result()


def run_schedule():
    schedule.every().day.at("09:00").do(news_9)
    schedule.every().day.at("13:00").do(news_13)
    schedule.every().day.at("17:00").do(news_17)
    schedule.every().day.at("21:00").do(news_21)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    executor_news = Thread(target=run_schedule, args=())
    executor_news.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
