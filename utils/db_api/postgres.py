from sqlalchemy import create_engine, Column, BigInteger, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
from environs import Env

env = Env()
env.read_env()

user = env.str('DB_USER')
password = env.str('DB_PASSWORD')
host = env.str('HOST')
database = env.str('DB_NAME')
port = env.str('PORT')

ENGINE = create_engine(env.str("DB_URL"))

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)
    username = Column(String, nullable=True)
    subscribed = Column(Boolean, nullable=False, default=True)
    notification_time = Column(Integer, nullable=True, default=9)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    name = Column(String, nullable=True)


class UserCategory(Base):
    __tablename__ = 'user_categories'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    category_id = Column(Integer, ForeignKey(Category.id))


Base.metadata.create_all(ENGINE)
print('Database Successfully created')
