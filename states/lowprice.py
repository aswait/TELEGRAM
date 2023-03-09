from telebot.handler_backends import State, StatesGroup


class LowPrice(StatesGroup):
    start = State()
    check_out = State()
