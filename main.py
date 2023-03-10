from loader import bot
from utils.logging import logger
import handlers  # noqa
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from database.models import *


logger.info('Bot started')


def main():
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()

    with db:
        db.create_tables([Command, Hotel])


if __name__ == "__main__":
    main()
    logger.info('Bot ended')
