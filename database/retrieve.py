from database.models import *
from typing import List


def retrieve_data(user_id: int) -> List[dict]:
    query = (Command
             .select()
             .limit(7)
             .order_by(Command.id)
             .where(Command.telegram_id == user_id))
    result = list()

    for entry in query:
        command_info = dict()
        command_info['command'] = entry.command
        command_info['date'] = entry.date_time.strftime("%d-%m-%y %H:%M:%S")

        hotels = Hotel.select().where(Hotel.command_id == entry.id)
        hotels_list = list()

        for hotel in hotels:
            hotel_info = {'name': hotel.name, 'url': hotel.url}
            hotels_list.append(hotel_info)

        command_info['hotels'] = hotels_list

        result.append(command_info)

    return result
