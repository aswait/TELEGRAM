from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def hotels_count() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    button_list = [InlineKeyboardButton(text=str(num),
                                        callback_data=f'count {str(num)}')
                   for num in range(1, 11)]
    keyboard.add(*button_list)

    return keyboard
