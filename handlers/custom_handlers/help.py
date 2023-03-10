from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot
from utils.logging import logger


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    logger.info(f'user_name: {message.from_user.username} | user_id: {message.from_user.id} | command: {message.text}')
    bot.reply_to(message, help_message())


def help_message() -> str:
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    string = "\n".join(text)
    return string
