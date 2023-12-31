from loader import bot
from utils.logging import logger
from telebot.types import Message


@bot.message_handler(commands=["hello_world"])
def hello_world(message: Message) -> None:
    logger.info(f'user_name: {message.from_user.username} | user_id: {message.from_user.id} | command: {message.text}')
    bot.reply_to(message, "Hello, World")
