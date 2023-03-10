from database.models import *
from datetime import datetime
from utils.logging import logger
from typing import List


def db_command(hotel_info: List[dict], telegram_id: int, command: str) -> None:
    with db:
        entry = Command.create(telegram_id=str(telegram_id),
                               command=command,
                               date_time=datetime.now())

        for hotel in hotel_info:
            new_hotel = Hotel.create(name=hotel['name'],
                                     url=hotel['url'],
                                     command_id=entry.id)

    logger.info(f'tg.id {telegram_id} | new database entry')
