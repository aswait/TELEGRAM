from telebot.handler_backends import State, StatesGroup


class LowHighBest(StatesGroup):
    start = State()
    check_out = State()
    max_price = State()
    min_price = State()
