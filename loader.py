from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from data import config
from utils.db_api.postgres import *
from sqlalchemy.orm import sessionmaker

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

engine = ENGINE
Session = sessionmaker(engine)
session = Session()
if not session.query(Category).all():
    session.add(Category(
        title='kyiv',
        name='Київ'
    ))
    session.add(Category(
        title='lviv',
        name='Львів'
    ))
    session.add(Category(
        title='kharkiv',
        name='Харків'
    ))
    session.add(Category(
        title='vinnytsia',
        name='Вінниця'
    ))
    session.add(Category(
        title='dnipro',
        name='Дніпро'
    ))
    session.add(Category(
        title='odesa',
        name='Одеса'
    ))
    session.commit()
