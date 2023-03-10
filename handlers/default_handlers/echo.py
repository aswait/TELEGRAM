from telebot.types import Message
from states.start import Start

from loader import bot
from utils.logging import logger


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(content_types='text')
def bot_echo(message: Message):
    logger.info(f'user_name: {message.from_user.username} | user_id: {message.from_user.id} | command: {message.text}')
    if message.text.lower() == 'привет':
        bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    else:
        bot.reply_to(
            message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
        )
