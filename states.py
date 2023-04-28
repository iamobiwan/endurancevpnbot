from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    MAIN = State()
    PROMOCODE = State()

class AdminBotStates(StatesGroup):
    ORDER_ID = State()