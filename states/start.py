from telebot.handler_backends import State, StatesGroup


class Start(StatesGroup):
    start = State()
    check_out = State()
