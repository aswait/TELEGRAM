from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    bot.reply_to(message, help_message())


def help_message() -> str:
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    string = "\n".join(text)
    return string
