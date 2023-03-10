from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def photos_count() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    buttons = [InlineKeyboardButton(text=str(num),
                                    callback_data=f"photo {num}")
               for num in range(2, 11)]

    keyboard.add(*buttons)
    return keyboard
