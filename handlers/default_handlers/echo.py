from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    else:
        bot.reply_to(
            message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
        )
