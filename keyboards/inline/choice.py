from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def choice() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(text=f'✅ Да', callback_data='Yes'),
               InlineKeyboardButton(text=f'❌ Нет', callback_data='No')]

    keyboard.add(*buttons)
    return keyboard
