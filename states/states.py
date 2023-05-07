from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    startState = State()
    categoryState = State()
    timeState = State()
    subscriptionState = State()
    newsState = State()
    ready_newsState = State()
    planned_newsState = State()
