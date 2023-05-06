from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

navigate_news = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Далі')
        ],
        [
            KeyboardButton(text='Завершити')
        ]
    ], resize_keyboard=True
)
