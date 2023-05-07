from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отримати', callback_data='get')
        ],
        [
            InlineKeyboardButton(text='Відмовитись', callback_data='deny')
        ]
    ], resize_keyboard=True
)
