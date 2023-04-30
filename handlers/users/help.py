from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Почати діалог",
            "/help - Отримати поміч",
            "/choose_categories - Обрати категорії новин",
            "/choose_time - Обрати час отримання новин",
            "/subscription - Налаштувати отримання новин")

    await message.answer("\n".join(text))
