from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Отримати допомогу"),
            types.BotCommand("choose_categories", "Обрати категорії новин"),
            types.BotCommand("choose_time", "Обрати час новин"),
            types.BotCommand("subscription", "Налаштувати отримання новин"),
            types.BotCommand("get_news", "Отримати новини негайно")
        ]
    )
