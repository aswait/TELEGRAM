from loader import bot
from telebot.types import Message
from utils.history_message import history_message
from utils.logging import logger


@bot.message_handler(commands=['history'])
@logger.catch
def history(message: Message) -> None:
    logger.info(f'user_name: {message.from_user.username} | user_id: {message.from_user.id} | command: {message.text}')
    result = history_message(message.from_user.id)
    if result:
        bot.send_message(message.chat.id, result, disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "Записей не найдено 🤷‍♂️")
