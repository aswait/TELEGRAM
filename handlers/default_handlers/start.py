from telebot.types import Message

from loader import bot
from utils.logging import logger


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    logger.info(f'user_name: {message.from_user.username} | user_id: {message.from_user.id} | command: {message.text}')
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!"
                          f"\nЭто телеграм бот по поиску отелей"
                          f"\n/help - доступные команды")
