from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.api_request import api_request
from typing import List
import json


def city_founding(city: str = 'Москва') -> List[dict]:
    response = api_request('locations/v3/search', {'q': '{}'.format(city), 'locale': 'ru_RU'}, 'GET')
    response = json.loads(response)

    cities_list = list()
    if response:
        for destination in response['sr']:  # Обрабатываем результат
            destination_id = destination.get('gaiaId')
            destination_name = destination['regionNames']['fullName']
            cities_list.append({
                'city_name': destination_name,
                'city_id': 'city {} {}'.format(destination_id, destination_name.split()[0])
            })
        return cities_list


def city_markup(city: str) -> InlineKeyboardMarkup:
    cities = city_founding(city)[:6]
    # Функция "city_founding" уже возвращает список словарей с нужным именем и id
    destinations = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=city.get('city_name'),
                                    callback_data=city.get('city_id')) for city in cities]
    destinations.add(*buttons)

    return destinations
